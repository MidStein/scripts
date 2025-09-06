# Scripts

Automation scripts and helper tools.

---

### Items

- [check-battery.py](#check-batterypy)
- [commit-msg](#commit-msg)
- [dotfiles-symlinker.bash](#dotfiles-symlinkerbash)
- [gmail](#gmail)
- [indgovtjobs.py](#indgovtjobspy)
- [packages-changed.py](#packages-changedpy)
- [rand.py](#randpy)
- [reminders.py](#reminderspy)
- [size-reducer.py](#size-reducerpy)
- [tmux-workspace.bash](#tmux-workspacebash)
- [toggle-wifi.bash](#toggle-wifibash)

---

## check-battery.py

Check if battery percentage is 100 and if so, send a desktop notification.

## commit-msg

This hook fails a `git commit` if commit subject is greater than 50 characters.

## dotfiles-symlinker.bash

Create symlinks for various dotfiles from ~/dotfiles to the paths where they
get read from associated software.

## gmail

These scripts use Google APIs that interact with Gmail and Calendar. They use
OAuth2 to authenticate with Google.

Requirements:

- [psutil](https://github.com/giampaolo/psutil)
- [Google API Client](https://github.com/googleapis/google-api-python-client/)
- [Google Auth Python
  Library](https://github.com/googleapis/google-auth-library-python)
- [google-auth-library-python-oauthlib](https://github.com/googleapis/google-auth-library-python-oauthlib)

### notifier.py

Shows a desktop notification if there is an unread email in the Gmail inbox.

### self.py

Sends me a gmail. This gets used by reminders.py and indgovtjobs.py. While
there is no Gmail API to schedule emails, I use a Calendar hack to get
scheduled gmails in this script. I create a calendar event for a particular
time and set notifying me at the time of the event by gmail. The gmail ends up
showing the title and description of the event.

### delete-reminders.py

Delete Google Calendar events created by reminders.py, so that the calendar
stays clean.

## indgovtjobs.py

Emails me all new IT fresher jobs by indgovtjobs.in. It uses gmail/self.py to
send me a gmail.

Requires [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## packages-changed.py

Gives a diff of which packages have I installed and removed from the last time.

In another file, I maintain a list of packages that I have installed which are
not dependencies of other packages and another list of which packages I have
uninstalled. If I were to install archlinux elsewhere, I would refer back to
that file.

## rand.py

Pick random lines from stdin. Useful with `seq` to generate random numbers that
fall in a range. It gives 5 outputs by default, in case I don't like one
output, I try the next.

## reminders.py

Sets up reminders for a particular day by scheduling Gmail notifications. This
uses gmail/self.py.

Requires [Pydantic](https://docs.pydantic.dev/latest/)

## size-reducer.py

Reduces size of JPEG, PNG and PDF files to lower than a passed size.

Uses Pillow library to reduce image files. It tries to reduce image quality 5%
at a time till the file size becomes lower than that passed. Reducing PDF sizes
with Ghostscript works occasionally. Ghostscript only provides `ebook` and
`screen` settings to reduce file size. I use this script to comply with various
application registration websites that restrict file upload to a specific size.

Requires [Pillow](https://pillow.readthedocs.io/en/stable/) and
[Ghostscript](https://www.ghostscript.com/)

## tmux-workspace.bash

Sets up a tmux session according to my preferred way of working.

I open one session for each project, which in turn is based on one directory
path. It starts three windows. The first one has nvim running. The second and
third window have 4 panes, with two panes maximized to work in and the other
two as substitutes. The third window is always open with panes opened at home
directory. This means, I run all project specific commands in the second window
and non project specific commands in the third window.

Project specific setup commands are saved in a different file which this script
loads. It also sets the project name at the right of the status line. This
script also loads the last saved nvim session to get me back to where I left
nvim for example during the last day.

## toggle-wifi.bash

Toggle Wi-Fi on/off.
