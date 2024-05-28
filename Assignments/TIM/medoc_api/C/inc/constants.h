#ifndef _PYTHON_API_INC_CONSTANTS
#define _PYTHON_API_INC_CONSTANTS
#include "stddef.h"

#define _NUM_SAFETY_LIMITS 10
const size_t NUM_SAFETY_LIMITS = _NUM_SAFETY_LIMITS;
const float SAFETY_LIMITS_TEMP[_NUM_SAFETY_LIMITS] = {
  56.f,
  55.f,
  52.f,
  51.f,
  50.f,
  49.f,
  47.f,
  6.f,
  0.f,
  -10.f
};
const size_t SAFETY_LIMITS_MS[_NUM_SAFETY_LIMITS] = {
  0,
  50,
  400,
  1000,
  5000,
  10000,
  60000,
  300000,
  300000,
  300000
};

size_t get_safety_ms(float temp);
size_t get_safety_level(float temp);

#endif
