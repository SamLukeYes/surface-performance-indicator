#!/usr/bin/python3

# Copyright (C) 2021  Sam L. Yes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pystray
import os
from threading import Thread
from PIL import Image, ImageDraw
from time import sleep

modes = {
    'Normal': (1, (255, 255, 255)), # white
    'Better Performance': (3, (0, 255, 0)), # green
    'Best Performance': (4, (50, 150, 255)), # blue
}

cli = '/usr/bin/surface'

def mode_detect() -> str:
    with os.popen(f'{cli} performance get') as stdout:
        output = stdout.read()
    for mode in modes.keys():
        if mode in output:
            return mode
    # if fail, notify and quit
    os.system("notify-send -u critical 'Surface Performance' 'Failed to get current performance mode'")
    exit(1)

class indicator:

    def __init__(self):

        self.items = dict()
        for mode in modes.keys():
            self.items[mode] = pystray.MenuItem(mode, self.trigger, checked=self.check)

        self.icon = pystray.Icon(
            'Surface Performance', 
            menu = pystray.Menu(
                pystray.MenuItem(
                    'Performance',
                    pystray.Menu(
                        *self.items.values()
                    )
                    ),
                pystray.MenuItem(
                    'Quit', self.stop
                )
            )
        )
        self.daemon = Thread(target=self.refresh)
        self.mode = None

    def check(self, item):
        if self.items[self.mode] == item:
            return True
        return False

    def trigger(self, icon, item):
        target = item.text
        command = f'{cli} performance set {modes[target][0]}'
        code = os.system(command)
        if code:
            self.icon.notify(f"Error! surface-control returned code {code}", 'Surface Performance Indicator')
        #self.update_icon()

    def update_icon(self, mode):
        image = Image.new('RGB', (17, 17))
        draw = ImageDraw.Draw(image)
        for x, y in ((0, 0), (0, 9), (9, 0), (9, 9)):
            draw.rectangle((x, y, x+7, y+7), fill=modes[mode][1])
        self.icon.icon = image

    def refresh(self):
        while self.running:
            mode = mode_detect()
            if self.mode != mode:
                self.mode = mode
                self.update_icon(mode)
                self.icon.update_menu()
                sleep(1)

    def start(self):
        self.running = True
        self.daemon.start()
        sleep(1)
        self.icon.run()

    def stop(self):
        self.running = False
        self.icon.stop()

if __name__ == '__main__':
    indicator().start()