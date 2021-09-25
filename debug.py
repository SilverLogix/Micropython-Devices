# ---------- #


""" ========== from debug import "MODULE" ========= """


# noinspection PyUnusedLocal
@micropython.native
def profile(f, *args, **kwargs):
    ncalls = 0
    ttime = 0.0

    # noinspection PyShadowingNames
    @micropython.native
    def new_func(*args, **kwargs):
        import utime

        nonlocal ncalls, ttime
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        ncalls += 1
        ttime += delta
        print('Function: {} Call count = {} Total time = {:6.3f}ms'.format(f.__name__, ncalls, ttime / 1000))
        return result

    return new_func


''' ------------------------------------------------- '''


@micropython.viper
def serial_mem(mp: bool):
    import micropython
    micropython.mem_info(mp)


""" ================================================= """


@micropython.native
def space_free():   # Display remaining free space
    from os import statvfs

    bits = statvfs('/flash')
    # print(str(bits))
    blksize = bits[0]  # 4096
    blkfree = bits[3]  # 12
    freesize = blksize * blkfree  # 49152
    mbcalc = 1024 * 1024  # 1048576
    mbfree = freesize / mbcalc  # 0.046875
    print("Flash: " + str(mbfree) + "MB")


@micropython.viper
def getram():
    import gc
    rfree = str(gc.mem_free())
    print("RAM: " + rfree)


@micropython.viper
def m_freq():   # Get current machine Freq
    import machine

    gfr = str(machine.freq())

    print("Mhz: " + gfr)
    return gfr


@micropython.viper
def raw_temp():   # Get current CPU temp
    import esp32

    raw = str(esp32.raw_temperature())
    rtemp = ("CPU Temp: " + raw + "F")
    print(rtemp)

    rrr = rtemp
    return rrr


@micropython.native
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


@micropython.viper
def getmac():   # Get and display chip MAC address
    import network
    import ubinascii
    mac = ubinascii.hexlify(network.WLAN(1).config('mac'), ':').decode()
    print(str("MAC: " + mac))


def pprint():   # Put it all together and PRINT
    import gc

    print("")
    print("-------------------")
    getmac()
    space_free()
    getram()
    m_freq()
    raw_temp()
    showVoltage()
    print("--------------------")
    print("")

    gc.collect()
