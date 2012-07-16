from copy import copy
import inspect
import sys

from django.conf import settings
from holodeck import widgets


def logical_to_physical_shard_mapper(logical_shard_number):
    """
    Maps a logical shard to its physical couterpart.
    Many logical shards can be contained in a physical shard.
    """
    return logical_shard_number / (
        settings.LOGICAL_SHARDS / len(settings.PHYSICAL_SHARDS))


def generate_shard_database_settings():
    """
    Generates Django database settings for logical shards mapped
    to physical shards/databases.
    """
    dbs = {}
    for i in range(0, settings.LOGICAL_SHARDS):
        shard = copy(settings.PHYSICAL_SHARDS[
            logical_to_physical_shard_mapper(i)])
        shard_name = 'shard_%s' % i
        shard['NAME'] = '%s_%s' % (shard['NAME_PREFIX'], shard_name)
        dbs[shard_name] = shard
    return dbs


def metric_to_shard_mapper(metric):
    """
    Given a metric determines in which logical shard it's
    reverse relations are stored.
    """
    return metric.id % settings.LOGICAL_SHARDS


def sample_to_shard_mapper(sample):
    """
    Given a shard determines in which logical shard it's stored.
    """
    return sample.metric_id % settings.LOGICAL_SHARDS


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
