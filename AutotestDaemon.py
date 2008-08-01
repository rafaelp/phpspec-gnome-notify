#!/usr/bin/env python  
# coding: utf-8  
# monitor.py 20071108 AF  
   
import os, sys, re
from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes  

PHPSpecGnomeNotify = os.path.dirname(__file__)+"/PHPSpecGnomeNotify.php"

wm = WatchManager()

def Monitor():  
    class close_event(ProcessEvent):  
        def process_IN_CLOSE(self, event):  
            f = event.name and os.path.join(event.path, event.name) or event.path  
            if re.compile('Describe(.*)\.php$').search(f, 1):
              os.system(PHPSpecGnomeNotify)
  
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
        print 'use: %s diretório' % sys.argv[0]  
        sys.exit(1)  
  
    for path in dirlist:  
        os.chdir(path)
        wm.add_watch(path, EventsCodes.IN_CLOSE_WRITE, rec=True)  
  
    Monitor()
