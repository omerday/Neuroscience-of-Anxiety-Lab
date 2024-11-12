#include "constants.h"


size_t get_safety_ms(float temp)
{
  for (int i = 0; i < NUM_SAFETY_LIMITS; i++)
  {
    size_t safety_temp = SAFETY_LIMITS_TEMP[i];
    size_t temp_ms = SAFETY_LIMITS_MS[i];
    if (temp >= safety_temp)
    {
        return temp_ms;
    }
  }

  // Outbounds all safe temperatures
  return 0;
}

size_t get_safety_level(float temp)
{
  for (int i = 0; i < NUM_SAFETY_LIMITS; i++)
  {
    size_t safety_temp = SAFETY_LIMITS_TEMP[i];
    size_t temp_ms = SAFETY_LIMITS_MS[i];
    if (temp >= safety_temp)
    {
        return safety_temp;
    }
  }

  // Outbounds all safe temperatures
  return SAFETY_LIMITS_TEMP[NUM_SAFETY_LIMITS - 1];
}
