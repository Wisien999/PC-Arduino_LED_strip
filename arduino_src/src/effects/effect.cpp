#include "config.h"
#include "effects/effect.h"

#include <FastLED.h>
#include <Arduino.h>



Effect::Effect(CRGB* leds_arr, byte last_led_index, int _transition_time)
{
    if (last_led_index >= 0 && last_led_index < NUM_LEDS)
        last_led = last_led_index;
    else
        last_led = NUM_LEDS;

    leds = leds_arr;

    if (_transition_time > 0)
        transition_time = _transition_time;
    else
        transition_time = DEFAULT_TRANSITION_TIME;

    last_time = millis();

}


void Effect::do_step()
{
}


Effect::~Effect() {}
