#ifndef PULSATING_COLORS_H
#define PULSATING_COLORS_H


#include <Arduino.h>
#include <FastLED.h>
#include "effect.h"
#include "structures.h"


class Pulsating_colors : public Effect
{
    private:
        transition_function bright_funct;
        CHSV color;
        bool not_changed;


    public:
        Pulsating_colors(CRGB* leds_arr, byte last_led_index, transition_function _bright_function, int _transition_time);
        ~Pulsating_colors();
        void do_step() override;
};


#endif