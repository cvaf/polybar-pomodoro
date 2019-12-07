# polybar-pomodoro
Polybar module for a simple pomodoro timer.

Display during a task: ![]('imgs/screen_busy.png')

Display during a break: ![]('imgs/screen_break.png')


Add the following to our polybar config:

```
[module/pomodoro]
type = custom/script

interval = 1
format-background = ${color.mf}
format-foreground = ${color.fg}
exec = "python ~/Documents/Python/pomo/pomo_action.py --opt='update'"

click-left = python ~/Documents/Python/pomo/pomo_action.py --opt='left'
click-middle = python ~/Documents/Python/pomo/pomo_action.py --opt='middle'
click-right = python ~/Documents/Python/pomo/pomo_action.py --opt='right'


[module/pomodoro_i]
type = custom/text

content = ♛
content-background = ${color.purple}
content-foreground = ${color.fg}
content-padding = 1

click-left = "python ~/Documents/Python/pomo/pomo_action.py --opt='left'" &
click-middle = "python ~/Documents/Python/pomo/pomo_action.py --opt='middle'" &
click-right = "python ~/Documents/Python/pomo/pomo_action.py --opt='right'" &
```