import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

import os


def resource_path(path):
    pwd = os.path.dirname(__file__)
    rel_path = os.path.join(pwd, path)
    return os.path.abspath(rel_path)

class MegaWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(1024, 768)
        self.set_icon_from_file(resource_path('megamailicon.png'))

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                           GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
                            lambda obj, pspec: max_action.set_state(
                                               GLib.Variant.new_boolean(obj.props.is_maximized)))
        
        self.builder = Gtk.Builder()
        self.builder.add_from_file(resource_path("mega.glade"))

        print("megawindow!")


    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()


        