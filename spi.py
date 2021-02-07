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
from PIL import Image, ImageDraw

modes = {
    'Normal': (1, (255, 255, 255)), # white
    'Better Performance': (3, (0, 255, 0)), # green
    'Best Performance': (4, (50, 150, 255)), # blue
}

cli = '/usr/bin/surface'

class indicator:

    def __init__(self):

        self.mode_detect()
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
        self.update_icon()

    def mode_detect(self):
        with os.popen(f'{cli} performance get') as stdout:
            output = stdout.read()
        for mode in modes.keys():
            if mode in output:
                self.mode = mode
                return
        # if fail, notify and quit
        os.system("notify-send -u critical 'Surface Performance' 'Failed to get current performance mode'")
        exit(1)

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
        self.mode_detect()
        self.update_icon()

    def update_icon(self):
        image = Image.new('RGB', (17, 17))
        draw = ImageDraw.Draw(image)
        for x, y in ((0, 0), (0, 9), (9, 0), (9, 9)):
            draw.rectangle((x, y, x+7, y+7), fill=modes[self.mode][1])
        self.icon.icon = image

    def stop(self):
        self.icon.stop()

if __name__ == '__main__':
    app = indicator()
    app.icon.run()