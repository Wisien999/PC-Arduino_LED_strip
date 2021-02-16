#ifndef EFFECT_H
#define EFFECT_H
 
#include <FastLED.h>

#include "config.h"

class Effect
{
    protected:
        byte last_led;
        // CRGBArray<NUM_LEDS>* leds;
        CRGB* leds;
        int transition_time;
        unsigned long last_time;

    public:
        Effect(CRGB* leds_arr, byte last_led_index, int _transition_time);
        virtual ~Effect();

        virtual void do_step();
};

#endif