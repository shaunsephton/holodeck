class ShardRouter(object):
    """
    A router to control/map holodeck.models.Sample shard read/writes.
    """
    def allow_syncdb(self, db, model):
        "Make sure the Sample model only apperas on shard dbs."
        # TODO: move this import uptop
        from holodeck.models import Sample
       
        # TODO: startswith check sucks, improve.
        if db.startswith('shard_'):
            return model == Sample
        elif model == Sample:
            return False
        return None
