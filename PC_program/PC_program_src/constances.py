from enum import IntEnum

class EffectsIDs(IntEnum):
    FILL_SOLID = 10
    FILL_GRADIENT = 11
    LINEAR_COLORS = 12
    PULSATING_COLOR = 13
    PULSATING_COLORS = 14
    TRAVELING_PIXELS = 15


class OrdersIDs(IntEnum):
    STOP=0
    SET_BLENDING_RATIO=1
    FILL_SOLID=10 # Reserve first 10 indexes for custom commands
    FILL_GRADIENT=11
    LINEAR_COLORS=12
    PULSATING_COLOR=13
    PULSATING_COLORS=14
    TRAVELING_PIXELS=15

class Transition_functionsIDs(IntEnum):
    TRIWAVE=0
    CUBICWAVE=1
    QUADWAVE=2
    
