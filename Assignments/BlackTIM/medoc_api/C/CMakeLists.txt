cmake_minimum_required(VERSION 3.12)
project(PythonAPI LANGUAGES C)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(SOURCE_FILE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")

include_directories( "${CMAKE_CURRENT_SOURCE_DIR}/inc/" )
FILE(GLOB SOURCES
  "${SOURCE_FILE_DIR}/constants.c"
)

add_library(PythonAPI SHARED ${SOURCES})
