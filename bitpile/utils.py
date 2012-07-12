from copy import copy
import bitpile_settings


def shard_mapper():
    result = {}
    mapper = bitpile_settings.LOGICAL_SHARDS / len(bitpile_settings.PHYSICAL_SHARDS)
    
    for i in range(0, bitpile_settings.LOGICAL_SHARDS):
        shard = copy(bitpile_settings.PHYSICAL_SHARDS[i/mapper])
        shard_name = 'shard_%s' % i
        shard['NAME'] = '%s_%s' % (shard['NAME_PREFIX'], shard_name)
        result[shard_name] = shard

    return result
