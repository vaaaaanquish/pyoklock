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
from clocks import BigClock
from google_calender import GCalender

parser = argparse.ArgumentParser()
parser.add_argument('--events', type=int, default=10)
parser.add_argument('-s', '--second', action='store_true', help='print second')
parser.add_argument('-f', '--frame', action='store_true', help='print frame')
parser.add_argument(
    '-g',
    '--google_calender',
    action='store_true',
    help='print google calender')


def make_app(sec, width, frame=True, calender=True, events=10):
    """make auto refresh application class"""
    kb = KeyBindings()

    @kb.add('c-c')
    def _(event):
        event.app.exit()

    def _vsplit(padding, m):
        return VSplit([
            Window(width=padding, always_hide_cursor=True), m,
            Window(width=padding, always_hide_cursor=True)
        ])

    clock = BigClock(sec=sec)
    padding = to_dimension(D(preferred=0))
    body = Window(
        content=FormattedTextControl(text=clock.get_clock),
        width=width,
        height=14,
        always_hide_cursor=True)
    if frame:
        body = Frame(body)
    if calender:
        gcalender = GCalender(events)
        under_text = Window(
            content=FormattedTextControl(text=gcalender.get_calender_text),
            width=gcalender.get_max_length(),
            height=padding,
            always_hide_cursor=True)
    else:
        under_text = Window(height=padding, always_hide_cursor=True)

    # make container app
    root_container = HSplit([
        Window(height=padding, always_hide_cursor=True),
        _vsplit(padding, body),
        _vsplit(padding, under_text)
    ],
                            key_bindings=None)
    layout = Layout(container=root_container)
    return Application(
        layout=layout, key_bindings=kb, full_screen=True, refresh_interval=.1)


def main():
    args = parser.parse_args()
    if args.second:
        app = make_app(True, 124, args.frame, args.google_calender,
                       args.events)
    else:
        app = make_app(False, 80, args.frame, args.google_calender,
                       args.events)
    app.run()


if __name__ == '__main__':
    main()
