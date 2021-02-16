#include "config.h"
#include "structures.h"
#include "effects/effect.h"

#include <stdlib.h>
#include <Arduino.h>
#include <FastLED.h>

// int parse_linear_colors(char* arg, int &last_led, int &transition_time);
// int parse_pulsating_color(char* arg, int &last_led, int &transition_time, CHSV &color, transition_function &bright_function);


bool do_order(Order order, char* arg, Effect*& effect, CRGB* leds);
