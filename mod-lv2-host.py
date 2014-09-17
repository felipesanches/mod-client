#!/usr/bin/env python

from os.path import join, realpath

import os, sys
import subprocess

MOD_ADDR="http://127.0.0.1:7988"

ROOT = os.path.dirname(realpath(sys.argv[0]))

DATA_DIR = join(ROOT, 'data')

os.environ['MOD_DEV_HOST'] = "0"
os.environ['MOD_DEV_HMI'] = "1"
os.environ['MOD_DATA_DIR'] = DATA_DIR
os.environ['MOD_DESKTOP'] = "1"
os.environ['MOD_LOG'] = "0"
os.environ['MOD_HTML_DIR'] = join(ROOT, 'mod-ui/html')
os.environ['MOD_PLUGIN_LIBRARY_DIR'] = join(os.environ['HOME'], ".lv2")
os.environ['MOD_DEVICE_WEBSERVER_PORT'] = '7988'
os.environ['MOD_PHANTOM_BINARY'] = join(ROOT, 'phantomjs-1.9.0-linux-x86_64/bin/phantomjs')
os.environ['MOD_SCREENSHOT_JS'] = join(ROOT, 'screenshot.js')

if len(sys.argv) > 1:
    if sys.argv[1] == "--scan-lv2":
        print "Scanning and indexing your LV2 plugins...",
        from mod import rebuild_database
        rebuild_database()
        print "done"
        sys.exit(0)
    else:
        print "Usage: %s [--scan-lv2]" % sys.argv[0]
        sys.exit(2)

def jack_not_running():
    p = subprocess.Popen(['jack_wait', '-c'], stdout=subprocess.PIPE)
    p.wait()
    return "not running" in p.stdout.read()

if jack_not_running():
    print "can't connect to jackd, is it running?"
    sys.exit(1)

from mod import webserver
from multiprocessing import Process

# run mod-ui and mod-host
host = subprocess.Popen([join(ROOT, "mod-host/mod-host")])
ui = Process(target=webserver.run)
ui.start()

# start a PyQt webkit
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl(MOD_ADDR))
web.show()
r = app.exec_()
ui.terminate()
host.kill()
os.system("pkill mod-host")
sys.exit(r)
