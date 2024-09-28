
import machine
import debug
import gfx


machine.freq(80_000000)  # 240_

gfx.init()
gfx.boot(gfx.RED)

debug.bug_boot()

del debug
