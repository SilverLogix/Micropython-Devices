import micropython


def bug_boot():
    import network
    import ubinascii
    import machine
    from os import statvfs
    import os
    import gc
    import time

    bits = statvfs('/flash')
    mbfree = bits[0] * bits[3] / (1024 * 1024)
    mac = ubinascii.hexlify(network.WLAN(1).config('mac'), ':').decode()
    dirr = str(os.listdir())
    time.sleep_ms(100)

    print("")
    print(f"MAC: {mac}")
    print(f"Mhz: {machine.freq() / 1e6:.0f}")
    print(f"Flash: {mbfree:.2f} MB")
    print("")
    print(f"Files: {dirr}")
    print("")

    del statvfs, network, ubinascii, machine, os
    gc.collect()


def time_it(f, n):
    import utime
    t0 = utime.ticks_us()
    f(n)
    t1 = utime.ticks_us()
    dt = utime.ticks_diff(t1, t0)
    fmt = '{:5.3f} sec, {:6.3f} usec/read : {:8.2f} kreads/sec'
    print(fmt.format(dt * 1e-6, dt / n, n / dt * 1e3))

    # time_it(showVoltage, N)


def serial_mem(mp: bool):
    import micropython

    micropython.mem_info(mp)
    del micropython


@micropython.native
def crash_esp32():
    import machine
    """
    Crash the ESP32 by writing to an invalid memory address.
    This will trigger a panic and reset the device.
    """
    # Define an invalid memory address (aligned to 4 bytes)
    address = 0x00000000  # Using address 0, which is typically unmapped

    try:
        # Attempt to read from the invalid address
        machine.mem32[address]
    except Exception as e:
        print(f"Crash attempt triggered an exception: {e}")
        print("ESP32 should reset now.")


def inf_recurs(depth=0):
    import utime
    """Crash by stack overflow due to infinite recursion."""
    print(f"Recursion depth: {depth}")
    utime.sleep_ms(1)  # Small delay to allow for print
    return inf_recurs(depth + 1)


def watchout():
    """Crash by triggering the watchdog timer."""
    # Disable the software WDT if it's running
    try:
        import machine
        machine.WDT(timeout=1000)  # 1 second timeout
    except:
        pass  # Hardware WDT might still be active

    print("Waiting for watchdog timer...")
    while True:
        pass  # Busy loop to prevent feeding the watchdog
