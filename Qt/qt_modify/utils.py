import types


class QtModifier:
    """
    The qualifier of qt_modify, used to easily register custom function to Qt package
    """
    def __init__(self):
        self.changes = dict()

    def register(self, full_name):
        def receiver(function):
            self.changes[full_name] = function
            return function
        return receiver

    def modify(self, root_module):
        assert isinstance(root_module, types.ModuleType)
        root_name = root_module.__name__

        for full_name, function in self.changes.items():
            module = root_module
            cur_name = root_name
            name_list = full_name.split(".")
            for name in name_list[:-1]:
                module = getattr(module, name, None)
                if not module:
                    raise AttributeError("{} don't have attribute {}".format(cur_name, name))
                cur_name = ".".join([cur_name, name])
            setattr(module, name_list[-1], function)
