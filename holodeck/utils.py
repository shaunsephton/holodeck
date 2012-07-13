from copy import copy
from django.conf import settings


def logical_to_pysical_shard_mapper(logical_shard_number):
    return logical_shard_number / (settings.LOGICAL_SHARDS / len(settings.PHYSICAL_SHARDS))

def generate_shard_database_settings():
    dbs = {}
    for i in range(0, settings.LOGICAL_SHARDS):
        shard = copy(settings.PHYSICAL_SHARDS[logical_to_pysical_shard_mapper(i)])
        shard_name = 'shard_%s' % i
        shard['NAME'] = '%s_%s' % (shard['NAME_PREFIX'], shard_name)
        dbs[shard_name] = shard
    return dbs

def metric_to_shard_mapper(metric):
    return metric.id % settings.LOGICAL_SHARDS

def sample_to_shard_mapper(sample):
    return sample.metric_id % settings.LOGICAL_SHARDS
