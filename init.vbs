Set WshShell = CreateObject("WScript.Shell")

WshShell.Run Chr(34) & Replace(WScript.ScriptFullName, "init.vbs", "init.bat") & Chr(34), 0, False

Set WshShell = Nothing