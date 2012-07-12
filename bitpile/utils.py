from copy import copy
import bitpile_settings


def logical_to_pysical_shard_mapper(logical_shard_number):
    return logical_shard_number / (bitpile_settings.LOGICAL_SHARDS / len(bitpile_settings.PHYSICAL_SHARDS))

def generate_shard_database_settings():
    dbs = {}
    for i in range(0, bitpile_settings.LOGICAL_SHARDS):
        shard = copy(bitpile_settings.PHYSICAL_SHARDS[logical_to_pysical_shard_mapper(i)])
        shard_name = 'shard_%s' % i
        shard['NAME'] = '%s_%s' % (shard['NAME_PREFIX'], shard_name)
        dbs[shard_name] = shard
    return dbs

def sample_to_shard_mapper(sample):
    return sample.bucket_id % bitpile_settings.LOGICAL_SHARDS
