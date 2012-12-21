/*  libmib/parse/astring.c version 1998.08.20 (from libmib )
   Summary/Purpose: allocated string functions
- - - - - - - - - - - - Copyright Notice - - - - - - - - - - - -
     Copyright 1999 Forrest J. Cavalier III

   WARNING: This software may have been modified.
   See http://www.mibsoftware.com/libmib/ for documentation and
   up-to-date original copies.  Arrangements for custom versions,
   support, and other licensing terms are made in writing.

   We would appreciate that you notify us of defect discoveries
   and enhancements so that others can benefit from improvements
   to this software.

  - - - - - - - - - - - - - License - - - - - - - - - - - - - - - - -
   Permission is hereby granted, to any person obtaining a copy of
   this software (the "Software"), to deal in the Software without
   restriction, including the rights to use, copy, modify, merge,
   publish, distribute, sublicense, and/or sell copies of the Software,
   subject to all the following conditions.

   1. The text beginning with the copyright notice above, and including
      the four clauses of this license shall be included in full and
      unmodified in all copies of the source files or portions thereof.

   2. You are not required to accept this License, since you have not
      signed it.  However, nothing else grants you permission to modify or
      distribute the Software or its derivative works.  These actions are
      prohibited by law if you do not accept this License.

   3. The author(s) grant you a non-exclusive right to use the author-
      given names and trademarks of the Software to publish and distribute
      only unmodified source files.  Your rights to deal in the Software
      under this license are subject to the condition that you do not
      use nor associate trademarks, names, or reputation of the author(s)
      with derivative works except within the source files.

   4. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
      EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
      MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
      IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
      CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
      TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
      SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
      
*/

/**************************************************************/



#ifdef LIBMIB
/* We are building as part of libmib.  Use libmib headers */
#define LIBMIB_IMPLEMENT
#include "compat.h"
#include <malloc.h>
#include <string.h>
#include <assert.h>
#include "astring.h"

#else
/* Here if not part of libmib, so header files are not available.
   define and predeclare items which would have been done in compat.h
   and astring.h under libmib builds
 */
#define LIBMIB_PRIVATE static

#include <malloc.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>

#define LIBMIB_PTR /* no memory model */
#define _frealloc realloc
#define _ffree free
#define _fstrlen strlen
#define _fstrcpy strcpy
#define _fmemcpy memcpy
#define _fmemchr memchr
#define _fstrncpy strncpy

/* These declare the provided interfaces.  Copy to whatever
 * header files you need
 */
    #ifndef LIBMIB_PTR
    #define LIBMIB_PTR /* no memory model */
    #endif

    char LIBMIB_PTR *astrensure(char LIBMIB_PTR * LIBMIB_PTR *ppsz,int cbMin);
    void astrfree(char LIBMIB_PTR * LIBMIB_PTR *ppsz);

    char LIBMIB_PTR *astrcpy(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pSrc);
    char LIBMIB_PTR *astrn0cpy(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pSrc,int n);
	/* NOTE: astrn0cpy Always stores the ending \0 */

    char LIBMIB_PTR *astrcat(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pszSrc);
    char LIBMIB_PTR *astrn0cat(char LIBMIB_PTR*LIBMIB_PTR*ppasz,const char LIBMIB_PTR*pSrc,int n);
	/* NOTE: astrn0cat Always stores the ending \0 */

    char LIBMIB_PTR *afgets(char LIBMIB_PTR*LIBMIB_PTR*ppasz,FILE *f);
    int afgettoch(char LIBMIB_PTR * LIBMIB_PTR *ppasz,FILE *f,char chStop);
/*********************************************/
#endif
/**************************************************************/

/**************************************************************/


#ifndef LIBMIB_ASTRING_OPTIMIZED
/* These are the simple, not optimized versions of the
   core routines astrensure, astrfree, astrstatic.  The
   optimized versions appear at the end
 */
/**************************************************************/
/**************************************************************/
char LIBMIB_PTR *astrensure(char LIBMIB_PTR * LIBMIB_PTR *ppsz,int cbMin)
{  /* This is the core routine for supporting allocated strings.
      Ensure that there is enough room to copy a string
      of strlen()==cbMin and a NUL terminator to *ppsz.

    */
    char LIBMIB_PTR *ret;

/* The simple version simply does a realloc. */
/* Overallocate, to reduce fragmentation, and efficient reallocs */
    cbMin = (cbMin / 240) * 256 + 240;

    cbMin++; /* Always reserve room for the NUL terminator, so
	        that callers don't always have to be
		adding 1 to strlen()s */
    ret = _frealloc(*ppsz,cbMin);
    if (!ret) {
	/* realloc couldn't satisfy the request.  The existing
	   string is freed to show there was an error. */
	astrfree(ppsz);
	return 0;
    }
    *ppsz = ret;
    return *ppsz;

} /* astrensure */
/**************************************************************/

/**************************************************************/
void astrstatic(char LIBMIB_PTR *LIBMIB_PTR *ppsz)
{ /* Similar to strensure, but always does a realloc to the exact
     string length
   */
    int cbMin;
    char LIBMIB_PTR *ret;

    if (!*ppsz) {
	return;
    }
    cbMin = _fstrlen(*ppsz)+1; /* Always reserve room for the Null terminator, so
	        that callers don't always have to be
		adding 1 to strlen()s */
    ret = _frealloc(*ppsz,cbMin); /* Always realloc */
    if (!ret) { /* Oh well, nothing lost */

    } else {
	*ppsz = ret;
    }
    return;
} /* astrstatic */
/**************************************************************/


/**************************************************************/
void astrfree(char LIBMIB_PTR * LIBMIB_PTR *ppsz)
{
    if (*ppsz) {
	_ffree(*ppsz);
	*ppsz = 0;
    }
    return;
} /* astrfree */
/**************************************************************/

#endif /* ndef OPTIMIZED */

/**************************************************************/
char LIBMIB_PTR *astrcpy(char LIBMIB_PTR * LIBMIB_PTR *ppsz,const char LIBMIB_PTR *src)
{ 
    int toalloc = _fstrlen(src);
    if (*ppsz) {
	**ppsz = '\0'; /* Signal astrensure that don't need to preserve */
    }
    astrensure(ppsz,toalloc);
    if (!*ppsz) {
	    return 0;
    }
    _fstrcpy(*ppsz,src);
    return *ppsz;
}
/**************************************************************/


/**************************************************************/
char LIBMIB_PTR *astrn0cpy(char LIBMIB_PTR * LIBMIB_PTR *ppsz,const char LIBMIB_PTR *pSrc,int len)
{ 
    int toalloc;
    char LIBMIB_PTR *pStop;
    
    if (*ppsz) {
	**ppsz = '\0'; /* Signal astrensure that don't need to preserve */
    }
    pStop = _fmemchr(pSrc,'\0',len);
    if (pStop) {
       toalloc = pStop - pSrc;
    } else {
       toalloc = len;
    }
    if (len < toalloc) {
        toalloc = len;
    }

    astrensure(ppsz,toalloc);
    if (!*ppsz) {
	return 0;
    }
    
    _fmemcpy(*ppsz,pSrc,len); /* Don't use strncpy, which zero fills. */
    (*ppsz)[len] = '\0';
    return *ppsz;
} /* astrn0cpy */
/**************************************************************/


/**************************************************************/
char LIBMIB_PTR *astrcat(char LIBMIB_PTR * LIBMIB_PTR *ppsz,const char LIBMIB_PTR *src)
{
    int toalloc;
    int len = 0;
    toalloc = _fstrlen(src);

    if (*ppsz) {
	len = _fstrlen(*ppsz);
	toalloc += len;
    }
    astrensure(ppsz,toalloc);
    if (!*ppsz) {
	return 0;
    }
    _fstrcpy(*ppsz+len,src);
    return *ppsz;
} /* astrcat */
/**************************************************************/


/**************************************************************/
char LIBMIB_PTR *astrn0cat(char LIBMIB_PTR * LIBMIB_PTR *ppsz,const char LIBMIB_PTR *pSrc,int n)
{ 
    char LIBMIB_PTR *pStop;
    int toalloc;
    int len = 0;
    if (n < 0) {
	assert(0&&"astrn0cat called with n < 0");
	return *ppsz;
    }
    if (n == 0) { /* 3-Feb-99 */
	return *ppsz;
    }
    pStop = _fmemchr(pSrc,'\0',n);
    if (pStop) {
       n = pStop - pSrc;
    }

    toalloc = n;

    if (*ppsz) {
	len = _fstrlen(*ppsz);
        toalloc += len;
    }

    astrensure(ppsz,toalloc);
    if (!*ppsz) {
	return 0;		
    }
    _fmemcpy(*ppsz+len,pSrc,n); /* Don't use strncpy, which zero fills. */
    (*ppsz)[len+n] = '\0';
    return *ppsz;
} /* astrn0cat */
/**************************************************************/


/**************************************************************/
char LIBMIB_PTR *afgets(char LIBMIB_PTR * LIBMIB_PTR *ppasz,FILE *f)
{
/* This also shows the proper use of an index, instead of
   a separate pointer which can go stale.
 */
    char ch;
    int room = 0;
    int ind = 0;

    while(!feof(f)) {
	if (ind >= room-1) {
	    room += 256;
	    if (!astrensure(ppasz,room)) {
		return 0; /* failed */
	    }
	}
	ch = fgetc(f);
	if ((ch == EOF) && feof(f)) {
	    break;
	}
	(*ppasz)[ind++] = ch;
	(*ppasz)[ind] = '\0';
	if (!ch || (ch == '\n')) {
	    return *ppasz;
	}
    }	
    if (!ind) { /* Nothing */
	astrfree(ppasz);
	return 0;
    }
    return *ppasz;
} /* afgets */
/**************************************************************/


/**************************************************************/
int afgettoch(char LIBMIB_PTR * LIBMIB_PTR *ppasz,FILE *f,char chStop)
{ /* Similar to afgets, but returns at eof, or when ch is
     obtained.  Returns number of characters.

   */
    char ch;
    int room = 0;
    int ind = 0;

    while(!feof(f)) {
	if (ind >= room-1) {
	    room += 256;
	    if (!astrensure(ppasz,room)) {
		return 0; /* failed */
	    }
	}
	ch = fgetc(f);
	if ((ch == EOF) && feof(f)) {
	    break;
	}
	(*ppasz)[ind++] = ch;
	(*ppasz)[ind] = '\0';
	if (ch == chStop) {
	    return ind;
	}
    }	
    if (!ind) { /* Nothing */
	astrfree(ppasz);
	return 0;
    }
    return ind;
} /* afgettoch */
/**************************************************************/


#ifdef LIBMIB_ASTRING_OPTIMIZED
/**************************************************************/
/* The implementation profile.  Use astrprofile() to change */
    LIBMIB_PRIVATE struct {
	int cbMin;  /* Minimum first allocation. Shorter strings are
		       placed in longer buffers to prevent copies
		       during realloc() when the buffer changes size.
		     */
	int cWorking; /* Number of "working strings" that are tracked.
		         Allows some optimization of storage and
			 reallocs()
		       */
	int bvFLAGS;  /* Implementation strategy, etc */
    } _profile = {

#ifdef WIN32
        1024,10,defaultFLAGS /* win32 default profile does not include ballast, since
	         the _expand() function call is available.
	       */
#else
	1024,10,defaultFLAGS|ASTRING_BALLAST /* Allocate "ballast" */
#endif
};
#endif
/**************************************************************/



#ifdef LIBMIB_ASTRING_OPTIMIZED

/**************************************************************/
void astrprofile(int cWorking,int cbMin,int bvFLAGS)
{
if (cbMin < 1) {
    cbMin = 1;
}
if (cWorking < 10) {
    cWorking = 10;
}
_profile.cbMin = cbMin;
_profile.cWorking = cWorking;
_profile.bvFLAGS = bvFLAGS;
} /* astrprofile */
/**************************************************************/

/**************************************************************/
/* Table of recently used astrings.  Tracking recently used strings
 * allows us to mark some strings as "active" and manage them a little
 * differently to prevent realloc() copies when the length changes.
 *
 * These are for internal/implementation use only.
 */
LIBMIB_PRIVATE struct astr_s {
    char LIBMIB_PTR *p;	/* Pointer to string */
    int cbAlloc; /* number of bytes allocated, with possible room for expansion */
    int pubMin; /* number of bytes that the caller thinks we allocated */
    char LIBMIB_PTR *pBallast; /* Post-allocated, helps with some malloc() implementations */
    int Age;
} LIBMIB_PTR *ppastr;

LIBMIB_PRIVATE struct astr_s LIBMIB_PTR *_Lookup(char LIBMIB_PTR *psz)
{
    struct astr_s LIBMIB_PTR *pFound = 0;
    int ind;
    if (!ppastr) {
	return 0;
    }
    ind = 0;
    while(ind < _profile.cWorking) {
	if (ppastr[ind].p) {
	    if (ppastr[ind].p == psz) {
		ppastr[ind].Age = 0;
		pFound = &ppastr[ind];
	    } else {
		ppastr[ind].Age += 1;
	    }
	}
	ind++;
    }
    return pFound;
} /* _Lookup */

LIBMIB_PRIVATE struct astr_s LIBMIB_PTR *_Insert(void LIBMIB_PTR *pBefore,void LIBMIB_PTR *p,int cbAlloc,int pubMin)
{ /* Need to choose which one gets booted.  We do a shrink, if
     the memory sytem supports it.  (currently only WIN32)
  */
    struct astr_s LIBMIB_PTR *pOldest = 0L;
    int ind;
    assert(cbAlloc >= pubMin);

    if (!ppastr) {
	ppastr = _fmalloc(_profile.cWorking * sizeof(struct astr_s));
	if (!ppastr) {
	    return 0;
	}
	_fmemset(ppastr,0,_profile.cWorking * sizeof(struct astr_s));
    }
    if (pBefore) {
	pOldest = pBefore;
    } else {
	ind = 0;
	while(ind < _profile.cWorking) {
	    if (!ppastr[ind].p) {
		pOldest = &ppastr[ind];
		break;
	    }
	    if (!pOldest || (ppastr[ind].Age > pOldest->Age)) {
		pOldest = &ppastr[ind];
	    }
	    ind++;
	}
	if (pOldest->p) {
	    if (pOldest->pBallast) {
		_ffree(pOldest->pBallast);
		pOldest->pBallast = 0;
	    }
#ifdef WIN32
	    if (!_profile.bvFLAGS & ASTRING_BALLAST) {
		_expand(pOldest->p,pOldest->pubMin); /* Shrink it, if we can */
	    }
#endif
	}
    }

    /* And replace with current */
    pOldest->p = p;
    pOldest->cbAlloc = cbAlloc;
    pOldest->pubMin = pubMin;
    pOldest->Age = 0;

    return pOldest;
} /* _Insert */
/**************************************************************/

LIBMIB_PRIVATE char LIBMIB_PTR *astrensure(char LIBMIB_PTR * LIBMIB_PTR *ppsz,int cbMin)
{
    struct astr_s LIBMIB_PTR *pCurrent;
    int pubMin;
    int bUseRealloc = 1;
    char LIBMIB_PTR *ret2;
    cbMin++; /* Always reserve room for the NUL terminator, so
	        that callers don't always have to be
		adding 1 to strlen()s */

    /* Optimized method */
   

    pCurrent = _Lookup(*ppsz); /* Also does LRU tracking */
    pubMin = cbMin;
    if (pCurrent) {
	if (pCurrent->cbAlloc > cbMin) {
	    pCurrent->pubMin = pubMin;
	    cbMin = pCurrent->cbAlloc;
	    /* We are pretty certain that the request is going to be satisfied
	       without a copy during realloc, but...we may not be able to trust
	       the pCurrent value, because the caller could have done a free(),
	       then malloc() instead of calling astrfree(), astrensure() as they
	       are supposed to.  We do a realloc to make sure the buffer still
	       is as large as it used to be....
	     */
	} else { /* We are pretty certain that the request is going to require
		    a change of alloc block length, and perhaps a copy.

		    We adjust the allocation to give room for growth, and we
		    remove any ballast allocations.
		  */
	    /* Bump up cbMin to give room to grow later */
	    if (cbMin + _profile.cbMin > cbMin) { /* Prevent integer overflow */
		cbMin += (_profile.cbMin - (cbMin % _profile.cbMin)); /* multiple of _profile.cbMin */
	    }
	    if (pCurrent->pBallast) {
		_ffree(pCurrent->pBallast);
		pCurrent->pBallast = 0;
	    }
	    if (!*ppsz) { /* Don't care about what is there now, so
			     just free & malloc, don't bother with realloc
			   */
		bUseRealloc = 0;
	    }
	}
    }

    /* Minimum first allocation according to profile */
    if (cbMin < _profile.cbMin) {
	cbMin = _profile.cbMin;
    }
    if (_profile.bvFLAGS & ASTRING_DOMOVE) {
	/* Force a move */
	if (pCurrent && pCurrent->pBallast) {
	    _ffree(pCurrent->pBallast);
	    pCurrent->pBallast = 0;
	}
	ret = _frealloc(*ppsz,cbMin);
	if (ret && (ret == *ppsz)) {
	    ret2 = _fmalloc(cbMin);
	    if (ret2) {
		_fmemcpy(ret2,ret,cbMin);
		_ffree(ret);
		ret = ret2;
	    }

	}
    } else {
	if (bUseRealloc) {
	    /* realloc does the right thing (acts as malloc) if *ppsz is 0, but
	       need to store a null terminator (done below) */
	    ret = _frealloc(*ppsz,cbMin);
	} else {
	    /* Here to avoid realloc copying */
	    if (ppsz) {
		_ffree(*ppsz);
	    }
	    if (pCurrent && pCurrent->pBallast) {
	        _ffree(pCurrent->pBallast);
	        pCurrent->pBallast = 0;
	    }
	    ret = _fmalloc(cbMin);
	}
    }
    if (!ret) {
	/* realloc couldn't satisfy the request.  The existing
	   string is freed to show there was an error. */
	if (pCurrent) {
	    pCurrent->p = 0; /* Show not used */
	    if (pCurrent->pBallast) {
		_ffree(pCurrent->pBallast);
		pCurrent->pBallast = 0;
	    }
	}
	astrfree(ppsz);
	return 0;
    }
    if (_profile.bvFLAGS & ASTRING_BALLAST) {
	if (pCurrent) {
	    pCurrent->pBallast = _fmalloc(_profile.cbMin);
	}
    }
    if (!*ppsz) { /* Make sure the new string has 0 length */
	*ret = '\0';
    }
    *ppsz = ret;
    pCurrent = _Insert(pCurrent,ret,cbMin,pubMin);
    return ret;
}

void astrfree(char LIBMIB_PTR * LIBMIB_PTR *ppsz)
{
    struct astr_s LIBMIB_PTR *pFound;
#ifdef LIBMIB_ASTRING_OPTIMIZED
    opt_astrfree(ppsz);
    return;
    if (*ppsz) {
	pFound = _Lookup(*ppsz);
	_ffree(*ppsz);
	if (pFound) {
	    pFound->p = 0;
	    if (pFound->pBallast) {
		_ffree(pFound->pBallast);
		pFound->pBallast = 0;
	    }
	}
	*ppsz = 0;
    }
#else
    if (*ppsz) {
	_ffree(*ppsz);
	*ppsz = 0;
    }
#endif
    return;
} /* astrfree */

/**************************************************************/
void astrstatic(char LIBMIB_PTR *LIBMIB_PTR *ppsz)
{ /* Similar to strensure, but always does a realloc to the exact
     string length
   */
    int cbMin;
    char LIBMIB_PTR *ret;
#ifdef LIBMIB_ASTRING_OPTIMIZED
    struct astr_s LIBMIB_PTR *pCurrent;
#endif

    if (!*ppsz) {
	return;
    }
    cbMin = _fstrlen(*ppsz)+1; /* Always reserve room for the Null terminator, so
	        that callers don't always have to be
		adding 1 to strlen()s */
#ifdef LIBMIB_ASTRING_OPTIMIZED
    pCurrent = _Lookup(*ppsz); /* Also does LRU tracking */
    if (pCurrent) {
	if (pCurrent->pBallast) {
	    _ffree(pCurrent->pBallast);
	    pCurrent->pBallast = 0;
	}
	pCurrent->p = 0; /* Show not used */
    }
#endif
    ret = _frealloc(*ppsz,cbMin); /* Always realloc */
    if (!ret) { /* Oh well, nothing lost */

    } else {
	*ppsz = ret;
    }
    return;
} /* astrstatic */
/**************************************************************/

#endif


