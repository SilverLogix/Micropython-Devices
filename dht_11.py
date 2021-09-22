
class dht_11(object):
    def __init__(self, pinn):
        import uasyncio
        import machine
        d = dht.DHT11(machine.Pin(pinn, machine.Pin.PULL_UP))

        print("Init")

