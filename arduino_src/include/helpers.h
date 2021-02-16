#ifndef HELPERS_H
#define HELPERS_H

#include <FastLED.h>
; // XD


bool are_strings_the_same(char input[],char check[]); // Checks if 2 strings are equal (for some reason strcmp() does not work)

void fill_leds_with_symetric_gradient(CRGB* leds, uint8_t last_led, CHSV start_end, CHSV center, uint8_t index, uint8_t blur_radious);

uint8_t random_num8(uint8_t start, uint8_t end); // Generate random number from range 0-255 the greater number the more probable


#endif