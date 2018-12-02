import DistributedTreasure

class DistributedSZTreasure(DistributedTreasure.DistributedTreasure):
    __module__ = __name__

    def __init__(self, cr):
        DistributedTreasure.DistributedTreasure.__init__(self, cr)