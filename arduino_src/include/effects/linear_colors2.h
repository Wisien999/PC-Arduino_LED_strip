#ifndef LINEAR_COLORS2_H
#define LINEAR_COLORS2_H


#include <Arduino.h>
#include <FastLED.h>
#include "effect.h"



class Linear_colors2 : public Effect
{
    private:
        byte curr_i;
        uint8_t hue;
        bool fix_colors; // Fix colors after one 3-color cycle or allow it to change slightly


    public:
        Linear_colors2(CRGB* leds_arr, byte last_led_index, bool _fix_colors, int _transition_time);
        ~Linear_colors2();
        void do_step() override;
};


#endif