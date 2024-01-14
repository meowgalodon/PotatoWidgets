from ...__Import import *
from ...Variable import Listener, Poll, Variable


class BasicProps(Gtk.Widget):
    def __init__(
        self,
        halign,
        valign,
        hexpand,
        vexpand,
        active,
        visible,
        classname,
        # tooltip,
        css,
        size=[10, 10],
    ):
        Gtk.Widget.__init__(self)
        self.set_hexpand(True if hexpand else False)
        self.set_vexpand(True if vexpand else False)
        self.set_halign(halign)
        self.set_valign(valign)
        self.set_visible(visible)
        self.set_active(active)
        self.set_classname(classname)
        self.__clasif_size(size)

        for key, value in locals().items():
            callback = {
                "halign": self.set_halign,
                "valign": self.set_valign,
                "hexpand": self.set_hexpand,
                "vexpand": self.set_vexpand,
                "active": self.set_sensitive,
                "visible": self.set_visible,
                "size": self.set_size,
                "classname": self.set_classname,
            }.get(key)

            self.bind(value, callback) if callback else None

    def set_size(self, size):
        self.__clasif_size(size)

    def set_halign(self, param):
        super().set_halign(self.__clasif_align(str(param)))

    def set_valign(self, param):
        super().set_valign(self.__clasif_align(str(param)))

    def set_active(self, param):
        if param != None and param:
            super().set_sensitive(param)

    def __clasif_size(self, size):
        if isinstance(size, int):
            self.set_size_request(size, size)
        elif isinstance(size, list):
            if len(size) == 2:
                self.set_size_request(size[0], size[1])
            elif len(size) == 1:
                self.set_size_request(size[0], size[0])

    def __clasif_align(self, param):
        dict = {
            "fill": Gtk.Align.FILL,
            "start": Gtk.Align.START,
            "end": Gtk.Align.END,
            "center": Gtk.Align.CENTER,
            "baseline": Gtk.Align.BASELINE,
        }
        return dict.get(param.lower(), Gtk.Align.FILL)

    def set_classname(self, param):
        if isinstance(param, (str)):
            context = self.get_style_context()
            [context.add_class(i) for i in param.split(" ") if i != " "]
        elif isinstance(param, (list)):
            for i in param:
                if isinstance(i, (Listener, Variable, Poll)):
                    pass

    def bind(self, variable, callback):
        if isinstance(variable, (Listener, Variable, Poll)):
            try:
                argcount = callback.__code__.co_argcount
            except:
                argcount = -1

            try:
                argname = [
                    i
                    for i in callback.__code__.co_varnames[
                        : callback.__code__.co_argcount
                    ]
                ]
            except:
                argname = []
            try:
                function_name = callback.__name__
            except:
                function_name = None

            # print(function_name, argcount, argname)
            if function_name == "<lambda>":
                if argcount == 1:
                    if "self" in argname:
                        variable.connect(
                            "valuechanged",
                            lambda _: GLib.idle_add(lambda: callback(self)),
                        )
                    else:
                        variable.connect(
                            "valuechanged",
                            lambda out: GLib.idle_add(
                                lambda: callback(out.get_value())
                            ),
                        )
                elif argcount == 2:
                    variable.connect(
                        "valuechanged",
                        lambda out: GLib.idle_add(
                            lambda: callback(self, out.get_value())
                        ),
                    )
                elif argcount == -1:
                    variable.connect(
                        "valuechanged",
                        lambda out: GLib.idle_add(lambda: callback(out.get_value())),
                    )
            else:
                variable.connect(
                    "valuechanged",
                    lambda out: GLib.idle_add(lambda: callback(out.get_value())),
                )
