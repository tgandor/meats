#include <my_global.h>
#include <my_sys.h>

#include <mysql.h>
#include <m_ctype.h>
#include <m_string.h>	

#ifndef _MSC_VER
#  define __declspec(anything)
#endif

/*
 -- The SQL script for installation:

 drop function if exists countstr;
 create function countstr(needle text, haystack text) returns int soname 'udf_countstr.dll';
 
 drop function if exists bmh_countstr;
 create function bmh_countstr(needle text, haystack text) returns int soname 'udf_countstr.dll';
 
 -- Simple stored functions, doing the same

 -- a) by string replacement
drop function if exists sf_countstr;
create function sf_countstr(needle text, haystack mediumtext) returns int
return (
  length(haystack)-length(replace(haystack, needle, ''))
) / length(needle);

 -- b) by repeated searching
drop function if exists sfi_countstr;
delimiter $$
create function sfi_countstr (needle text, haystack mediumtext) returns int
begin
set @num = 0;
set @pos = locate(needle, haystack);
while @pos <> 0 do
  set @num = @num + 1;
  set @pos = locate(needle, haystack, @pos+1);
end while;
return @num;
end $$
delimiter ;


 -- Uninstall script:
 
 drop function if exists countstr;
 drop function if exists bmh_countstr;
 
 drop function if exists sf_countstr;
 drop function if exists sfi_countstr;

 */

extern "C" {
	
	/* Naive search algorithm */

	__declspec(dllexport) 
	my_bool 
	countstr_init(UDF_INIT *initid, UDF_ARGS *args, char *message ) {
		if ( args->arg_count != 2 ) {
			strcpy(message, "wrong number of arguments: countstr() requires two arguments");
			return 1;
		}
		return 0;
	}

	__declspec(dllexport)
	long long 
	countstr(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error ) {
		unsigned int i=0, j=0;
		int count = 0;
		if ( args->lengths[0] > args->lengths[1] ) 
			return 0;
		while(i < args->lengths[1] - args->lengths[0] + 1) {
			while(j < args->lengths[0] && args->args[0][j] == args->args[1][i+j])
				++j;
			if (j == args->lengths[0]) {
				++count;
				i += j;
			} else {
				++i;
			}
			j = 0;
		}
		return count;
	}
	
	__declspec(dllexport)
	void 
	countstr_deinit(UDF_INIT *initid) {
	}

	/* Boyer-Moore-Horspool */

	inline int *precomp(char *needle, int nlen) {
		int *badchar = (int *)malloc(255*sizeof(int));
		for(int i=0; i<255; ++i)
			badchar[i] = nlen;
		int last = nlen-1;
		for(int i=0; i<last; ++i)
			badchar[(unsigned char)needle[i]] = last - i;
		return badchar;
	}

	__declspec(dllexport) 
	my_bool 
	bmh_countstr_init(UDF_INIT *initid, UDF_ARGS *args, char *message ) {
		if ( args->arg_count != 2 ) {
			strcpy(message, "wrong number of arguments: bmh_countstr() requires two arguments");
			return 1;
		}
		if ( args->args[0] ) { // first argument constant
			initid->ptr = (char *)precomp(args->args[0], args->lengths[0]);
		} else 
			initid->ptr = 0;
		return 0;
	}

	__declspec(dllexport)
	long long bmh_countstr(UDF_INIT *initid, UDF_ARGS *args, char *is_null, char *error ) {
		if ( args->lengths[0] > args->lengths[1] ) 
			return 0;

		int count = 0;
		
		int *badchar;
		unsigned i=0;
		if ( initid->ptr )
			badchar = (int *)initid->ptr;
		else
			badchar = precomp(args->args[0], args->lengths[0]);
		int last = args->lengths[0]-1;
		while (i < args->lengths[1] - args->lengths[0] + 1) {
			int j;
			for(j=last; args->args[0][j]==args->args[1][i+j]; --j) {
				if (!j) {
					++count;
					break;
				}
			}
			i += badchar[(unsigned char)args->args[1][i+last]];
		}

		if ( !initid->ptr ) {
			free(badchar);
		}

		return count;
	}
	
	__declspec(dllexport)
	void 
	bmh_countstr_deinit(UDF_INIT *initid) {
		if ( initid->ptr ) {
			free(initid->ptr);
		}
	}
}
