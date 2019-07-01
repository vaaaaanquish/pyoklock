from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import Box, Frame
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import AnyDimension
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.layout.dimension import to_dimension
from prompt_toolkit.layout.containers import VSplit, HSplit
import argparse
from .utils import BigClock
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--second', action='store_true', help='print second')


def make_app(sec, width):
    """make auto refresh application class"""
    kb = KeyBindings()
    @kb.add('c-c')
    def _(event):
        event.app.exit()

    clock = BigClock(sec=sec)
    padding = to_dimension(D(preferred=0))
    body = Frame(
            Window(
                content=FormattedTextControl(text=clock.get_clock),
                width=width,
                height=14,
                always_hide_cursor=True))
    root_container = HSplit([
        Window(height=padding, always_hide_cursor=True),
        VSplit([
            Window(width=padding, always_hide_cursor=True),
            body,
            Window(width=padding, always_hide_cursor=True),
            ]),
        Window(height=padding, always_hide_cursor=True),
        ], key_bindings=None)
    layout = Layout(container=root_container)
    return Application(layout=layout, key_bindings=kb, full_screen=True, refresh_interval=.1)


def main():
    args = parser.parse_args()
    if args.second:
        app = make_app(True, 124)
    else:
        app = make_app(False, 80)
    app.run()


if __name__ == '__main__':
    main()
