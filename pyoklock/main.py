from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.layout.dimension import to_dimension
from prompt_toolkit.layout.containers import VSplit, HSplit
import argparse
import sys
import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir))
from clocks import BigClock, SmallClock, MinimumClock
from google_calender import GCalender

parser = argparse.ArgumentParser()
parser.add_argument('--events', type=int, default=10, help='recently events num')
parser.add_argument('--model', type=int, default=1, help='size (0,1,2)')
parser.add_argument('-s', '--second', action='store_true', help='print second')
parser.add_argument('-f', '--frame', action='store_true', help='print frame')
parser.add_argument('-c', '--color', action='store_true', help='print 5min red, 15min green color')
parser.add_argument('-t', '--today', action='store_true', help='print today event only')
parser.add_argument('-g', '--google_calender', action='store_true', help='print google calender')


def make_app(sec, width, height, frame=True, gcalender=None, color=False):
    """make auto refresh application class"""
    kb = KeyBindings()

    @kb.add('c-c')
    def _(event):
        event.app.exit()

    def _vsplit(padding, m):
        return VSplit([Window(width=padding, always_hide_cursor=True), m, Window(width=padding, always_hide_cursor=True)])

    if height == 14:
        clock = BigClock(sec=sec, color=color, gcalender=gcalender)
    elif height == 7:
        clock = MinimumClock(sec=sec, color=color, gcalender=gcalender)
    else:
        clock = SmallClock(sec=sec, color=color, gcalender=gcalender)
    padding = to_dimension(D(preferred=0))
    body = Window(content=FormattedTextControl(text=clock.get_clock), width=width, height=height, always_hide_cursor=True)
    if frame:
        body = Frame(body)
    if gcalender is None:
        under_text = Window(height=padding, always_hide_cursor=True)
    else:
        ct = gcalender.get_calender_text_formatted if color else gcalender.get_calender_text
        under_text = Window(content=FormattedTextControl(text=ct), width=gcalender.get_max_length(), height=padding, always_hide_cursor=True)

    # make container app
    root_container = HSplit([Window(height=padding, always_hide_cursor=True), _vsplit(padding, body), _vsplit(padding, under_text)], key_bindings=None)
    layout = Layout(container=root_container)
    return Application(layout=layout, key_bindings=kb, full_screen=True, refresh_interval=.1)


def main():
    args = parser.parse_args()
    gcalender = GCalender(args.events, args.today, args.color) if args.google_calender else None
    if args.second:
        if args.model == 0:
            app = make_app(True, 56, 7, args.frame, gcalender, args.color)
        elif args.model == 2:
            app = make_app(True, 124, 14, args.frame, gcalender, args.color)
        else:
            app = make_app(True, 83, 9, args.frame, gcalender, args.color)
    else:
        if args.model == 0:
            app = make_app(True, 36, 7, args.frame, gcalender, args.color)
        elif args.model == 2:
            app = make_app(False, 80, 14, args.frame, gcalender, args.color)
        else:
            app = make_app(False, 53, 9, args.frame, gcalender, args.color)
    app.run()


if __name__ == '__main__':
    main()
