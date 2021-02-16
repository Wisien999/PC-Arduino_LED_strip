#ifndef STRUCTURES_H
#define STRUCTURES_H

enum transition_function
{
    TRIWAVE,
    CUBICWAVE,
    QUADWAVE
};


enum Order
{
    STOP,
    SET_BLENDING_RATIO,
    FILL_SOLID=10, // Reserve first 10 indexes for custom commands
    FILL_GRADIENT,
    LINEAR_COLORS,
    PULSATING_COLOR,
    PULSATING_COLORS,
    TRAVELING_PIXELS
};


#endif