Set WshShell = CreateObject("WScript.Shell")

currentFolder = Left(
    WScript.ScriptFullName,
    InStrRev(WScript.ScriptFullName, "\")
)

WshShell.Run _
    Chr(34) & currentFolder & "init.bat" & Chr(34), _
    0, _
    False