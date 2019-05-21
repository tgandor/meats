from __future__ import print_function


class Dataclass:
    x = 0
    y = 0


pt1 = Dataclass()
print('pt1', pt1.x, pt1.y)

# except for constructor, it's all the same...
pt2 = Dataclass()

pt2.x = 5
pt2.y = 6
print('pt1', pt1.x, pt1.y) # 0 0
print('pt2', pt2.x, pt2.y) # 5 6

pt1.x += 1
# prototype not modified:
print('prototype:', Dataclass.x, Dataclass.y) # 0 0
print('pt1', pt1.x, pt1.y) # 1 0
