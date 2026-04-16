

class navigation:

    def __init__(self, trackers):

        layersDic = dict()
        
        layerCounter = 0
        for tr in trackers:
            for blayer in tr.barrelLayers:
                layersDic[layerCounter] = blayer


