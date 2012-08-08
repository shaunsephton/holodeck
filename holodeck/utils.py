import inspect
import sys

from holodeck import widgets


def load_class_by_string(class_path):
    """
    Returns a class when given its full name in
    Python dot notation, including modules.
    """
    parts = class_path.split('.')
    module_name = '.'.join(parts[:-1])
    class_name = parts[-1]
    __import__(module_name)
    mod = sys.modules[module_name]
    return getattr(mod, class_name)


def get_widget_type_choices():
    """
    Generates Django model field choices based on widgets
    in holodeck.widgets.
    """
    choices = []
    for name, member in inspect.getmembers(widgets, inspect.isclass):
        if member != widgets.Widget:
            choices.append((
                "%s.%s" % (member.__module__, member.__name__),
                member.name
            ))
    return choices
