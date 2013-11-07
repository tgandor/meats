REM  *****  BASIC  *****

REM -- PASTE THIS INTO YOUR [My Macros & Dialogs].Standard
REM -- (or: toolbar command "Insert BASIC Source")
REM -- having it in a library does not work
REM -- alternatively you can paste it into document's own module
REM -- (probably when you like to confirm every time you open it)

Function HUMAN(a)
	Let sufix = "  "
	If a > 1024 then 
		a = a / 1024
		sufix = " K"
	End If
	If a > 1024 then 
		a = a / 1024
		sufix = " M"
	End If
	If a > 1024 then 
		a = a / 1024
		sufix = " G"
	End If
	If a > 1024 then 
		a = a / 1024
		sufix = " T"
	End If
	If a > 1024 then 
		a = a / 1024
		sufix = " P"
	End If
	Dim b as Long
	b = a * 10
	a = b / 10
	HUMAN = a & sufix
End Function
