mod-client
==========

Instructions to run the MOD LV2 Host on any GNU/Linux

Make sure you have Python 2.7 and PyQt4 installed:

On Debian:
$ apt-get install python-qt4

On ArchLinux:
$ pacman -S python2-pyqt4

$ git clone --recursive http://github.com/portalmod/mod-client
$ cd mod-client

Debian users:
$ virtualenv env
$ ln -s /usr/lib/python2.7/dist-packages/PyQt4 env/lib/python2.7/site-packages/
$ ln -s /usr/lib/python2.7/dist-packages/sip.so env/lib/python2.7/site-packages/

ArchLinux users:
$ virtualenv2 env
$ ln -s /usr/lib/python2.7/site-packages/PyQt4 env/lib/python2.7/site-packages/
$ ln -s /usr/lib/python2.7/site-packages/sip.so env/lib/python2.7/site-packages/

$ . env/bin/activate
$ pip install -e requirements.txt --allow-unverified PIL --allow-external PIL
$ cd mod-ui/
$ python setup.py install
$ cd ..
$ cd mod-host
$ make
$ cd ..
$ ./mod-lv2-host.py --scan-lv2
This may take some time, while MOD software indexes information about your LV2 plugins

$ ./mod-lv2-host.py
