class ShardRouter(object):
    """
    A router to control/map bitpile.models.Sample shard read/writes.
    """
    def allow_syncdb(self, db, model):
        "Make sure the Sample model only apperas on shard dbs."
        from bitpile.models import Sample
       
        # TODO: startswith check sucks, improve.
        if db.startswith('shard_'):
            return model == Sample
        elif model == Sample:
            return False
        return None
