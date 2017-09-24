# MacRC
Control your Mac with an Arduino and an infrared remote control

## Introduction
This is a simple project which lets you control your Mac with a standard infrared remote control. You can control the volume, mute and
unmute and jump between tracks in iTunes - and it's quite easy to modify or extend the tasks you can control.
Perfect if you abuse your iMac as a TV or media center from time to time...
The way it works is with an IR receiver connected to an Arduino board, which sends commands to a Python script
running as a background task, which in turn mostly uses AppleScript commands. I've come across several projects and libraries similar to
this project, but I could get none of them to work on OSX, so I ended up making my own.

## Getting started
### Arduino + IR receiver
This project uses [IRLib2](https://github.com/cyborg5/IRLib2/tree/master/IRLib2), which you need to install in your Arduino folder.
Now, simply use the Arduino software to upload the sketch to your board.
I'm using an Arduino Uno together with an AD22100KT IR receiver, although I believe most other Arduino boards should work as well, and
using a different receiver should only need minimal changes in the code. For the AD22100KT, it is possible to plug directly into IO pins
2, 3 and 4, where 2 is the signal output and 4 is the input voltage. For other receivers, please refer to the data sheet and modify the code
accordingly.

The next important point is the remote control protocol. One can modify the sketch to include a different protocol by
changing the line
```Arduino
#include <IRLib_P03_RC5.h>
```
On the other hand, with a universal remote control, one could also try the different settings for Philips TVs, one of which should be
compatible with this sketch. Depending on the remote control, it might be necessary to switch the command numbers in the sketch. In order
to do this, you should enable the line
```Arduino
//Serial.println(command);
```
and use Serial Monitor in order to see which commands are received.

To make matters more complicated, note that not all IR receivers are compatible with all protocols; be sure to research the topic before
buying a remote or an IR receiver.

## Python script
The recommended location for the MacRC folder is the home directory. Although OSX comes with Python pre-installed, it is usually not
a good idea to modify it, so I would recommend using [Anaconda](https://www.anaconda.com/download/). Python 3.5 or 3.6 should work, I have
not tested other version. The `serial` package is required, which can be installed with Anaconda by opening a terminal and typing
```bash
conda install serial
```
Before you start the background task, it is highly recommended to test out the script in a terminal window. In order to get detailed output,
type
```bash
python macRC.pyw -v
```
You should see how Python connects to the Arduino and prints the commands it receives. In case the connection is lost, i.e. if a cable is 
unplugged, the script will try to re-establish the connection - feel free to try it out as well.

If the script is running well in the terminal window, it' time to intall the background task. Check `macRC.plist` to make shure that the
directories to your Python interpreter and to the Python script are correct. Then, copy it to the following location:
```
<your-home-folder>/Library/LaunchAgents/
```
You will need to log out and back in, afterwards it should work! If the background task is giving you any kind of trouble, I recommend
getting [LaunchControl](http://www.soma-zone.com/LaunchControl/) to figure it out.

Happy remote-controlling :smile:
