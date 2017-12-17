"""Module handling writing to the screen."""

import logging

from constants import DIR_TO_CHAR

from Adafruit_CharLCD import Adafruit_CharLCD

logger = logging.getLogger(__name__)


class ScreenWriter(object):
    """docstring for ScreenWriter."""

    def __init__(self, rs, en, d4, d5, d6, d7):
        """Config."""
        self.columns = 16
        self.lines = 1
        self.lcd = Adafruit_CharLCD(rs, en, d4, d5, d6, d7,
                                    self.columns, self.lines)

    def _direction_to_char(self, dir):
        return DIR_TO_CHAR[dir]

    def write_to_lcd(self, value, dir):
        """Write out to lcd."""
        self.lcd.clear()
        self.lcd.message(str(value))
        self.lcd.message(self._direction_to_char(dir))
