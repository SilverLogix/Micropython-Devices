
from sys import modules
import gc


global IP


# ----------- Connect to a router ----------- #
def connect_normal(ssid: str, passw: str):
    import network

    network.WLAN(0).active(False)
    network.WLAN(1).active(False)
    try:
        norm = network.WLAN(network.STA_IF) # noqa
        norm.active(True)
        norm.connect(ssid, passw)

        while not norm.isconnected():
            pass

        print('Connection successful')
        print(norm.ifconfig())
    except OSError:
        print("Wifi Internal Error, Rebooting\n")
        import machine
        machine.reset()


# ---------- Connect to a router with a static IP ---------- #
def connect_static(ssid: str, passw: str, static: str, routerip: str):
    import network

    stat = network.WLAN(network.STA_IF) # noqa
    stat.ifconfig((static, "255.255.255.0", routerip, routerip))
    stat.active(True)
    stat.connect(ssid, passw)

    while not stat.isconnected():
        pass

    print('Connection successful')
    print(str(stat.ifconfig()))


# --------- Create a Hotspot ---------- #
def access_point(ssid: str, pswd: str):
    import network

    ap = network.WLAN(network.AP_IF) # noqa
    ap.active(True)
    ap.config(essid=ssid, password=pswd, authmode=network.AUTH_WPA_WPA2_PSK, txpower=3) # noqa

    print('AP Active \n')

    varif = ap.ifconfig()
    print(varif[0]+'\n')

    global IP
    IP = str(varif[0])


def kill_all(cmd: bool):
    import network

    network.WLAN(0).active(cmd)
    network.WLAN(1).active(cmd)


def get_npt():
    #  (2023,   6,    7,   18,   0,  36,    2,      158)
    #   year, month, day, hour, min, sec, weekday, yearday

    import ntptime  # noqa
    import time
    ntptime.settime()  # this queries the time from an NTP server
    savings = 1
    utc = (-6 + savings) * 60 * 60  # change the '-4' according to your timezone
    actual_time = time.localtime(time.time() + utc)
    print("\n")
    print(actual_time)
    del modules["ntptime"]
    gc.collect()
    return actual_time


def ping(host, count=4, timeout=5000, interval=10, quiet=False, size=32):
    import utime
    import uselect
    import uctypes
    import usocket
    import ustruct
    import urandom # noqa

    def checksum(pkt):
        total = 0
        for i in range(0, len(pkt), 2):
            if i + 1 < len(pkt):
                total += (pkt[i] << 8) + pkt[i + 1]
            else:
                total += pkt[i] << 8
        while (total >> 16):
            total = (total & 0xffff) + (total >> 16)
        return ~total & 0xffff

    gc.collect()

    # prepare packet
    assert size >= 16, "pkt size too small"
    pkt = b'Q' * size
    pkt_desc = {
        "type": uctypes.UINT8 | 0,
        "code": uctypes.UINT8 | 1,
        "checksum": uctypes.UINT16 | 2,
        "id": uctypes.UINT16 | 4,
        "seq": uctypes.INT16 | 6,
        "timestamp": uctypes.UINT64 | 8,
    }
    h = uctypes.struct(uctypes.addressof(pkt), pkt_desc, uctypes.BIG_ENDIAN)
    h.type = 8  # ICMP_ECHO_REQUEST
    h.code = 0
    h.checksum = 0
    h.id = urandom.getrandbits(16)
    h.seq = 1

    # init socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_RAW, 1)
    sock.setblocking(0)
    sock.settimeout(timeout / 1000)
    addr = usocket.getaddrinfo(host, 1)[0][-1][0]  # ip address
    sock.connect((addr, 1))
    not quiet and print("PING %s (%s): %u data bytes" % (host, addr, len(pkt)))

    seqs = list(range(1, count + 1))  # [1,2,...,count]
    c = 1
    t = 0
    n_trans = 0
    n_recv = 0
    finish = False

    while t < timeout:
        if t == interval and c <= count:
            # send packet
            h.checksum = 0
            h.seq = c
            h.timestamp = utime.ticks_us()
            h.checksum = checksum(pkt)
            if sock.send(pkt) == size:
                n_trans += 1
                t = 0  # reset timeout
            else:
                seqs.remove(c)
            c += 1

        # recv packet
        while 1:
            socks, _, _ = uselect.select([sock], [], [], 0)
            if socks:
                resp = socks[0].recv(1024)
                resp_mv = memoryview(resp)
                h2 = uctypes.struct(uctypes.addressof(resp_mv[20:]), pkt_desc, uctypes.BIG_ENDIAN)
                # validate checksum (optional)
                seq = h2.seq
                if h2.type == 0 and h2.id == h.id and (seq in seqs):  # 0: ICMP_ECHO_REPLY
                    t_elasped = (utime.ticks_us() - h2.timestamp) / 1000
                    ttl = ustruct.unpack('!B', resp_mv[8:9])[0]  # time-to-live
                    n_recv += 1
                    not quiet and print("%u bytes from %s: icmp_seq=%u, ttl=%u, time=%f ms" % (len(resp), addr, seq, ttl, t_elasped))
                    seqs.remove(seq)
                    if len(seqs) == 0:
                        finish = True
                        break
            else:
                break

        if finish:
            break

        utime.sleep_ms(1)
        t += 1

    # close
    sock.close()
    ret = (n_trans, n_recv)
    not quiet and print("%u packets transmitted, %u packets received" % (n_trans, n_recv))
    gc.collect()
