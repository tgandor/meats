REM  *****  BASIC  *****

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
	Dim b as Long
	b = a * 10
	a = b / 10
	HUMAN = a & sufix
End Function

Sub Main

End Sub
