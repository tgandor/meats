" I found it somewhere else, but almost the same thing is here:
" https://superuser.com/questions/1091942/

Const rootdir = "C:\"
Const logname = "GlobalHotkeys.txt"

Set fso = CreateObject("Scripting.FileSystemObject")
Set wshell = CreateObject("WScript.Shell")

Set logfile = fso.CreateTextFile(logname, True)
logfile.Write "Searching for shortcuts with hotkeys" & vbCrLf

recursedirs(fso.GetFolder(rootdir))

logfile.Write "Done searching" & vbCrLf
logfile.Close

Sub recursedirs(dir)
    If trylistdir(dir) Then
        For Each subdir In dir.SubFolders
            recursedirs subdir
        Next

        For Each file In dir.Files
            extn = fso.GetExtensionName(file.Path)
            If LCase(extn) = "lnk" Then
                check(file.Path)
            End If
        Next
    End If
End Sub

Function trylistdir(dir)
    On Error Resume Next
    trylistdir = (dir.SubFolders.Count + dir.Files.Count >= 0)
End Function

Sub check(fname)

    Set lnk = wshell.CreateShortcut(fname)
    hk = lnk.Hotkey
    If hk <> "" then
        logfile.Write fname & " : " & hk & vbCrLf
    End If

End Sub
