#include <Arduino.h>
#include <FastLED.h>

#include "helpers.h"
#include "effects/effect.h"
#include "config.h"
#include "effects/pulsating_colors.h"
#include "structures.h"



Pulsating_colors::Pulsating_colors(CRGB *leds_arr, byte last_led_index, transition_function _bright_function, int _transition_time)
    : Effect(leds_arr, last_led_index, _transition_time)
{
    color = CHSV(random8(), random8(), 0);
    
    bright_funct = _bright_function;
    not_changed = true;
}

void Pulsating_colors::do_step()
{
    uint8_t step = millis()*256/transition_time; // one step is made every "transmition_time/256" miliseconds andthere are 256 steps


    uint8_t brightness_tmp;

    switch (bright_funct)
    {
    case TRIWAVE:
        brightness_tmp = triwave8(step);
        break;
    case CUBICWAVE:
        brightness_tmp = cubicwave8(step);
        break;
    case QUADWAVE:
        brightness_tmp = quadwave8(step);
        break;
    default:
        break;
    } 


    color.value = map8(brightness_tmp, 0, MAX_BRIGHTNESS);


    fill_solid(leds, NUM_LEDS, color);

    if (brightness_tmp == 0)
    {
        not_changed = false;
    
        color.hue = random(256);
        color.saturation = random(0, 255);
    }
    


    FastLED.show();
}


Pulsating_colors::~Pulsating_colors() {}