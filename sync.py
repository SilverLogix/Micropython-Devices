import uasyncio

async def sleep_5sec():
    while True:
        print('sleep 5 seconds')
        await uasyncio.sleep(5)

async def sleep_7sec():
    while True:
        print('sleep 7 seconds')
        await uasyncio.sleep(7)

if __name__ == '__main__':
    loop = uasyncio.get_event_loop()
    loop.create_task(sleep_5sec())  # schedule asap
    loop.create_task(sleep_7sec())
    loop.run_forever()
