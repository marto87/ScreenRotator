#! /usr/bin/env python3

import os
import signal
from subprocess import call
from gi.repository import Gtk
from gi.repository import AppIndicator3 as AppIndicator

APPINDICATOR_ID = "screenrotator"
orientation = "left"

def main():
    global indicator
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('./icon.svg'), AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_label("Horizontal", "Horizontal")
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Gtk.main()

def build_menu():
    menu = Gtk.Menu()
    #rotate
    item_rotate = Gtk.MenuItem('Rotar pantalla')
    item_rotate.connect('activate', rotate_screen)
    menu.append(item_rotate)
    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)
    #quit
    item_quit = Gtk.MenuItem('Cerrar')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def rotate_screen(source):
    global orientation
    if orientation == "normal":
        indicator.set_label("Vertical", "Horizontal")
        source.set_label("Rotar pantalla (Vertical)")
        direction = "left"
    elif orientation == "left":
        indicator.set_label("Horizontal", "Horizontal")
        source.set_label("Rotar pantalla (Horizontal)")
        direction ="normal"
    call(["xrandr", "-o", direction])
    orientation = direction

if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    call(["xrandr", "-o", orientation])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
