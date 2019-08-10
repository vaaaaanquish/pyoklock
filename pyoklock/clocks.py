from datetime import datetime as dt
import numpy as np
from prompt_toolkit.formatted_text import FormattedText
import os

background_char = os.getenv('PYOKLOCK_BACK_CHAR', ' ')
background_char = ' ' if not background_char else background_char
digit_char = os.getenv('PYOKLOCK_DIGIT_CHAR', '\u2588')
digit_char = '\u2588' if not digit_char else digit_char


class BigClock:
    """----------------------------[BigClock 80 * 14 image]--------------------------
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
    ------------------------------------------------------------------------------"""
    def __init__(self, sec=False, color=False, gcalender=None):
        self.sec = sec
        self.color = color
        self.gcalender = gcalender

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

        t = '\n'.join([''.join(x) for x in clock])
        # 5 min bofore, 15 min after events
        if self.color:
            b_event = []
            a_event = []
            for x in self.gcalender.events:
                if x['month'] == now.month and x['day'] == now.day and x['hour'] is not None:
                    d = (x['hour'] * 60 + x['minute']) - (now.hour * 60 + now.minute)
                    if d <= 5 and d > 0:
                        b_event.append(x)
                    if d <= 0 and d >= -15:
                        a_event.append(x)

            if b_event:
                return FormattedText([('#FF0000', t)])
            if a_event:
                return FormattedText([('#008000', t)])
        return t

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


class SmallClock:
    """------------[SmallClock 53 * 9 image]-------------
    #####################################################
    #         ###         #########         ###         #
    #  #####  ###  #####  ###   ###  #####  ###  #####  #
    #  #####  ###  #####  ###   ###  #####  ###  #####  #
    #         ###         #########         ###         #
    #  #####  ###  #####  ###   ###  #####  ###  #####  #
    #  #####  ###  #####  ###   ###  #####  ###  #####  #
    #         ###         #########         ###         #
    #####################################################
    --------------------------------------------------"""
    def __init__(self, sec=False, color=False, gcalender=None):
        self.sec = sec
        self.color = color
        self.gcalender = gcalender

    def get_clock(self):
        """make clock text"""
        if self.sec:
            clock = np.array([[background_char] * 83] * 9)
        else:
            clock = np.array([[background_char] * 53] * 9)
        now = dt.now()
        clock[1:8, 1:10] = self.get_number(now.hour // 10)
        clock[1:8, 13:22] = self.get_number(now.hour % 10)
        clock[1:8, 23:29] = self.get_coron()
        clock[1:8, 31:40] = self.get_number(now.minute // 10)
        clock[1:8, 43:52] = self.get_number(now.minute % 10)
        if self.sec:
            clock[1:8, 53:59] = self.get_coron()
            clock[1:8, 61:70] = self.get_number(now.second // 10)
            clock[1:8, 73:82] = self.get_number(now.second % 10)

        t = '\n'.join([''.join(x) for x in clock])
        # 5 min bofore, 15 min after events
        if self.color:
            b_event = []
            a_event = []
            for x in self.gcalender.events:
                if x['month'] == now.month and x['day'] == now.day and x['hour'] is not None:
                    d = (x['hour'] * 60 + x['minute']) - (now.hour * 60 + now.minute)
                    if d <= 5 and d > 0:
                        b_event.append(x)
                    if d <= 0 and d >= -15:
                        a_event.append(x)

            if b_event:
                return FormattedText([('#FF0000', t)])
        return t

    def get_coron(self):
        """make coron ndarray"""
        n = np.array([[background_char] * 6] * 7)
        n[2:3, 2:5] = digit_char
        n[4:5, 2:5] = digit_char
        return n

    def get_number(self, num):
        """make number ndarray"""
        n = np.array([[digit_char] * 9] * 7)
        if num == 0:
            n[1:6, 2:7] = background_char
        if num == 1:
            n[0:7, 0:7] = background_char
        if num == 2:
            n[1:3, 0:7] = background_char
            n[4:6, 2:9] = background_char
        if num == 3:
            n[1:3, 0:7] = background_char
            n[4:6, 0:7] = background_char
        if num == 4:
            n[0:3, 2:7] = background_char
            n[4:7, 0:7] = background_char
        if num == 5:
            n[1:3, 2:9] = background_char
            n[4:6, 0:7] = background_char
        if num == 6:
            n[1:3, 2:9] = background_char
            n[4:6, 2:7] = background_char
        if num == 7:
            n[1:7, 0:7] = background_char
        if num == 8:
            n[1:3, 2:7] = background_char
            n[4:6, 2:7] = background_char
        if num == 9:
            n[1:3, 2:7] = background_char
            n[4:6, 0:7] = background_char
        return n


class MinimumClock:
    """---[MinimumClock 36 * 7 image]---
    ####################################
    #      ##      ######      ##      #
    #  ##  ##  ##  ##  ##  ##  ##  ##  #
    #      ##      ######      ##      #
    #  ##  ##  ##  ##  ##  ##  ##  ##  #
    #      ##      ######      ##      #
    ####################################
    ---------------------------------"""
    def __init__(self, sec=False, color=False, gcalender=None):
        self.sec = sec
        self.color = color
        self.gcalender = gcalender

    def get_clock(self):
        """make clock text"""
        if self.sec:
            clock = np.array([[background_char] * 55] * 7)
        else:
            clock = np.array([[background_char] * 36] * 7)
        now = dt.now()
        clock[1:6, 1:7] = self.get_number(now.hour // 10)
        clock[1:6, 9:15] = self.get_number(now.hour % 10)
        clock[1:6, 16:20] = self.get_coron()
        clock[1:6, 21:27] = self.get_number(now.minute // 10)
        clock[1:6, 29:35] = self.get_number(now.minute % 10)
        if self.sec:
            clock[1:6, 36:40] = self.get_coron()
            clock[1:6, 41:47] = self.get_number(now.second // 10)
            clock[1:6, 49:55] = self.get_number(now.second % 10)

        t = '\n'.join([''.join(x) for x in clock])
        # 5 min bofore, 15 min after events
        if self.color:
            b_event = []
            a_event = []
            for x in self.gcalender.events:
                if x['month'] == now.month and x['day'] == now.day and x['hour'] is not None:
                    d = (x['hour'] * 60 + x['minute']) - (now.hour * 60 + now.minute)
                    if d <= 5 and d > 0:
                        b_event.append(x)
                    if d <= 0 and d >= -15:
                        a_event.append(x)

            if b_event:
                return FormattedText([('#FF0000', t)])
        return t

    def get_coron(self):
        """make coron ndarray"""
        n = np.array([[background_char] * 4] * 5)
        n[1, 1:3] = digit_char
        n[3, 1:3] = digit_char
        return n

    def get_number(self, num):
        """make number ndarray"""
        n = np.array([[digit_char] * 6] * 5)
        if num == 0:
            n[1:4, 2:4] = background_char
        if num == 1:
            n[0:5, 0:4] = background_char
        if num == 2:
            n[1, 0:4] = background_char
            n[3, 2:6] = background_char
        if num == 3:
            n[1, 0:4] = background_char
            n[3, 0:4] = background_char
        if num == 4:
            n[0:2, 2:4] = background_char
            n[3:5, 0:4] = background_char
        if num == 5:
            n[1, 2:6] = background_char
            n[3, 0:4] = background_char
        if num == 6:
            n[1, 2:6] = background_char
            n[3, 2:4] = background_char
        if num == 7:
            n[1:5, 0:4] = background_char
        if num == 8:
            n[1, 2:4] = background_char
            n[3, 2:4] = background_char
        if num == 9:
            n[1, 2:4] = background_char
            n[3, 0:4] = background_char
        return n
