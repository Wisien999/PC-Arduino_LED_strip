#ifndef LINEAR_COLORS_H
#define LINEAR_COLORS_H


#include <Arduino.h>
#include <FastLED.h>
#include "effect.h"


class Linear_colors1 : public Effect
{
    private:
        byte curr_i;
        CRGB color;

    public:
        Linear_colors1(CRGB* leds_arr, byte last_led_index, int _transition_time);
        ~Linear_colors1();
        void do_step() override;
};


#endif