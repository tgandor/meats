/* - - - - - Copyright Notice - - - - - - - - - - - - 
     Copyright 1998 Forrest J. Cavalier III

   See http://www.mibsoftware.com/libmib/ for documentation and
   original copies of this software.

   This software shall be distributed with the implementation
   source code libmib/parse/astring.c, according to the
   libmib license terms therein.
*/
/**************************************************************/
#ifndef INC_LIBMIB_ASTRING_H
#define INC_LIBMIB_ASTRING_H
#define LIBMIB_BEFORE_DECL
#include "compat.h"

/* There are 4 methods of implementing ASPRINTF
 */
/* The best way is if there is a vsnprintf(), this includes
 * Solaris 2.6 (but not earlier), recent versions of Linux,
 * and WIN32
 */
#define ASTRING_USE_VSNPRINTF

/* If have SNPRINTF, we can use that.  The implementation to use
 * snprintf is a bit clumsy and convoluted, because we have to
 * parse the format string and break calls to snprintf into
 * little chunks.
#define ASTRING_USE_SNPRINTF   
*/

/* If don't have SNPRINTF, we can work with sprintf().  The printf
 * format string is parsed and the necessary space is predicted.
 * But in the unlikely event we fail to predict how much space is
 * going to get used, (because we have a different parse of the
 * string than the system used) the overrun is detected and we
 * have no choice but to exit because the buffer was corrupted.
 * 
#define ASTRING_USE_SPRINTF   
*/

/* Finally, if you don't want asprintf() at all
#define ASTRING_NOASPRINTF   
*/

#include <stdio.h> /* Declares the FILE * for afgets() */
#include <stdarg.h>

#ifdef __cplusplus
extern "C" {
#endif 
/**************************************************************/
/* There are just two simple points for creating and destroying astrings:
 *
 *   1. Always initialize an astring to 0 before the first use.
 *        char *ppasz = 0;
 *
 *   2. Always call astrfree() or free() to prevent memory leaks.
 *        astrfree(&ppasz);
 *
 */
/**************************************************************/

/**************************************************************/
/* astring "allocators".
 *
 * Allocators are functions which can change the size (and
 * potentially move the string, since they are implemented via
 * realloc()
 */
    /* Equivalents to strcpy() and strncpy() */
#ifndef LIBMIB_NOIMPL_astrcpy
    char LIBMIB_PTR *astrcpy(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pSrc);
#endif
#ifndef LIBMIB_NOIMPL_astrn0cpy
    char LIBMIB_PTR *astrn0cpy(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pSrc,int n);
	/* NOTE: astrn0cpy Always stores the ending \0 */
#endif
#ifndef LIBMIB_NOIMPL_astrcat
    /* Equivalents to strcat() and strncat() */
    char LIBMIB_PTR *astrcat(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pszSrc);
#endif
#ifndef LIBMIB_NOIMPL_astrn0cat
    char LIBMIB_PTR *astrn0cat(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pSrc,int n);
	/* NOTE: astrn0cat Always stores the ending \0 */
#endif

#ifndef LIBMIB_NOIMPL_avsprintf
    /* "Smart" replacements for libc functions */
#ifndef ASTRING_NOASPRINTF
    int avsprintf(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char *format,va_list ap);
    int asprintf(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char *format,...);
#endif
#endif

#ifndef LIBMIB_NOIMPL_afgets
    char LIBMIB_PTR*afgets(char LIBMIB_PTR*LIBMIB_PTR*ppasz,FILE *f);
#endif
#ifndef LIBMIB_NOIMPL_afgettoch
    int afgettoch(char LIBMIB_PTR*LIBMIB_PTR*ppasz,FILE *f,char chStop);
#endif

/**************************************************************/

/**************************************************************/
/* astring "operations"
 * Complete documentation is at http://www.mibsoftware.com/libmib,
 * but summaries are provided here.
 * 
 * Since an astring is simply a char *, most any non-volatile string
 * operations can be used, including the string functions of libc,
 * such as strlen(), strchr(), etc.
 *
 * IMPORTANT: don't use "stale" pointers after calling an astring
 *   function, which can move the buffer.  This is such a common
 *   source of programmer error that there is an implementation
 *   profile flag for debugging, called ASTRING_DOMOVE.  Use it.
 *
 */

/**************************************************************/
/* "Advanced" astring implementation access and features */
    void astrfree(char LIBMIB_PTR*LIBMIB_PTR*ppasz); 
	/* Use this whenever possible to free an astring,
	   which allows better optimization than just a
	   call to free()
	 */

    char LIBMIB_PTR *astrensure(char LIBMIB_PTR*LIBMIB_PTR*ppasz,int len); 
	/* Ensures that *ppsz points to len+1 bytes */

	/* astrensure is used internally, but it is useful to
	   "reserve" an amount for external use.  Note that any 
	   call to an astring function will cancel previous
	   "reservations" made with astrensure.  (Storage is then
	   ensured only up to and including the first \0.)
	 */
    
    void astrstatic(char LIBMIB_PTR*LIBMIB_PTR*ppasz); 
	/* Minimize storage for the astring */

	/* The implementation of astrings "overallocates" to prevent
	   unnecessary copying of "active" strings.  This is fine for
	   most astrings, which are function "auto" variables.
	   
	   If a large number of astrings are persistent ("long-lived")
	   then astrstatic() will realloc for exactly the size needed
	   to store the string, and there is less memory waste.
	 */

    void astrprofile(int cWorking,int cbMin,int bvFlags); 
	/* Normally not used. See other documentation for this
	   advanced function which changes the implementation
	   strategies
	 */
#define ASTRING_BALLAST 1
#define ASTRING_DOMOVE 2

#ifdef _DEBUG
#define defaultFLAGS ASTRING_DOMOVE
#else
#define defaultFLAGS 0
#endif


#ifdef __cplusplus
};
#endif 

#undef LIBMIB_BEFORE_DECL
//#include <libmib/local.h>
#endif /* Recursive-include check */
