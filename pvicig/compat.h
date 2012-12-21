/* libmib/compat.h version 1998.07.20
    Summary/Purpose: define macros used to promote cross-platform
                     compatibility.

   - - - - - - - - - - - - Copyright Notice - - - - - - - - - - - - 
     Copyright 1998 Forrest J. Cavalier III

   See http://www.mibsoftware.com/libmib/ for documentation and
   original copies of this software.

   This software is provided by Forrest J. Cavalier III, d-b-a
   Mib Software, under the following terms and conditions, which
   are believed to meet the open-source definition, version 1.0
   at http://www.opensource.org

   Contact Mib Software (mibsoft@mibsoftware.com) to discuss custom
   and enhanced versions of this and other software, other licensing
   terms, and support. We would appreciate that you notify us of defect
   discoveries and enhancements so that others can benefit from work
   on open-source software.

  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

   Permission is hereby granted, free of charge, to any person obtaining
   a copy of this software (the "Software"), to deal in the Software
   without restriction, including without limitation the rights to use,
   copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software
   is furnished to do so, subject to the following conditions:

   1. The above copyright notice and this permission notice shall
      be included in the source code of all copies or substantial
      portions of the Software.

   2. Modifications to the source code may be created and the software
      built from modified source code may be distributed.  Unless other
      licensing agreements are made in writing,
         a) Source code modifications shall be distributed only as
	    "patch files." 
      and
         b) When source code of the Software is distributed, it shall
	    be in its "pristine", unmodified form.
      and
         c) Modified works that are distributed shall be named differently
            than the original.

      Contact the author if you wish to arrange other terms.

   3. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
      EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
      MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
      IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
      CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
      TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
      SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
#ifndef _INC_LIBMIB_COMPAT_H
#define _INC_LIBMIB_COMPAT_H
#ifdef WIN32
#if _MSC_VER == 800
#define LIBMIB_COMPAT_PROFILE 1 /* short=16 int=16 long=32 */
#endif
#if _MSC_VER == 1000
/* MSVC 4.0 */
#define LIBMIB_COMPAT_PROFILE 2 /* short=16 int=32 long=32*/
#endif
typedef long offset_t;
#else
#ifdef linux
#include <sys/bitypes.h>
#define LIBMIB_COMPAT_PROFILE 0
typedef u_int32_t uint32_t;
typedef u_int16_t uint16_t;
typedef off_t offset_t;

#endif
#ifdef __FreeBSD__
#include <sys/types.h>
#define LIBMIB_COMPAT_PROFILE 0
typedef u_int32_t uint32_t;
typedef u_int16_t uint16_t;
typedef off_t offset_t;
#endif

#ifdef sun
#define LIBMIB_COMPAT_PROFILE 2
#if 0
/* DEBUG: This doesn't work on 5.5.1 */
#include <sys/inttypes.h>
#define LIBMIB_COMPAT_PROFILE 0
#endif
#endif

#endif
/**************************************************************/
#if LIBMIB_COMPAT_PROFILE == 0
/* Already defined */
#else
#if LIBMIB_COMPAT_PROFILE == 1
/* O/S and compiler profile 1: WIN16 and other systems
 * where short=16 bits, int=16 bits, long=32 bits
 */
typedef unsigned long uint32_t;
typedef long int32_t;

typedef unsigned short uint16_t;
typedef short int16_t;

/* C99 types */
typedef char int_least8_t;
typedef int int_least16_t
typedef long int_least32_t
//typedef char int_least64_t
typedef long intmax_t;

typedef int int_fast8_t;
typedef int int_fast16_t
typedef long int_fast32_t
//typedef char int_fast64_t

typedef unsigned char uint_least8_t;
typedef unsigned int uint_least16_t
typedef unsigned long uint_least32_t
//typedef uint_least64_t
typedef unsigned long uintmax_t;

typedef unsigned int uint_fast8_t;
typedef unsigned int uint_fast16_t
typedef unsigned long uint_fast32_t
//typedef uint_fast64_t

#else
/**************************************************************/
#if LIBMIB_COMPAT_PROFILE == 2
/* O/S and compiler profile 2: WIN32 and other systems
 * where short=16 bits, int=32 bits, long=32 bits
 */
typedef unsigned long uint32_t;
typedef long int32_t;

typedef unsigned short uint16_t;
typedef short int16_t;

/* C99 types */
typedef char int_least8_t;
typedef short int_least16_t;
typedef long int_least32_t;
//typedef char int_least64_t;
typedef long intmax_t;

typedef int int_fast8_t;
typedef short int_fast16_t;
typedef long int_fast32_t;
//typedef char int_fast64_t;

typedef unsigned char uint_least8_t;
typedef unsigned short uint_least16_t;
typedef unsigned long uint_least32_t;
//typedef uint_least64_t
typedef unsigned long uintmax_t;

typedef unsigned int uint_fast8_t;
typedef unsigned short uint_fast16_t;
typedef unsigned long uint_fast32_t;
//typedef uint_fast64_t
#else
/**************************************************************/
	#error "Unknown compiler.  Need profile/defs for UINT32, UINT16, etc."
/**************************************************************/
#endif
#endif
#endif
/**************************************************************/
#ifndef BOOL
#ifndef WIN32
#define BOOL int
#else
typedef int BOOL;
#endif

#define FALSE   0
#define TRUE    1

#endif
/**************************************************************/


/**************************************************************/
#if !defined(WIN32)&&!defined(_WINDOWS)&&!defined(_MSDOS) /* was WINDOWS MSDOS 5-4-2001 */
#define strnicmp strncasecmp
#endif

#ifndef LIBMIB_ALIGN
#define LIBMIB_ALIGN 0
#endif
/**************************************************************/
#if defined(WIN32)
#define MIB_LIB97
#define MIB_FLATMEM
#else
#if !defined(_WINDOWS)&&!defined(_MSDOS) /* was WINDOWS MSDOS 5-4-2001 */
#define MIB_FLATMEM
#endif
#endif

/**************************************************************/



/**************************************************************/
/* Memory model compatibility */

#if defined(MIB_FLATMEM)
/* "Flat" memory model has no need for pointer types */
#define LIBMIB_FAR
#define LIBMIB_HUGE
#define LIBMIB_NEAR

#define halloc(a,b) malloc((a)*(b))
#define hfree free
#define hmemcpy memcpy
#define hrealloc realloc

#define _ffree free
#define _fmalloc malloc
#define _frealloc realloc
#define _fheapchk _heapchk

#define _fstrlen strlen
#define _fstrcpy strcpy
#define _fstrcat strcat
#define _fstrcspn strcspn
#define _fstrchr strchr
#define _fstrstr strstr
#define _fstrcmp strcmp
#define _fstrlwr strlwr
#define _fstricmp _stricmp	/* Not ANSI */
#define _fstrnicmp _strnicmp	/* Not ANSI */
#define _fstrncpy strncpy
#define _fstrrchr strrchr
#define _fstrncmp strncmp

#define _fmemcpy memcpy
#define _fmemset memset
#define _fmemcmp memcmp
#define _fmemchr memchr
#define _fmemmove memmove

#define MIB_PASCAL

#ifdef WIN32
#define LIBMIB_EXPORT __declspec( dllexport )
#else
#define LIBMIB_EXPORT
#endif


#else
/* Non-flat ("segmented") memory model needs pointer types */
#define LIBMIB_FAR far
#define LIBMIB_HUGE huge
#define LIBMIB_NEAR near
#define LIBMIB_PASCAL _pascal	/* Pascal calling conventions */
#define LIBMIB_EXPORT _export  /* Can be called from outside linked unit */
#endif

/* Declarations of pointers are prefixed using macros, so that
   the memory model for pointers can be controlled.  In a flat
   memory model, this is 0.

   const is user through a macro LIBMIB_CONST.

    Example           Declared as
    const char *p;    LIBMIB_CONST char LIBMIB_PTR *p;

    long *p	      long MIB_FAR *p

*/
#ifndef LIBMIB_PTR
#define LIBMIB_PTR LIBMIB_FAR
#endif
/**************************************************************/



/**************************************************************/
#define LIBMIB_PRIVATE static
#define LIBMIB_CONST const
typedef long LIBMIB_ERRNO;

#ifndef charError
#define charError char
#endif


/**************************************************************/
#ifdef WIN32
#define LIBMIB_O_BINARY O_BINARY
#else
#define LIBMIB_O_BINARY 0
#endif


/**************************************************************/
#if defined(DEBUG)||defined(_DEBUG)
#define LIBMIB_DEBUG
#endif


#endif

