# ---------- #


def space_free():   # Display remaining free space
    from os import statvfs

    bits = statvfs('/flash')
    # print(str(bits))
    blksize = bits[0]  # 4096
    blkfree = bits[3]  # 12
    freesize = blksize * blkfree  # 49152
    mbcalc = 1024 * 1024  # 1048576
    mbfree = freesize / mbcalc  # 0.046875
    print("Free space:" + str(mbfree))


def m_freq():   # Get current machine Freq
    import machine

    gfr = str(machine.freq())

    print("Mhz: " + gfr)

    return gfr


def raw_temp():   # Get current CPU temp
    import esp32

    raw = str(esp32.raw_temperature())
    rtemp = ("CPU Temp: " + raw + "F")
    print(rtemp)
    rrr = rtemp
    return rrr


def showVoltage():   # Show current(pun intended) used Voltage
    # noinspection PyUnresolvedReferences
    from machine import ADC, Pin

    adc = ADC(Pin(32))

    vref = int(1100)

    v = adc.read()
    battery_voltage = (float(v) / 4095.0) * 2.0 * 3.3 * (vref / 1000.0)
    voltage = ("Voltage: {0:0.2f}v".format(battery_voltage))
    print(voltage)

    ddd = voltage
    return ddd


def getmac():   # Get and display chip MAC address
    import network
    import ubinascii
    mac = ubinascii.hexlify(network.WLAN(1).config('mac'), ':').decode()
    print(str(mac))


def pprint():   # Put it all together and PRINT
    import gc

    print("")
    print("-------------------")
    getmac()
    space_free()
    m_freq()
    raw_temp()
    showVoltage()
    print("--------------------")
    print("")

    gc.collect()


'''
N = 200_000
def time_it(f, n):
    t0 = utime.ticks_us()
    f(n)
    t1 = utime.ticks_us()
    dt = utime.ticks_diff(t1, t0)
    fmt = '{:5.3f} sec, {:6.3f} usec/read : {:8.2f} kreads/sec'
    print(fmt.format(dt * 1e-6, dt / n, n / dt * 1e3))

time_it(showVoltage, N)
'''
