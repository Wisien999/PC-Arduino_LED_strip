#include "config.h"
#include "orders.h"
#include "structures.h"
#include "helpers.h"
#include "effects/all_effects.h"

#include <stdlib.h>
#include <Arduino.h>
#include <FastLED.h>



bool get_last_led_and_transition_time(char* arg, uint8_t &last_led, int &transition_time)
{
    last_led = atoi(strtok(arg, ARGUMENTS_SEPARATOR));
    transition_time = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));

    return true;    
}



bool parse_fill_solid(char* arg, uint8_t &last_led, CHSV &color)
{
    last_led = atoi(strtok(arg, ARGUMENTS_SEPARATOR));


    uint8_t hue = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    uint8_t saturation = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    uint8_t value = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));

    color = CHSV(hue, saturation, value);


    return true;
}



// bool parse_fill_gradient(char* arg, uint8_t &last_led, uint8_t &brightness, TBlendType &blend_type, CHSVPalette16 &palette)
bool parse_fill_gradient(char* arg, uint8_t &last_led, uint8_t &brightness, CHSV colors[16])
{
    // (there will be 16 colors send ALWAYS)
    // last_led,brightness,blend_type,color1,color2,...,color16

    last_led = atoi(strtok(arg, ARGUMENTS_SEPARATOR));
    brightness = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));


    // palette = CHSVPalette16();

    uint8_t hue, saturation, value;
    for(auto i = 0; i < 16; ++i)
    {
        hue = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
        saturation = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
        value = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    
        // palette[i] = CHSV(hue, saturation, value);
        colors[i] = CHSV(hue, saturation, value);
    }


    return true;
} 



bool parse_linear_colors(char* arg, uint8_t &last_led, int &transition_time, bool &fix_colors)
{
    // order is last_led,transition_time,fix_colors(has meaning only in case transition_time > 300)
    get_last_led_and_transition_time(arg, last_led, transition_time);

    fix_colors = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));


    return true;
}



bool parse_pulsating_color(char* arg, uint8_t &last_led, int &transition_time, CHSV &color, transition_function &bright_function)
{ 
    // last_led,transition_time,color,brightness_control_function
    get_last_led_and_transition_time(arg, last_led, transition_time);

    uint8_t hue = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    uint8_t saturation = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    uint8_t brightness = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));

    color = CHSV(hue, saturation, brightness);

    bright_function = static_cast<transition_function>(atoi(strtok(NULL, ARGUMENTS_SEPARATOR)));


    return true;
}



bool parse_pulsating_colors(char* arg, uint8_t &last_led, int &transition_time, transition_function &bright_function)
{
     
    get_last_led_and_transition_time(arg, last_led, transition_time);

    bright_function = static_cast<transition_function>(atoi(strtok(NULL, ARGUMENTS_SEPARATOR)));
    Serial.println(bright_function);

    return true;
}



bool parse_traveling_pixels(char* arg, uint8_t &last_led, int &transition_time, uint8_t &cycle_range, uint8_t blur_radious, CHSV &color, CHSV &background_color)
{
    // last_led,transition_time,cycle_range,blur_radious,color,background_color
    get_last_led_and_transition_time(arg, last_led, transition_time);


    cycle_range = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));


    blur_radious = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));


    uint8_t hue = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    uint8_t saturation = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    uint8_t brightness = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));

    color = CHSV(hue, saturation, brightness);


    hue = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    saturation = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));
    brightness = atoi(strtok(NULL, ARGUMENTS_SEPARATOR));

    background_color = CHSV(hue, saturation, brightness);

    return true;
}



bool do_order(Order order, char* arg, Effect*& effect, CRGB* leds)
{
    uint8_t last_led;

    switch (order)
    {
    case Order::FILL_SOLID:
        {
            CHSV color;
            parse_fill_solid(arg, last_led, color);

            fill_solid(leds, last_led, color);
            
            return true;
        }
        break;
    case Order::FILL_GRADIENT:
        {
            CHSVPalette16 pattern; 
            uint8_t brightness;
            CHSV colors[16];


            parse_fill_gradient(arg, last_led, brightness, colors);

            // fill_palette((leds, last_led, 0, 15, pattern, brightness, TBlendType::LINEARBLEND);

            for (uint8_t i = 1; i < 16; ++i)
            {
                fill_gradient_HSV(leds, (i-1)*last_led/16, colors[i-1], i*last_led/16, colors[i], TGradientDirectionCode::SHORTEST_HUES);
            }
        }
        break;
    case Order::LINEAR_COLORS:
        {
            bool fix_colors;
            CHSV color;
            int transition_time;

            parse_linear_colors(arg, last_led, transition_time, fix_colors);
            
            if (transition_time < 300)
            {
                effect = new Linear_colors1(leds, last_led, transition_time);
            }
            else
            {
                effect = new Linear_colors2(leds, last_led, fix_colors, transition_time);
            }

            return true; 
        }
        break;
    case Order::PULSATING_COLOR:
        {
            transition_function brightness_function;
            CHSV color;
            int transition_time;


            parse_pulsating_color(arg, last_led, transition_time, color, brightness_function);        

            effect = new Pulsating_color(leds, last_led, color, brightness_function, transition_time);

            return true;
        }
        break;

    case Order::PULSATING_COLORS:
        {
            int transition_time;
            transition_function bright_function;


            parse_pulsating_colors(arg, last_led, transition_time, bright_function);

            effect = new Pulsating_colors(leds, last_led, bright_function, transition_time);


            return true;
        }

        break;
    case Order::TRAVELING_PIXELS:
        {
            int transition_time;
            uint8_t cycle_range, blur_radious;
            CHSV color;
            CHSV background_color;


            parse_traveling_pixels(arg, last_led, transition_time, cycle_range, blur_radious, color, background_color);
            
            effect = new Traveling_pixels(leds, last_led, color, background_color, cycle_range, blur_radious, transition_time);

            return true;
        }
        break;
    default:
        {
            return false; 
        }
        break;
    } 

    return 0;
}