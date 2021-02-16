#include <Arduino.h>
#include <FastLED.h>

#include "effects/effect.h"
#include "config.h"
#include "effects/pulsating_color.h"
#include "structures.h"



Pulsating_color::Pulsating_color(CRGB *leds_arr, byte last_led_index, CHSV _color, transition_function _bright_function, int _transition_time)
    : Effect(leds_arr, last_led_index, _transition_time)
{
    color = _color;
    
    bright_funct = _bright_function;
}

void Pulsating_color::do_step()
{
    uint8_t step = millis()*256/transition_time; // one step is made every "transmition_time/256" miliseconds andthere are 256 steps


    uint8_t brightness_tmp;

    switch (bright_funct) // Calculate the current brightness using function of choice
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


    color.value = map8(brightness_tmp, 0, MAX_BRIGHTNESS); // Map brightness to set brightness range


    fill_solid(leds, NUM_LEDS, color);
}


Pulsating_color::~Pulsating_color() {}