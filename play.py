from key_reader.v00 import Reader
from model.v00 import Model
from world.v00 import World
from animation.v00 import Animation

model = Model()

for _ in range(1000):
    model.run()
