#ifndef PULSATING_COLOR_H
#define PULSATING_COLOR_H


#include <Arduino.h>
#include <FastLED.h>
#include "effect.h"
#include "structures.h"


class Pulsating_color : public Effect
{
    private:
        transition_function bright_funct;
        CHSV color;


    public:
        Pulsating_color(CRGB* leds_arr, byte last_led_index, CHSV _color, transition_function _bright_function, int _transition_time);
        ~Pulsating_color();
        void do_step() override;
};


#endif