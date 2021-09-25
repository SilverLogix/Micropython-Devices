# ---------- #


""" ========== from debug import "MODULE" ========= """


# noinspection PyUnusedLocal
@micropython.native
def pro_and_mem(f, *args, **kwargs):
    import utime
    import gc

    gc.collect()
    im = gc.mem_free()
    funcname = str(f).split(' ')[1]

    # noinspection PyShadowingNames
    @micropython.native
    def funcmem(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        ou = gc.mem_free()
        # print(im)
        # print(ou)
        print(f"Function ({funcname}) took = {delta / 1000:6.3f}ms and used {im-ou} of memory \n")
        return result
    return funcmem


''' ------------------------------------------------- '''


# noinspection PyUnusedLocal
@micropython.native
def profile(f, *args, **kwargs):
    import utime
    myname = str(f).split(' ')[1]

    # noinspection PyShadowingNames
    @micropython.native
    def new_fun(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print(f"Function ({myname}) time = {delta/1000:6.3f}ms \n")
        return result
    return new_fun


''' ------------------------------------------------- '''


# noinspection PyUnusedLocal
@micropython.native
def profile_total(f, *args, **kwargs):
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
        print(f"Function: ({f.__name__}) Call count = {ncalls} | Total time = {ttime/1000:6.3f}ms \n")
        return result

    return new_func


''' ------------------------------------------------- '''


# noinspection PyUnusedLocal
@micropython.native
def used_mem(f, *args, **kwargs):
    import gc
    gc.collect()
    im = gc.mem_free()
    name = str(f).split(' ')[1]

    # noinspection PyShadowingNames
    @micropython.native
    def new_mem(*args, **kwargs):
        result = f(*args, **kwargs)
        ou = gc.mem_free()
        to = (im - ou)
        print(f"Function ({name}) used memory = {to} \n")
        return result
    return new_mem


''' ------------------------------------------------- '''


# noinspection PyUnusedLocal
@micropython.native
def profile(f, *args, **kwargs):
    import utime
    myname = str(f).split(' ')[1]

    # noinspection PyShadowingNames
    @micropython.native
    def new_fun(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print(f"Function ({myname}) time = {delta/1000:6.3f}ms \n")
        return result
    return new_fun


''' ------------------------------------------------- '''


@micropython.viper
def serial_mem(mp: bool):   # Using True displays a map in the serial output
    import micropython
    if mp:
        micropython.mem_info(True)
    else:
        micropython.mem_info()


''' ------------------------------------------------- '''


@micropython.native
def files():
    import os
    dirr = str(os.listdir())
    print(f"Files: {dirr}")


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
    print(f"Flash: {mbfree}MB")


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
def show_voltage():   # Show current(pun intended) used Voltage
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
def get_mac():   # Get and display chip MAC address
    import network
    import ubinascii
    mac = ubinascii.hexlify(network.WLAN(1).config('mac'), ':').decode()
    print(f"MAC: {mac}")


@micropython.native
def b_print():   # Put it all together and PRINT
    import gc

    print(f"\n-------------------")
    get_mac()
    space_free()
    m_freq()
    raw_temp()
    show_voltage()
    files()
    print(f"-------------------- \n")

    gc.collect()
