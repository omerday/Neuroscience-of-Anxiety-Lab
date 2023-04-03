from psychopy import parallel
from psychopy import core

port = parallel.setPortAddress(int("0xE050", 16))
parallel.setData(0)

core.wait(10)

parallel.setData(200)

core.wait(5)

core.quit()