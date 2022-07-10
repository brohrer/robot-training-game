import time
from key_reader.v00 import Reader
from model.v00 import Model
from world.v00 import World
from animation.v00 import Animation

name = f"{int(time.time())}"
model = Model(name)

for _ in range(1000):
    model.run()
