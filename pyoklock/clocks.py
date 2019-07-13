from datetime import datetime as dt
import numpy as np

"----------------------------[BigClock 80 * 14 image]--------------------------"
################################################################################
#               ####               ##########               ####               #
#               ####               ##########               ####               #
#    #######    ####    #######    ###    ###    #######    ####    #######    #
#    #######    ####    #######    ###    ###    #######    ####    #######    #
#    #######    ####    #######    ##########    #######    ####    #######    #
#               ####               ##########               ####               #
#               ####               ##########               ####               #
#    #######    ####    #######    ##########    #######    ####    #######    #
#    #######    ####    #######    ###    ###    #######    ####    #######    #
#    #######    ####    #######    ###    ###    #######    ####    #######    #
#               ####               ##########               ####               #
#               ####               ##########               ####               #
################################################################################
"------------------------------------------------------------------------------"
background_char = ' '
digit_char = '\u2588'


class BigClock:
    def __init__(self, sec):
        self.sec = sec

    def get_clock(self):
        """make clock text"""
        if self.sec:
            clock = np.array([[background_char] * 124] * 14)
        else:
            clock = np.array([[background_char] * 80] * 14)
        now = dt.now()
        clock[1:13, 1:16] = self.get_number(now.hour // 10)
        clock[1:13, 20:35] = self.get_number(now.hour % 10)
        clock[1:13, 36:43] = self.get_coron()
        clock[1:13, 45:60] = self.get_number(now.minute // 10)
        clock[1:13, 64:79] = self.get_number(now.minute % 10)
        if self.sec:
            clock[1:13, 80:87] = self.get_coron()
            clock[1:13, 89:104] = self.get_number(now.second // 10)
            clock[1:13, 108:123] = self.get_number(now.second % 10)
        return '\n'.join([''.join(x) for x in clock])

    def get_coron(self):
        """make coron ndarray"""
        n = np.array([[background_char] * 7] * 12)
        n[2:4, 2:6] = digit_char
        n[8:10, 2:6] = digit_char
        return n

    def get_number(self, num):
        """make number ndarray"""
        n = np.array([[digit_char] * 15] * 12)
        if num == 0:
            n[2:10, 4:11] = background_char
        if num == 1:
            n[0:12, 0:11] = background_char
        if num == 2:
            n[2:5, 0:11] = background_char
            n[7:10, 4:15] = background_char
        if num == 3:
            n[2:5, 0:11] = background_char
            n[7:10, 0:11] = background_char
        if num == 4:
            n[0:5, 4:11] = background_char
            n[7:12, 0:11] = background_char
        if num == 5:
            n[2:5, 4:15] = background_char
            n[7:10, 0:11] = background_char
        if num == 6:
            n[2:5, 4:15] = background_char
            n[7:10, 4:11] = background_char
        if num == 7:
            n[2:12, 0:11] = background_char
        if num == 8:
            n[2:5, 4:11] = background_char
            n[7:10, 4:11] = background_char
        if num == 9:
            n[2:5, 4:11] = background_char
            n[7:10, 0:11] = background_char
        return n
