#ifndef TRAVELING_PIXELS_H
#define TRAVELING_PIXELS_H


#include <Arduino.h>
#include <FastLED.h>
#include "effect.h"



class Traveling_pixels : public Effect
{
    private:
        int curr_i;
        CHSV color;
        CHSV background_color;
        uint8_t cycle_range;
        uint8_t blur_radious;



    public:
        Traveling_pixels(CRGB* leds_arr, byte last_led_index, CHSV _color, CHSV _background_color, uint8_t cycle_range, uint8_t _blur_range, int _transition_time);
        ~Traveling_pixels();
        void do_step() override;
};


#endif