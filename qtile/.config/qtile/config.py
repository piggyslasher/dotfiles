# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
from typing import List  # noqa: F401
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
# from libqtile.utils import guess_terminal
from libqtile import hook
from datetime import datetime as dt
import os
import subprocess
# import dex
from plasma import Plasma
from libqtile.config import EzKey


@hook.subscribe.startup
def dbus_register():
    id = os.environ.get('DESKTOP_AUTOSTART_ID')
    if not id:
        return
    subprocess.Popen(['dbus-send',
                      '--session',
                      '--print-reply',
                      '--dest=org.gnome.SessionManager',
                      '/org/gnome/SessionManager',
                      'org.gnome.SessionManager.RegisterClient',
                      'string:qtile',
                      'string:' + id])


# When application launched automatically focus it's group


@hook.subscribe.client_new
def modify_window(client):
    # if (client.window.get_wm_transient_for() or client.window.get_wm_type() in floating_types):
    #    client.floating = True

    for group in groups:  # follow on auto-move
        match = next((m for m in group.matches if m.compare(client)), None)
        if match:
            # there can be multiple instances of a group
            targetgroup = client.qtile.groups_map[group.name]
            targetgroup.cmd_toscreen(toggle=False)
            break

# Hook to fallback to the first group with windows when last window of group is killed


@hook.subscribe.client_killed
def fallback(window):
    if window.group.windows != {window}:
        return

    for group in qtile.groups:
        if group.windows:
            qtile.current_screen.toggle_group(group)
            return
    qtile.current_screen.toggle_group(qtile.groups[0])


# Work around for matching Spotify


@hook.subscribe.client_new
def slight_delay(window):
    time.sleep(0.02)


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

# Add th, nd or st to the date - use custom_date in text box


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


def custom_date():
    return custom_strftime('%A, {S} %B', dt.now())


mod = "mod4"

terminal = 'kitty'
home = os.path.expanduser('~')

MYCOLORS = [
    '#1f1f1f',  # BLACK
    '#de352e',  # RED
    '#2dc55e',  # GREEN
    '#f3bd09',  # YELLOW
    '#1081d6',  # BLUE
    '#6c71c4',  # MAGENTA / PERIWINKLE
    '#1dd361',  # CYAN
    '#eee8d5'   # WHITE
]

BLACK = MYCOLORS[0]
RED = MYCOLORS[1]
GREEN = MYCOLORS[2]
YELLOW = MYCOLORS[3]
BLUE = MYCOLORS[4]
MAGENTA = MYCOLORS[5]
CYAN = MYCOLORS[6]
WHITE = MYCOLORS[7]

# keys = [
#     Key([mod, 'control'], 'l', lazy.spawn('gnome-screensaver-command -l')),
#     Key([mod, 'control'], 'q',
#         lazy.spawn('gnome-session-quit --logout --no-prompt')),
#     Key([mod, 'shift', 'control'], 'q',
#         lazy.spawn('gnome-session-quit --power-off')),
#     # Switch between windows in current stack pane
#     Key([mod], "k", lazy.layout.down(),
#         desc="Move focus down in stack pane"),
#     Key([mod], "j", lazy.layout.up(),
#         desc="Move focus up in stack pane"),

#     # Key([mod], "h", lazy.layout.left()),
#     # Key([mod], "l", lazy.layout.right()),
#     Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
#     Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
#     Key([mod, "mod1"], "j", lazy.layout.flip_down()),
#     Key([mod, "mod1"], "k", lazy.layout.flip_up()),
#     Key([mod, "mod1"], "h", lazy.layout.flip_left()),
#     Key([mod, "mod1"], "l", lazy.layout.flip_right()),
#     Key([mod, "control"], "j", lazy.layout.grow_down()),
#     Key([mod, "control"], "k", lazy.layout.grow_up()),
#     Key([mod, "control"], "h", lazy.layout.grow_left()),
#     Key([mod, "control"], "l", lazy.layout.grow_right()),
#     Key([mod], "n", lazy.layout.normalize()),
#     Key([mod], "m",
#         lazy.layout.maximize(),
#         desc='toggle window between minimum and maximum sizes'
#         ),
#     Key([mod], "h",
#         lazy.layout.grow(),
#         lazy.layout.increase_nmaster(),
#         desc='Expand window (MonadTall), increase number in master pane (Tile)'
#         ),
#     Key([mod], "l",
#         lazy.layout.shrink(),
#         lazy.layout.decrease_nmaster(),
#         desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
#         ),

#     # Move windows up or down in current stack
#     Key([mod, "control"], "k", lazy.layout.shuffle_down(),
#         desc="Move window down in current stack "),
#     Key([mod, "control"], "j", lazy.layout.shuffle_up(),
#         desc="Move window up in current stack "),

#     # Switch window focus to other pane(s) of stack
#     Key([mod], "space", lazy.layout.next(),
#         desc="Switch window focus to other pane(s) of stack"),

#     # Swap panes of split stack
#     Key([mod, "shift"], "space", lazy.layout.rotate(),
#         desc="Swap panes of split stack"),

#     # Toggle between split and unsplit sides of stack.
#     # Split = all windows displayed
#     # Unsplit = 1 window displayed, like Max layout, but still with
#     # multiple stack panes
#     Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
#         desc="Toggle between split and unsplit sides of stack"),
#     Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

#     # Toggle between different layouts as defined below
#     Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
#     Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

#     # Qtile system keys
#     # Key([mod, "control"], "l", lazy.spawn("betterlockscreen -l")),
#     Key([mod, "control"], "r", lazy.restart(), desc="Restart qtile"),
#     Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown qtile"),
#     Key([mod], "r", lazy.spawncmd(),
#         desc="Spawn a command using a prompt widget"),
#     Key([mod, "control"], "p",
#         lazy.spawn("rofi -show p -modi p:" + \
#                    home+"/.local/bin/rofi-power-menu -width 20 -lines 6")),

#     # Rofi
#     Key(["control"], "space", lazy.spawn("rofi -show drun")),

#     # ------------ Hardware Configs ------------
#     # Volume
#     Key([], "XF86AudioMute",
#         lazy.spawn(home + "/.local/bin/volumecontrol mute")),
#     Key([], "XF86AudioLowerVolume", lazy.spawn(
#         home + "/.local/bin/volumecontrol down")),
#     Key([], "XF86AudioRaiseVolume", lazy.spawn(
#         home + "/.local/bin/volumecontrol up")),

#     # Media keys
#     Key([], "XF86AudioPlay", lazy.spawn(
#         "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " \
#         "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.PlayPause")),
#     Key([], "XF86AudioNext", lazy.spawn(
#         "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " \
#         "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Next")),
#     Key([], "XF86AudioPrev", lazy.spawn(
#         "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " \
#         "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Previous")),

#     # Brightness
#     Key([], "F2", lazy.spawn(home + "/.local/bin/brightnesscontrol down")),
#     Key([], "F3", lazy.spawn(home + "/.local/bin/brightnesscontrol up")),

#     # Screenshot
#     # Save screen to clipboard
#     Key([], "Print", lazy.spawn("/usr/bin/escrotum -C")),
#     # Save screen to screenshots folder
#     Key([mod], "Print",
#         lazy.spawn("/usr/bin/escrotum " + home + \
#                    "/Pictures/Screenshots/screenshot_%d_%m_%Y_%H_%M_%S.png")),
#     # Capture region of screen to clipboard
#     Key([mod, "shift"], "s", lazy.spawn("/usr/bin/escrotum -Cs")),
# ]

keymap = {
    'M-q': lazy.window.kill(),

    'M-h': lazy.layout.left(),
    'M-j': lazy.layout.down(),
    'M-k': lazy.layout.up(),
    'M-l': lazy.layout.right(),

    'M-S-h': lazy.layout.move_left(),
    'M-S-j': lazy.layout.move_down(),
    'M-S-k': lazy.layout.move_up(),
    'M-S-l': lazy.layout.move_right(),

    'M-A-h': lazy.layout.integrate_left(),
    'M-A-j': lazy.layout.integrate_down(),
    'M-A-k': lazy.layout.integrate_up(),
    'M-A-l': lazy.layout.integrate_right(),

    'M-d': lazy.layout.mode_horizontal(),
    'M-v': lazy.layout.mode_vertical(),
    'M-S-d': lazy.layout.mode_horizontal_split(),
    'M-S-v': lazy.layout.mode_vertical_split(),
    'M-a': lazy.layout.grow_width(30),
    'M-x': lazy.layout.grow_width(-30),
    'M-S-a': lazy.layout.grow_height(30),
    'M-S-x': lazy.layout.grow_height(-30),
    'M-C-5': lazy.layout.size(500),
    'M-C-8': lazy.layout.size(800),
    'M-f': lazy.window.toggle_fullscreen(),
    'M-n': lazy.layout.reset_size(),
    'M-C-r': lazy.restart(),
    'M-<Return>': lazy.spawn(terminal),

    'M-C-q': lazy.spawn('gnome-session-quit --logout --no-prompt'),
    'M-S-C-q': lazy.spawn('gnome-session-quit --power-off'),
    'M-<space>': lazy.spawn('rofi -show drun'),
}

keys = [EzKey(k, v) for k, v in keymap.items()]

# Groups with matches

workspaces = [
    {"name": " Home", "key": "1", "matches": [Match(wm_class='firefox')]},
    {"name": " Dev", "key": "2", "matches": [
        Match(wm_class='geany'), Match(wm_class='vim')]},
    {"name": " Chat", "key": "3", "matches": [
        Match(wm_class='telegram-desktop')]},
    {"name": " GFX", "key": "4", "matches": [Match(wm_class='gimp')]},
    {"name": "阮 Music", "key": "5", "matches": [Match(wm_class='spotify')]},
]

groups = []
for workspace in workspaces:
    matches = workspace["matches"] if "matches" in workspace else None
    groups.append(
        Group(workspace["name"], matches=matches, layout="monadtall"))
    keys.append(Key([mod], workspace["key"],
                    lazy.group[workspace["name"]].toscreen()))
    keys.append(Key([mod, "shift"], workspace["key"],
                    lazy.window.togroup(workspace["name"])))

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 3,
                "margin": 16,
                "border_focus": BLUE,
                "border_normal": BLACK
                }

layouts = [
    Plasma(
        border_normal_fixed=BLACK,
        border_focus_fixed=CYAN,
        border_width_single=5,
        **layout_theme,
    ),
    layout.MonadTall(**layout_theme),
    layout.Stack(num_stacks=2, **layout_theme),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    layout.Bsp(**layout_theme),
    # layout.Columns(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='FantasqueSansMono Nerd Font',
    fontsize=14,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=10),
                widget.CurrentLayoutIcon(scale=0.7),
                widget.CurrentLayout(**widget_defaults),
                widget.GroupBox(borderwidth=2,
                                inactive='969696',
                                this_current_screen_border='eee8d5',
                                this_screen_border='eee8d5',
                                **widget_defaults),
                widget.Prompt(**widget_defaults),
                widget.Spacer(),
                widget.CheckUpdates(
                    **widget_defaults,
                    update_interval=1800,
                    distro='Arch_yay',
                    custom_command='checkupdates+aur',
                    display_format=' {updates}',
                    colour_have_updates=GREEN,
                    execute='kitty -e yay -Syu',
                ),
                widget.Mpris2(
                    name='spotify',
                    objname="org.mpris.MediaPlayer2.spotify",
                    display_metadata=['xesam:title', 'xesam:artist'],
                    scroll_chars=None,
                    stop_pause_text='',
                    **widget_defaults
                ),
                widget.BatteryIcon(
                ),
                widget.Battery(
                    charge_char='+',
                    discharge_char='',
                    unknown_char='',
                    format='{char}{percent:2.0%}',
                    **widget_defaults,
                ),
                widget.Volume(emoji=True),
                widget.Volume(**widget_defaults),
                widget.Systray(),
                widget.Spacer(length=10),
                widget.GenPollText(
                    func=custom_date, update_interval=1, **widget_defaults),
                widget.Clock(
                    **widget_defaults,
                    format='%H:%M'
                ),
                widget.Spacer(length=10),
            ],
            24, margin=[10, 16, 0, 16]  # N E S W
        ),
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    Match(title='Quit and close tabs?'),
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='Conky'),
    # Match(wm_class='Firefox'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
