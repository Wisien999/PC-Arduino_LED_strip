#include <Arduino.h>
#include <FastLED.h>

#include "config.h"
#include "data_transfer.h"
#include "helpers.h"
#include "effects/all_effects.h"
#include "orders.h"
#include "structures.h"

CRGB leds[NUM_LEDS];
CRGB pattern[2][NUM_LEDS];

bool active[2];

uint8_t blend_ratio=0;

Effect* program[2];


void setup()
{
  pinMode(UNUSED_ANALOG_PIN, INPUT); // prepare for random seed generation
  randomSeed(analogRead(UNUSED_ANALOG_PIN)); // randomize random()

  Serial.begin(9600);

  FastLED.addLeds<LED_TYPE, LED_PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);



}


void loop()
{
  char *val = "val\0";
  Order order;
  uint8_t place;
  if (check_for_orders(order, val, place))
  {
    if (order == Order::SET_BLENDING_RATIO)
    {
      blend_ratio = place; // in this case place is new blending ratio
    }
    else if (place > 1)
    {
      Serial.println("Err: I do not have that much space!");
    }
    else if (order == Order::STOP)
    {
      delete program[place];
      fill_solid(pattern[place], NUM_LEDS, CHSV(0, 0, 0));
      active[place] = false;
    }
    else
    {
      fill_solid(pattern[place], NUM_LEDS, CHSV(0, 0, 0));
      do_order(order, val, program[place], pattern[place]);
      active[place] = true;
    }
  }

  if (active[0]) program[0]->do_step();
  if (active[1]) program[1]->do_step();


  blend(pattern[0], pattern[1], leds, NUM_LEDS, blend_ratio);
  FastLED.show();
  // if (millis() %10 == 0)
  // Serial.println(leds[0].b);
}

