from .Imports import *
from .Variable import Poll


def wait(time_ms, callback):
    def on_timeout():
        callback()
        return False

    return GLib.timeout_add(Poll._parse_interval(time_ms), on_timeout)


def lookup_icon(icon_name, size=128, path=True):
    if icon_name is not None:
        theme = Gtk.IconTheme.get_default()

        for name in [
            icon_name.lower(),
            icon_name.title(),
            icon_name.capitalize(),
            icon_name,
        ]:
            icon_info = theme.lookup_icon(
                name,
                size,
                Gtk.IconLookupFlags.USE_BUILTIN,
            )
            if icon_info is not None:
                return icon_info.get_filename() if path else icon_info

    return "" if path else lookup_icon("application-x-addon-symbolic")
