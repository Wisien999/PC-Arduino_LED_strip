#include <Arduino.h>
#include <FastLED.h>

#include "effects/effect.h"
#include "config.h"
#include "effects/linear_colors2.h"



Linear_colors2::Linear_colors2(CRGB *leds_arr, byte last_led_index, bool _fix_colors, int _transition_time)
    : Effect(leds_arr, last_led_index, _transition_time)
{
    curr_i = 0;
    hue = 0;
    fix_colors = _fix_colors;
}


void Linear_colors2::do_step()
{
    // 1/3 of 255 (hue range is 0-255) is ~= 85. 85/90 is 0.9(4). We call it 0.94 and have 0.94/(transition_time/(1000*60)) beats per minute in range from 0 to 90
    uint8_t hue_diff = map8(beat8(0.94*60000/transition_time, last_time), 0, 90);


    leds[curr_i].setHSV(hue + hue_diff, 255, 90); // Set current LED color to current_hue


    if (hue_diff > 85) // If color was changed more than 1/3 of hue range
    {
        last_time = millis();
        curr_i += 1; // Go to next LED
        if (curr_i == last_led) // If it was the last LED
        {
            curr_i = START_LED; // Go to first LED
            hue += hue_diff; // change base hue

            if (fix_colors && hue < hue_diff) // After some cycles colors are no longer "pure". This exists to fix it
                hue = 0; // Set color to pure red
        }

    }
}


Linear_colors2::~Linear_colors2() {}
