#include <Arduino.h>
#include "helpers.h"
#include "structures.h"

#define INPUT_SIZE 200

bool check_for_orders(Order& cmd, char *val, uint8_t& place)
{
    if (Serial.available() > 0)
    {
        char input[INPUT_SIZE + 1];

        // Read input from Serial until ; what means command has ended
        byte size = Serial.readBytesUntil(';', input, INPUT_SIZE);
        input[size] = 0; // Add null terminator

        Serial.println(input);

        // Check if command is not empty
        if (input != 0)
        {
            // syntax is "order:pattern_place:value"
            cmd = static_cast<Order>(atoi(strtok(input, ":"))); // Get order numer and convert to enum
            place = atoi(strtok(NULL, ":")); // Get place number from input (only 0 or 1 is allowed)
            char *value = strtok(NULL, ":"); // Get value from second part of string
            
            if (value == 0) // If value is empty then syntax is invalid
            {
                Serial.println("Err: Invalid Syntax");
                return false;
            }

            // Otherwise copy order name and value to c-strings from main function
            strcpy(val, value);

            return true;
        }
        else // Probably never gonna happen
        {
            Serial.println("Err: Order empty");
            return false;
        }
    }
    return false;
}