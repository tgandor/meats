/*  libmib/parse/asprintf.c version 1998.08.20 (from libmib )
   Summary/Purpose: allocated string functions
     - - - - - - - - - - - - Copyright Notice - - - - - - - - - - - -
       Copyright 1999 Forrest J. Cavalier III

     IMPORTANT: This software may have been modified from the original
     "Libmib Mature" sources.  See http://www.mibsoftware.com/libmib/ for
     documentation and up-to-date original copies.

     This software is provided by Forrest J. Cavalier III, d-b-a
     Mib Software, under the following terms and conditions.

     Contact Mib Software (mibsoft@mibsoftware.com) to discuss custom
     and enhanced versions of this and other software, other licensing
     terms, and support. We would appreciate that you notify us of defect
     discoveries and enhancements so that others can benefit from work
     on this software. Other licensing arrangements are made in writing.

    - - - - - - - - - - - - - License - - - - - - - - - - - - - - - - -
     Permission is hereby granted, to any person obtaining a copy of
     this software (the "Software"), to deal in the Software without
     restriction, including the rights to use, copy, modify, merge,
     publish, distribute, sublicense, and/or sell copies of the Software,
     subject to all the following conditions.

     1. The above copyright notice and this permission notice shall
        be included in all copies of the source code or portions thereof.

     2. The Software source code may be distributed in unmodified form.

     3. The Software may be distributed in modified forms provided that
        the names and reputation of Mib Software and Libmib, and
        derivatives, shall not be used to advertise, describe, or 
        distribute the software, except within the source code itself.
        
     4. The electronic and printed documentation external to the source
        code shall not be distributed.

     
     5. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 
*/
/*BSELIMP*/
/**************************************************************/
/* This file supports selective implementation control.
 * See
 *    http://www.mibsoftware.com/libmib/selective.htm
 */
#ifdef LIBMIB_DEFAULT_NOIMPL
/* NOIMP everything that is not explicitly LIBMIB_IMP'ed
 */
#ifndef LIBMIB_IMPL_ASPRINTF_HEADER
#define LIBMIB_NOIMPL_ASPRINTF_HEADER
#endif

#ifndef LIBMIB_IMPL_avsprintf
#define LIBMIB_NOIMPL_avsprintf
#endif

#endif
/*ESELIMP*/

/**************************************************************/


#ifndef LIBMIB_NOIMPL_ASPRINTF_HEADER
#define LIBMIB_IMPLEMENT
#include "compat.h"
#include <malloc.h>
#include <string.h>
#include <assert.h>
#include "astring.h"
#include <stdlib.h> /* declaration of exit() */
/**************************************************************/
/* Sort out what implementation of asprintf we are supposed to use,
 * and adjust some compiler switches accordingly
 */

#ifdef ASTRING_USE_VSNPRINTF
/* This is the "best" implementation. */
#define ASTRING_HAVE_VSNPRINTF 1  /* if you are running some O/S which
                                   * has vsnprintf, that's best.
				   */
#else
#ifdef ASTRING_USE_SNPRINTF
    /* There is alternate code to implement asprintf without vsnprintf.
     * It is a more complicated implementation, and harder to follow, but
     * not really less efficient.
     */
#define ASTRING_HAVE_SNPRINTF 1
#else
#ifdef ASTRING_USE_SPRINTF
    /* 
     * If you only have sprintf, but not snprintf(), then there still is
     * an implementation that will work. In very rare cases, it can
     * fail to prevent a buffer overrun.  It exits.
     */
#else
/* Just leave it out altogether */
#define ASTRING_NOASPRINTF
#endif
#endif
#endif /* NOIMPL */
/**************************************************************/



/**************************************************************/
/* Use macros for critical error reporting.  See the libmib docs
 * on the subject.  If they aren't defined yet, use the
 * standard defaults.
 */
#ifndef PR_CRIT
#define PR_CRIT(msg) fprintf(stderr,"%s",msg);exit(-1);
#endif
#ifndef TSD
#define TSD(id,string) (string)
#endif


/**************************************************************/
#ifndef ASTRING_NOASPRINTF
/* If we are implementing asprintf, then we need to include some
 * additional files.
 */
#include <stdarg.h>
#include <ctype.h>
#endif
/**************************************************************/


/**************************************************************/
/* The windows libraries have some _ prefix function names.  This
 * code uses the non-prefix names.
 */
#ifdef WIN32
#define vsnprintf _vsnprintf
#define snprintf _snprintf
#endif
#ifdef _MSC_VER
#define vsnprintf _vsnprintf
#define snprintf _snprintf
#endif
/**************************************************************/



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
#endif /* NOIMP section */
/**************************************************************/


#ifndef LIBMIB_NOIMPL_avsprintf
/**************************************************************/

#ifdef ASTRING_HAVE_VSNPRINTF
/* This code is for systems which have a vsnprintf() function call.

   Although it is slow and stupid, we do the "if at first you don't
   succeed, try and try again" method which saves us all the
   argument munching we have to do on other systems.  We allocate
   a pretty big buffer at first anyway.
 */
int avsprintf(char LIBMIB_PTR * LIBMIB_PTR *ppasz,const char *format,va_list ap)
{
    
    size_t needlen;
    int cnt; /* Changed from unsigned 10/21/98: need to handle -1 return from vsnprintf */
    char LIBMIB_PTR *ret = 0;

    needlen = _fstrlen(format)+256;
    while(1) {
	astrensure(ppasz,needlen);
	if (!ppasz) {
	    return -1; /* out of memory! */
	}
	cnt = vsnprintf(*ppasz,needlen-1,format,ap);
	if (cnt > (int) needlen-1) {
	    PR_CRIT(TSD(F_libmib_astring_100,"F_libmib_astring_100: vsnprintf failed to stop overrun.\n"));
	    exit(-1);
	}
	if (cnt > 0) {
	    break; /* Success */
	}
	if (needlen * 4 < needlen) { /* overflow */
	    astrfree(ppasz); /* String won't fit in anything we can allocate! */
	    return -1;
	}
	needlen *= 4; /* Go around to get more space */
    }
    /* Since we could have formatted some \0's, we can't trust
       astrstatic() to work, but we don't want to have a huge
       buffer wasting space....
     */
    if (needlen > cnt+_profile.cbMin) { /* There is a bunch of wasted space. */
	ret = _frealloc(*ppasz,cnt+1);
	if (!ret) { /* Oh well, no way to reclaim */
	} else {
	    *ppasz = ret;
	}
    }
    return cnt;
} /* avsprintf */


int asprintf(char LIBMIB_PTR * LIBMIB_PTR *ppasz,const char *format,...)
{
    
    va_list ap;

    va_start(ap, format);
    return avsprintf(ppasz,format,ap);
} /* asprintf */


#else

/***************************************************************/
/* The remaining code is for systems without vsnprintf.
 * The strategy requires that we parse the printf format string
 * ourselves, try to predict how much space each item will take,
 * and then hand it in pieces to s[n]printf.  We can predict the
 * length of %s very accurately, so external input attacks
 * are going to be thwarted.
 *
 *
 * If we don't have snprintf, we just use sprintf.  In the very
 * rare case the prediction + extra space allocated was not enough,
 * then the sprintf() call corrupts allocated memory.  We detect
 * it using the sprintf return value, print a message and abort.
 *
 */
#ifdef ASTRING_HAVE_SNPRINTF
/* If we have snprintf, then we can retry if our prediction on
 * how much space was needed turns out to be inadequate.
 */
#define ARGBUF(buf,len) buf,len
#else
#define snprintf sprintf
#define ARGBUF(buf,len) buf
#endif

/* What follows first are three variants of a local helper function,
   to handle all cases of format specifiers which take a '*' width argument, 
   e.g.   ("Printing %10.*s",len,string)

   Then the actual astring() function
 */

LIBMIB_PRIVATE va_list do_snprintfw0(int *cnt, /* return value */
			     char *buf,
			     int cbBuf,
			     const char *pszFormat,
			     int argtype,
			     va_list apnext,
			     const char *sarg)
{
/*    int argtype; Low 8 bits is size
 * Next 8 bits is type, as follows
 */
#define ARGSARG 0x100
#define ARGPVOID 0x200
#define ARGINT 0x300
#define ARGFLOATING 0x400
#define ARGCHAR 0x500
#define ARGPERCT 0x600

    switch(argtype & 0xFF00) {
    case ARGINT:
	switch(argtype & 0xFF) {
	case 3:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,short));
	break;
#ifdef ASTRING_HAVE_LONG_LONG
	case 4: 
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,long long int));
	break;
#endif
	case 1:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,long int));
	break;
	case 0:
	default:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,int));
	break;
	}
	break;
    case ARGPVOID:
    	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,void *));

	break;
    case ARGCHAR:
    	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,char));

	break;
    case ARGFLOATING:
	switch(argtype & 0xff) {
	case 2:
    	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,long double));
	break;
	default:
    	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,va_arg(apnext,double));
	break;
	}
	break;
    case ARGPERCT:
	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat);
	break;
    case ARGSARG:
	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,sarg);
	break;
    default:
	/* Unknown type */
	assert(0);
	PR_CRIT(TSD(F_libmib_astring_101,"F_libmib_astring_101: asprintf failed. Unknown type\n"));
	exit(-1);
    break;
    }
    return apnext;
}

LIBMIB_PRIVATE va_list do_snprintfw1(int *cnt, /* return value */
			     char *buf,
			     int cbBuf,
			     const char *pszFormat,
			     int w1,
			     int argtype,
			     va_list apnext,
			     const char *sarg)
{
/*    int argtype; Low 8 bits is size
 * Next 8 bits is type, as follows
 */
    switch(argtype & 0xFF00) {
    case ARGINT:
	switch(argtype & 0xFF) {
	case 3:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,short));
	break;
#ifdef ASTRING_HAVE_LONG_LONG
	case 4: 
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,long long int));
	break;
#endif
	case 1:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,long int));
	break;
	case 0:
	default:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,int));
	break;
	}
	break;
    case ARGPVOID:
    	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,void *));

	break;
    case ARGCHAR:
    	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,char));

	break;
    case ARGFLOATING:
	switch(argtype & 0xff) {
	case 2:
    	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,long double));
	break;
	default:
    	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,va_arg(apnext,double));
	break;
	}
	break;
    case ARGPERCT:
	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1);
	break;
    case ARGSARG:
	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,sarg);
	break;
    default:
	/* Unknown type */
	assert(0);
	PR_CRIT(TSD(F_libmib_astring_101,"F_libmib_astring_101: asprintf failed. Unknown type\n"));
	exit(-1);
    break;
    }
    return apnext;
}

LIBMIB_PRIVATE va_list do_snprintfw2(int *cnt, /* return value */
			     char *buf,
			     int cbBuf,
			     const char *pszFormat,
			     int w1,int w2,
			     int argtype,
			     va_list apnext,
			     const char *sarg)
{
/*    int argtype; Low 8 bits is size
 * Next 8 bits is type, as follows
 */
    switch(argtype & 0xFF00) {
    case ARGINT:
	switch(argtype & 0xFF) {
	case 3:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,short));
	break;
#ifdef ASTRING_HAVE_LONG_LONG
	case 4: 
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,long long int));
	break;
#endif
	case 1:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,long int));
	break;
	case 0:
	default:
	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,int));
	break;
	}
	break;
    case ARGPVOID:
    	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,void *));

	break;
    case ARGCHAR:
    	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,char));

	break;
    case ARGFLOATING:
	switch(argtype & 0xff) {
	case 2:
    	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,long double));
	break;
	default:
    	    *cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,va_arg(apnext,double));
	break;
	}
	break;
    case ARGPERCT:
	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2);
	break;
    case ARGSARG:
	*cnt = snprintf(ARGBUF(buf,cbBuf),pszFormat,w1,w2,sarg);
	break;
    default:
	/* Unknown type */
	assert(0);
	PR_CRIT(TSD(F_libmib_astring_101,"F_libmib_astring_101: asprintf failed. Unknown type\n"));
	exit(-1);
    break;
    }
    return apnext;
}

int avsprintf(char **ppasz,const char *format,va_list ap)
{
    
    va_list apnext;
    int argtype; /* Low 8 bits is size */
		/* Next 8 bits is type */

    int w1;
    int w2;
    const char *p = format;
    const char *s = p;
    const char *sarg;
    int argWidth;
    int needlen;
    int cnt;
    int off = 0;
    char *subf = 0;

    astrcpy(ppasz,"");

    off = 0;
    while(*p) {
	if (*p != '%') {
	    p++;
	} else {
	    if (p > s) {
		astrensure(ppasz,p-s+off);
		strncpy(*ppasz+off,s,p-s);
		*(*ppasz+off+(p-s)) = '\0';
		off += p - s;
	    }
	    argWidth = 0;
	    s = p;
	    p++;
	    /*	We recognize a 7 part sequence starting with '%', which we
	        then hand out to vsprintf() to process.

		%		    required
		-		    optional
		[0-9]* or *	    optional (take arg)
		.[0-9]* or *	    optional (take arg)
		lLhq		    optional
		[doxfegcsu%]	    required
	    */
	    argtype = 0;
	    apnext = ap;
	    w1 = 0;
	    w2 = 0;
	    /* flags... */
	    p += strspn(p,"#0 +-"); /* We don't process them, we just skip them */
	    if (*p == '*') {
		w1 = va_arg(apnext,int);
		argWidth |= 1;
		p++;
	    } else while(isdigit(*p)) {
		w1 *= 10;
		w1 += *p - '0';
		p++;
	    }
	    if (*p == '.') {
		p++;
		if (*p == '*') {
		    w2 = va_arg(apnext,int);
		    argWidth |= 2;
		    p++;
		} else while(isdigit(*p)) {
		    w2 *= 10;
		    w2 += *p - '0';
		    p++;
		}
	    }
	    switch(*p) {
	    case 'L':
		argtype = 2;	/* long double */
		p++;
		break;
	    case 'l':
		argtype = 1;
		p++;
		break;
	    case 'h':
		argtype = 3;
		p++;
		break;
	    case 'q':
		argtype = 4;
		p++;
		break;
	    default:
		break;
	    }
	    /* Finally: the conversion character */
	    if (*p == 'n') {
		/* Store strlen */
		if (argtype == -1) {
		    *(va_arg(apnext,short int *)) = off;
		} else {
		    *(va_arg(apnext,int *)) = off;
		}
		p++;
	    } else {
		p++;
		/* Generate the format string.... */
		astrn0cpy(&subf,s,p-s);
		/* Determine the argument type and space needed */
		switch(*(p-1) ) {

		case 'c':case 'C':
		    needlen = w1+w2+16;
		    argtype |= ARGCHAR;
		    break;

		case 's':case 'S':
		    argtype |= ARGSARG;
		    sarg = va_arg(apnext,char *);
		    if (!sarg) {
			sarg = "(null)";
		    }
		    needlen = strlen(sarg)+w1+w2+1;
		    break;

#ifdef ASTRING_UPPERFMTLONG
		case 'D':case 'O':case 'U':
		    argtype = 1;
#endif
		case 'u':case 'i':case 'd':case 'o':case 'x':case 'X':
		    needlen = w1+w2+64;
		    argtype |= ARGINT;
		    break;

		case 'p':
		    needlen = w1+w2+64;
		    argtype |= ARGPVOID;
		    break;

		case 'E':case 'e':
		case 'f':
		case 'G':case 'g':
		    /* 1024 extra should be enough  */
		    argtype |= ARGFLOATING;
		    needlen = w1+w2+1024;
		    break;
		case '%':
		    argtype |= ARGPERCT;
		break;
		default: /* Unknown type */
		    needlen = w1+w2+1024;
		    break;
		}
		ap = apnext; /* Where we start */

		while(1) { /* Until we get it */
		    astrensure(ppasz,off+needlen);
		    apnext = ap; /* Reset */
		    if (argWidth == 2) {
			apnext = do_snprintfw1(&cnt,*ppasz+off,needlen,subf,w2,argtype,apnext,sarg);
		    } else if (argWidth == 1) {
			apnext = do_snprintfw1(&cnt,*ppasz+off,needlen,subf,w1,argtype,apnext,sarg);
		    } else if (argWidth == 3) {
			apnext = do_snprintfw2(&cnt,*ppasz+off,needlen,subf,w1,w2,argtype,apnext,sarg);
		    } else {
			apnext = do_snprintfw0(&cnt,*ppasz+off,needlen,subf,argtype,apnext,sarg);
		    }
		    if ((cnt >= 0) && (cnt < needlen - 5)) { /* Didn't hit the limit */
			break;
		    }
#ifndef ASTRING_HAVE_SNPRINTF
		    /* Don't have snprintf, so we just trashed something
		     * we give up.
		     */
		    
		    PR_CRIT(TSD(F_libmib_astring_102,"F_libmib_astring_102: asnprintf overrun.  didn't predict "));
		    PR_CRIT(subf);
		    exit(-1);
#endif
		    needlen += 256;
		}
		off += cnt;
	    }
	    ap = apnext;
	    s = p;	/* Continue */
	}
    }
    if (p > s) {
	astrensure(ppasz,p-s+off);
	strncpy(*ppasz+off,s,p-s);
	*(*ppasz+off+(p-s)) = '\0';
	off += p - s;
    }
    astrfree(&subf);
    return off;

} /* avsprintf */
int asprintf(char **ppasz,const char *format,...)
{
int ret;
    va_list ap;
    va_start(ap, format);
    return avsprintf(ppasz,format,ap);
} /* asprintf */

#endif /* end of else clause ASTRING_HAVE_VSNPRINTF */
#endif /* NOIMP section */
