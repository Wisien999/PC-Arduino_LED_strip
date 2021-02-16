#include <Arduino.h>
#include <FastLED.h>

#include "helpers.h"
#include "effects/effect.h"
#include "config.h"
#include "effects/traveling_pixels.h"


Traveling_pixels::Traveling_pixels(CRGB *leds_arr, byte last_led_index, CHSV _color, CHSV _background_color,
    uint8_t _cycle_range, uint8_t _blur_radious, int _transition_time)
    : Effect(leds_arr, last_led_index, _transition_time)
{
    color = _color;
    background_color = _background_color;
    cycle_range = min(_cycle_range, NUM_LEDS);
    curr_i = 0;
    
    blur_radious = _blur_radious;
}


void Traveling_pixels::do_step()
{

    if (millis() < last_time + transition_time)
        return;

    last_time = millis();


    fill_solid(leds, NUM_LEDS, background_color);

    for (uint8_t i = curr_i; i < NUM_LEDS; i += cycle_range)
    {
        fill_leds_with_symetric_gradient(leds, last_led, background_color, color, i, blur_radious);
    }


    ++curr_i;

    
    if (curr_i >= cycle_range)
    {
        curr_i = 0;        
    }
}


Traveling_pixels::~Traveling_pixels() {};