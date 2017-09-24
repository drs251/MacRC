from subprocess import Popen, PIPE
from distutils.util import strtobool
import serial
import sys
import time
import glob
import serial.tools.list_ports_posix


def run_applescript(scpt, args=()):
    p = Popen(['osascript', '-'] + list(args), stdin=PIPE, stdout=PIPE)
    stdout, stderr = p.communicate(scpt)
    return stdout


def toggle_mute():
    set_mute_script = b'''
        on run {x}
            set volume output muted x
        end run'''

    get_mute_script = b'''output muted of (get volume settings)'''

    mute_status = strtobool(run_applescript(get_mute_script).strip().decode())
    run_applescript(set_mute_script, [str(not mute_status)])


get_volume_script = b'''output volume of (get volume settings)'''
set_volume_script = b'''
    on run {x}
        set volume output volume x
    end run'''
volume_increment = 6


def increase_volume():
    volume = int(run_applescript(get_volume_script))
    volume += 6
    run_applescript(set_volume_script, [str(volume)])


def decrease_volume():
    volume = int(run_applescript(get_volume_script))
    volume -= 6
    run_applescript(set_volume_script, [str(volume)])


def pause_itunes():
    pause_itunes_script = b'''
        tell application "iTunes"
        pause
        end tell'''
    run_applescript(pause_itunes_script)


def play_itunes():
    play_itunes_script = b'''
        tell application "iTunes"
        play
        end tell'''
    run_applescript(play_itunes_script)


def next_track_itunes():
    next_track_itunes_script = b'''
        tell application "iTunes"
        next track
        end tell'''
    run_applescript(next_track_itunes_script)


def previous_track_itunes():
    next_track_itunes_script = b'''
        tell application "iTunes"
        previous track
        end tell'''
    run_applescript(next_track_itunes_script)


def connect_arduino():
    # find the arduino:
    portlist = glob.glob('/dev/tty.usbmodem*')
    for port in portlist:
        try:
            ser = serial.Serial(port=port, baudrate=9600, timeout=1)
        except Exception:
            continue
        else:
            break
    else:
        raise IOError("Arduino not found")
    return ser


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-v":
        # print some extra information (useful for troubleshooting)
        verbose = True
    else:
        verbose = False

    error = False
    try:
        ser = connect_arduino()
        if verbose:
            print("Connected to Arduino.")
    except Exception as err:
        error = True
        if verbose:
            print("Encountered Exception while connecting: {0}".format(err))

    while True:
        if not error:
            try:
                res = ser.readline().strip().decode()
                if verbose and res != '':
                    print("Got command " + str(res))
                if res == 'L':
                    increase_volume()
                elif res == 'S':
                    decrease_volume()
                elif res == 'M':
                    toggle_mute()
                elif res == 'N':
                    next_track_itunes()
                elif res == 'B':
                    previous_track_itunes()
                elif res == 'P':
                    play_itunes()
                elif res == 'H':
                    pause_itunes()
                elif verbose and res != '':
                    print("Unknown command: ", res)
            except Exception as err:
                error = True
                if verbose:
                    print("Encountered {0} in main loop: {1}".format(err.__class__.__name__, err))

        # try to reconnect to Arduino if connection is lost
        if error:
            time.sleep(5)
            try:
                ser = connect_arduino()
                error = False
                if verbose:
                    print("Reconnected to Arduino.")
            except Exception as err:
                error = True
                if verbose:
                    print("Reconnect failed.")
