from subprocess import PIPE, Popen
from pyautogui import write, keyUp
import requests
import re


def get_window_name():
    root = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)
    stdout, stderr = root.communicate()
    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    window_id = m.group(1)
    window = Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=PIPE)
    stdout, stderr = window.communicate()
    wmatch = re.match(b'WM_NAME\(\w+\) = (?P<name>.+)$', stdout)
    window_name = wmatch.group('name').decode('UTF-8').strip('"')
    return window_name


def main():
    window_name = get_window_name()
    if "Twitch" in window_name and "Firefox" in window_name:
        streamer = window_name.split(" ")[0]
        response = requests.get("http://127.0.0.1:6942",
                                params={"streamer": streamer})
        prefix = response.text
        keyUp("winleft")
        write(prefix)
    else:
        print("No stream!")


if __name__ == "__main__":
    main()
