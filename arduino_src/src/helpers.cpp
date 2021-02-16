#include "helpers.h"

#include <FastLED.h>


bool are_strings_the_same(char input[], char check[])
{
    int i;
    for(i=0; input[i]!='\0' || check[i]!='\0'; i++) {
        if(input[i] != check[i]) {
            return false;
        }
    }
    return true;
}


void fill_leds_with_symetric_gradient(CRGB* leds, uint8_t last_led, CHSV start_end, CHSV center, uint8_t index, uint8_t blur_radious)
{
    fill_gradient(leds, max(index - blur_radious, 0), start_end, min(index, last_led-1), center);
    fill_gradient(leds, max(index, 0), center, min(index + blur_radious, last_led-1), start_end);
}


uint8_t random_num8(uint8_t start, uint8_t end)
{
    int a, b;
    do
    {
        a = random(256);
        b = random8(256);
    } while (a <= b);

    return b;
}