#!/usr/bin/env python

from os.path import join

import os, sys
import subprocess

MOD_ADDR="http://127.0.0.1:7988"

DATA_DIR = join(os.environ['HOME'], '.mod-lv2-host/data')

os.environ['MOD_DEV_HOST'] = "0"
os.environ['MOD_DEV_HMI'] = "1"
os.environ['MOD_DATA_DIR'] = DATA_DIR
os.environ['MOD_DESKTOP'] = "1"
os.environ['MOD_LOG'] = "0"
os.environ['MOD_HTML_DIR'] = join(".", 'html')
os.environ['MOD_DEVICE_WEBSERVER_PORT'] = '7988'
os.environ['MOD_PHANTOM_BINARY'] = join(".", 'phantomjs-1.9.0-linux-x86_64/bin/phantomjs')
os.environ['MOD_SCREENSHOT_JS'] = join(".", 'screenshot.js')

#sys.path = sys.path

if len(sys.argv) > 1 and sys.argv[1] == "--scan-lv2":
    from mod import rebuild_database
    rebuild_database()
    sys.exit(0)

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
os.system("./mod-host/mod-host")
p = Process(target=webserver.run)
p.start()

# start a PyQt webkit
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

app = QApplication(sys.argv)
web = QWebView()
web.load(QUrl(MOD_ADDR))
web.show()
sys.exit(app.exec_())
