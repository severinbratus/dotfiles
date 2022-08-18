#!/usr/bin/env python3

from IPython import get_ipython
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import HasFocus, ViNavigationMode, ViSelectionMode, ViInsertMode, EmacsInsertMode, HasSelection
from prompt_toolkit.key_binding.vi_state import InputMode

import pyperclip


ip = get_ipython()


def copy_selection_to_clipboard(event):
    buffer = event.current_buffer
    data = buffer.copy_selection()
    pyperclip.copy(data.text)


def paste_from_clipboard(event):
    buffer = event.current_buffer
    data = pyperclip.paste()
    event.cli.vi_state.input_mode = InputMode.INSERT
    buffer.insert_text(data)
    event.cli.vi_state.input_mode = InputMode.NAVIGATION


# Register the shortcut if IPython is using prompt_toolkit
if getattr(ip, 'pt_app', None):

    filter_ = HasFocus(DEFAULT_BUFFER) & ViSelectionMode()
    ip.pt_app.key_bindings.add_binding('y', filter=filter_)(copy_selection_to_clipboard)

    filter_ = HasFocus(DEFAULT_BUFFER) & ViNavigationMode()
    ip.pt_app.key_bindings.add_binding('p', filter=filter_)(paste_from_clipboard)
