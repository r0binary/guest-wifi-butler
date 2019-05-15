# Guest WiFi Butler [![Build Status](https://travis-ci.com/r0binary/guest-wifi-butler.svg?branch=master)](https://travis-ci.com/r0binary/guest-wifi-butler)

This project turns a Raspberry Pi with WiFi adapter and attached touchscreen into a WiFi access
point. It is based on an idea from the german IT magazine c't. Your guests can easily connect to the
WiFi by scanning a QR code. It is regenerated every day to ensure your guests do not have unlimited
access. When the device is not requested to show the WiFi QR codes it turns into a digital photo
frame that show a slideshow of your favorite photographs.

## Build

    python setup.py sdist bdist_wheel

## Installation

The following instructions are copied from the [Kivy
installation guide for Raspberry Pi](https://kivy.org/docs/installation/installation-rpi.html).

    sudo pip install -U Cython==0.28.2
    sudo pip install git+https://github.com/kivy/kivy.git@master

And finally we need to install the `guest_wifi_butler` package

    sudo pip install guest_wifi_butler-X.X.X.tar.gz

## Enable Raspberry Pi Touchscreen

By default Kivy will not work properly with the Raspberry Pi's touchscreen.
To change that add these lines to `~/.kivy/config.ini` into input section

    mouse = mouse
    mtdev_%(name)s = probesysfs,provider=mtdev
    hid_%(name)s = probesysfs,provider=hidinput

The config is the one of the non-root user e.g. `pi`, so in this case it 
would be `/home/pi/.kivy/config.ini`.

## Configuration

### Force the screen to stay on

To force the Raspberry Pi's screen to stay on, adjust LightDM's
configuration like this:

    sudo nano /etc/lightdm/lightdm.conf

Add the following line to the `[SeatDefaults]` section:

    xserver-command=X -s 0 dpms

### Access Point configuration

In order to let bridged IP and ARP packets pass the access point, it is
required to set the following sysctl variables either manually or persistent
in `/etc/sysctl.conf`:

    net.bridge.bridge-nf-call-iptables=0
    net.bridge.bridge-nf-call-arptables=0
    net.bridge.bridge-nf-call-ip6tables=0

### Autostart on Boot

To automatically start the guest wifi butler on Raspian startup create a file `~/.config/autostart/guest_wifi_butler.desktop` with the following content: 

    [Desktop Entry]
    Encoding=UTF-8
    Type=Application
    Name=Guest WiFi Butler
    Exec=sudo butler
    StartupNotify=false
    Hidden=false

Once you reboot Raspian it will show the wifi butler after a few seconds.

## Development guide

Any help for this project will be appreciated. You can contribute through
bug reports, ideas for new features or own pull requests. To make sure you
did not break anything, you can run the (by far not complete) test suite.

### Runs Tests

    pytest guest_wifi_butler\test

### Code Coverage

    pytest --cov=guest_wifi_butler guest_wifi_butler\test