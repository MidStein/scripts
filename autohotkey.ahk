#KeyHistory 0

CapsLock::Esc

+F9::
  Gui, New

  Gui, Add, Edit, vTaskName
  Gui, Add, Button, gRunTask, RunTask

  Gui, Add, Text, , 01. CursorLeft
  Gui, Add, Text, , 02. ClickCenterRight
  Gui, Add, Text, , 03. GameMode
  Gui, Add, Text, , 04. NonGameMode
  Gui, Add, Text, , 05. EntertainMode
  Gui, Add, Text, , 06. MusicMode
  Gui, Add, Text, , 07. HackingMode
  Gui, Add, Text, , 08. NonHackingMode

  Gui, -SysMenu
  Gui, Show
return

CursorLeft:
  CoordMode, Mouse, Screen
  MouseMove, 0, A_ScreenHeight/2
Return

ClickCenterRight:
  CoordMode, Mouse, Screen
  MouseMove, 2 * A_ScreenWidth/3, A_ScreenHeight/2
  Click
  MouseMove, 0, A_ScreenHeight/2
Return

GameMode:
  ; https://www.autohotkey.com/docs/v1/Variables.htm
  ValorantPowerSchemeGuid := "f15e6c06-cc0e-4f4b-876f-e71c9d63af1e"
  ; https://www.autohotkey.com/board/topic/101027-switching-power-plans-using-ahk/
  Run, % "powercfg -SETACTIVE " . ValorantPowerSchemeGuid

  Send, {LWin}
  Sleep, 1000
  Send, AMD Radeon Settings
  Sleep, 1000
  Send, {Enter}
  Sleep, 2000
  Send, {Tab 3}
  Sleep, 1000
  Send, {Space}
  Sleep, 1000
  WinClose, Radeon
Return

NonGameMode:
  HpRecommendedPowerSchemeGuid := "48684d4a-8524-4093-8a63-ea7132b79c1c"
  Run, % "powercfg -SETACTIVE " . HpRecommendedPowerSchemeGuid

  Send, {LWin}
  Sleep, 1000
  Send, AMD Radeon Settings
  Sleep, 1000
  Send, {Enter}
  Sleep, 2000
  Send, {Tab 5}
  Sleep, 1000
  Send, {Space}
  Sleep, 1000
  WinClose, Radeon
Return

EntertainMode:
  Run, explorer D:\entertain
  Sleep, 1000
  Send, {Space}

  For property in ComObjGet( "winmgmts:\\.\root\WMI" ).ExecQuery( "SELECT * FROM WmiMonitorBrightnessMethods" ) {
    property.WmiSetBrightness(1, 100)
  }
Return

MusicMode:
  Run, chrome
  Sleep, 1000
  Send, open.spotify.com/search{Enter}
  Sleep, 5000
  Send, gi
Return

HackingMode:
  For property in ComObjGet( "winmgmts:\\.\root\WMI" ).ExecQuery( "SELECT * FROM WmiMonitorBrightnessMethods" ) {
    property.WmiSetBrightness(1, 0)
  }

  ; https://www.autohotkey.com/boards/viewtopic.php?t=60028
  SoundSet, +1, , Mute

  Send, {LWin}
  Sleep, 1000
  Send, lid
  Sleep, 1000
  Send, {Enter}
  Sleep, 1000
  Send, {Tab 3}{Up}{Tab 4}{Enter}
  Sleep, 1000
  WinClose, Power
Return

NonHackingMode:
  For property in ComObjGet( "winmgmts:\\.\root\WMI" ).ExecQuery( "SELECT * FROM WmiMonitorBrightnessMethods" ) {
    property.WmiSetBrightness(1, 30)
  }

  ; https://www.autohotkey.com/boards/viewtopic.php?t=60028
  SoundSet, +1, , Mute

  Send, {LWin}
  Sleep, 1000
  Send, lid
  Sleep, 1000
  Send, {Enter}
  Sleep, 1000
  Send, {Tab 3}{Down}{Tab 4}{Enter}
  Sleep, 1000
  WinClose, Power
Return

RunTask:
  GuiControlGet, TaskName
  if (TaskName = "01") {
    GoSub, CursorLeft
  }
  else if (TaskName = "02") {
    GoSub, ClickCenterRight
  }
  else if (TaskName = "03") {
    GoSub, GameMode
  }
  else if (TaskName = "04") {
    GoSub, NonGameMode
  }
  else if (TaskName = "05") {
    GoSub, EntertainMode
  }
  else if (TaskName = "06") {
    GoSub, MusicMode
  }
  else if (TaskName = "07") {
    GoSub, HackingMode
  }
  else if (TaskName = "08") {
    GoSub, NonHackingMode
  }
  Gui, destroy
return
