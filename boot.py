import micropython
import machine
import json

# noinspection PyArgumentList
machine.freq(240_000000)
micropython.alloc_emergency_exception_buf(100)

try:
    f = open("data.json", "r")
    f.close()    # continue with the file.

except OSError:  # open failed
    data = {"key": "value"}
    with open('data.json', 'w') as jsonfile:
        json.dump(data, jsonfile)

print(f"Booting......\n")
