#KeyHistory 0

CapsLock::Esc

+F9::
  Gui, New

  Gui, Add, Edit, vTaskName
  Gui, Add, Button, gRunTask, RunTask

  Gui, Add, Text, , 01. CursorLeft
  Gui, Add, Text, , 02. ClickCenterRight 

  Gui, -SysMenu 
  Gui, Show
return

CursorLeft:
  CoordMode, Mouse, Screen
  MouseMove, 0, A_ScreenHeight/2
return

ClickCenterRight:
  CoordMode, Mouse, Screen
  MouseMove, 2 * A_ScreenWidth/3, A_ScreenHeight/2
  Click
return


RunTask:
  GuiControlGet, TaskName
  if (TaskName = "01") {
    GoSub, CursorLeft
  }
  else if (TaskName = "02") {
    GoSub, ClickCenterRight
  }
  Gui, destroy
return

