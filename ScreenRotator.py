#! /usr/bin/env python3

import os
import signal
from subprocess import call
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

APPINDICATOR_ID = "screenrotator"
orientation = "right"

def main():
    global indicator
    script_path = os.path.dirname(os.path.realpath(__file__))
    icon_path = script_path + '/icon.svg'
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, icon_path, AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_label("Horizontal", "Horizontal")
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Gtk.main()

def build_menu():
    menu = Gtk.Menu()
    #rotate
    item_rotate = Gtk.MenuItem(label='Rotar pantalla')
    item_rotate.connect('activate', rotate_screen)
    menu.append(item_rotate)
    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)
    #quit
    item_quit = Gtk.MenuItem(label='Cerrar')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def rotate_screen(source):
    global orientation
    if orientation == "right":
        indicator.set_label("Vertical", "Horizontal")
        direction = "normal"
    elif orientation == "normal":
        indicator.set_label("Horizontal", "Horizontal")
        direction ="right"
    call(["xrandr", "-o", direction])
    orientation = direction

if __name__ == "__main__":
    #make sure the screen is in "right" orientation when the script starts
    call(["xrandr", "-o", orientation])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
