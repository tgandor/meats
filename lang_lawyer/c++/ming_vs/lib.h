#ifndef LIB_H
#define LIB_H
#pragma once

#ifdef _MSC_VER
#define DLLFUNC __declspec(dllexport)
#else
#define DLLFUNC __attribute__ ((dllexport))
#endif

#ifdef __cplusplus
extern "C" {
#endif

    int DLLFUNC max_div(int n);

#ifdef __cplusplus
}
#endif

#endif
