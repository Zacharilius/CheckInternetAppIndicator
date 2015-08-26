import os
import signal
import json
import time

import urllib2

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'InternetChecker'
cont = True;

def main():
    myIndicator = appindicator.Indicator.new(APPINDICATOR_ID, gtk.STOCK_NETWORK, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    myIndicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    myIndicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()

    # Checks Internet Connectivity Once
    option_checkOnce = gtk.MenuItem('Check Once')
    option_checkOnce.connect('activate', check_once)
    menu.append(option_checkOnce)

    # Notify when Internet Connectivity is available
    option_checkUntil = gtk.MenuItem('Check Until...')
    option_checkUntil.connect('activate', notify_when_on)
    menu.append(option_checkUntil)

    # Adds the ability to stop
    option_stopCheck = gtk.MenuItem('Stop Checking')
    option_stopCheck.connect('activate', stop_checking)
    menu.append(option_stopCheck)

    # Adds the ability to quit
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    # Shows the menu
    menu.show_all()
    return menu
def check_connectivity():
    try:
        response=urllib2.urlopen('http://74.125.224.72/',timeout=1)
        return "on"
    except urllib2.URLError as err: pass
    return "off"

def check_once(_):
    notify.Notification.new("The Internet is ", check_connectivity(), None).show()

def notify_when_on(_):
    # Resets the cont variable to true
    global cont
    cont = True

    # Loops until internet status is connected
    internet_status = ""
    while(internet_status != "on" and cont):
        internet_status = check_connectivity()
        print internet_status
        time.sleep(5)
    # Sends a notifcation that the Internet is back on.
    notify.Notification.new("The Internet is ", check_connectivity(), None).show()


def stop_checking(_):
    global cont
    print  cont
    cont = False
    print  cont


def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
