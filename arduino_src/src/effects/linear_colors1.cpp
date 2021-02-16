#include "effects/effect.h"
#include "config.h"
#include "effects/linear_colors1.h"

#include <Arduino.h>
#include <FastLED.h>


Linear_colors1::Linear_colors1(CRGB* leds_arr, byte last_led_index, int _transition_time)
    :Effect(leds_arr, last_led_index, _transition_time)
{
    curr_i = 0;
    color = CRGB(MAX_BRIGHTNESS,0,0);
}


void Linear_colors1::do_step()
{
    // if (millis() - last_time < transition_time)
    if (millis() < last_time + transition_time) // if it is not the time yet
    {
        // do nothing
        return;
    }

    last_time = millis();

    leds[curr_i] = color;

    curr_i += 1;


    if (curr_i == NUM_LEDS)
    {
        curr_i = 0;
        if (color.b == MAX_BRIGHTNESS)
        {
            color.b = 0;
            color.r = MAX_BRIGHTNESS;
        }
        else if (color.r == MAX_BRIGHTNESS)
        {
            color.r = 0;
            color.g = MAX_BRIGHTNESS;
        }
        else if (color.g == MAX_BRIGHTNESS)
        {
            color.g = 0;
            color.b = MAX_BRIGHTNESS;
        }
    }

    // FastLED.show();
}


Linear_colors1::~Linear_colors1() {}

