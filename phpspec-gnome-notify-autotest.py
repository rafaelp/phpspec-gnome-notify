#!/usr/bin/env python  
#encoding: utf-8
# phpspec-gnome-notify v0.1.1
# Rafael Lima (http://rafael.adm.br) at Myfreecomm (http://myfreecomm.com.br)
# http://rafael.adm.br/phpspec-gnome-notify
# License: http://creativecommons.org/licenses/by/2.5/

# Dependencies:

# * pyinotify
#  sudo apt-get install python-pyinotify

import os, sys, re
from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes  

PHPSpecGnomeNotify = os.getcwd()+'/'+os.path.dirname(__file__)+"/phpspec-gnome-notify.php"

wm = WatchManager()

def Monitor():  
    class close_event(ProcessEvent):  
        def process_IN_CLOSE(self, event):  
            f = event.name and os.path.join(event.path, event.name) or event.path  
            if re.compile('(.*)\.php$').search(f, 1):
              output = os.popen(PHPSpecGnomeNotify).read()
              print output

    notifier = Notifier(wm, close_event())  
  
    try:  
        while 1:  
            notifier.process_events()  
            if notifier.check_events():  
                notifier.read_events()  
    except KeyboardInterrupt:  
        notifier.stop()  
        return  
  
if __name__ == '__main__':  
    try:  
        dirlist = sys.argv[1:]  
        if not len(dirlist): raise Exception  
    except:  
        print 'use: %s [path]' % sys.argv[0]
        sys.exit(1)  
  
    for path in dirlist:  
        os.chdir(os.getcwd()+'/'+path)
        print 'monitoring %s' % os.getcwd()
        wm.add_watch(os.getcwd(), EventsCodes.IN_CLOSE_WRITE, rec=True)  
  
    Monitor()
