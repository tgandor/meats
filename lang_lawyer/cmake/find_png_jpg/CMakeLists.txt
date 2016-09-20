PROJECT(test_for_zlib_jpeg_png C)

# I use a minimum of 3.0 flat for features anyway, though nothing here
# should require anything this high
CMAKE_MINIMUM_REQUIRED(VERSION 3.0 FATAL_ERROR)

find_package(ZLIB QUIET)
find_package(JPEG QUIET)
find_package(PNG QUIET)

if (ZLIB_FOUND)
    message ("Cool: ZLIB found - Includes: ${ZLIB_INCLUDE_DIR} Libs: ${ZLIB_LIBRARIES}")
else (ZLIB_FOUND)
    message ("WARNING: Could not find ZLIB")
endif (ZLIB_FOUND)

if (JPEG_FOUND)
    message ("Cool: JPEG found - Includes: ${JPEG_INCLUDE_DIR} Libs: ${JPEG_LIBRARIES}")
else (JPEG_FOUND)
    message ("WARNING: Could not find JPEG")
endif (JPEG_FOUND)

if (PNG_FOUND)
    message ("Cool: PNG found - Includes: ${PNG_INCLUDE_DIR} Libs: ${PNG_LIBRARIES}")
else (PNG_FOUND)
    message ("WARNING: Could not find PNG")
endif (PNG_FOUND)

# courtesy of: http://stackoverflow.com/questions/9298278/cmake-print-out-all-accessible-variables-in-a-script#9328525
if (PRINT_VARS)
message("Dumping variables:")

get_cmake_property(_variableNames VARIABLES)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()
endif(PRINT_VARS)
