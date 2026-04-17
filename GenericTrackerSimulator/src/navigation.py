

class navigation:

    def __init__(self, trackers):

        self.trackers = trackers
        
        #Each tracker is allowed to have up to 100 layers or disks
        trackerOffset = 0
        for i in range(len(self.trackers)):
            trackerOffset = 500 * i
            for bl, j in enumerate(trackers[i].barrelLayers):
                bl.index = j + trackerOffset
            for ed, j in enumerate(trackers[i].pEndcapLayers):
                ed.index = j + 100 + trackerOffset
            for ed, j in enumerate(trackers[i].mEndcapLayers):
                ed.index = -j - 100 - trackerOffset

    ############################################################################
    def getLayerFromIndex(self, layerIndex):

        sign = 1
        if layerIndex < 0:
            sign = -1
        trIndex = int((sign*layerIndex) / 500)
        if trIndex >= len(self.trackers):
            return -1, 0, 0
        lIndex = (sign*layerIndex) % 500
        
        if sign == 1:
            #This is a barrel layer
            if lIndex >= 0 and layerIndex < 100:
                return trIndex, lIndex, 0
            #This is a positive endcap layer
            elif lIndex >= 100 and lIndex < 200:
                return trIndex, lIndex - 100, 1
            else:
                return -1, 0, 0
        else:
            #This is a negative endcap layer
            if lIndex >= 100 and lIndex < 200:
                return trIndex, lIndex - 100, -1
            else:
                return -1, 0, 0

    
    ############################################################################
    def candidates(self, tr, layer, sys):

        if tr == -1:
            return []

        listOfCandidates = []
        #Casuistics:
        
        #It's the first layer of the barrel of the first tracker
        if tr == 0 and layer == 0 and sys == 0: 
            nextBarrel = [0, 1, 0]
            nextPEndcap = [0, 0, 1]
            nextNEndcap = [0, 0, -1]
            myself = [0, 0, 0]
            self.trackers[tr].barrelLayers[layer].append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].append(myself)
        #It's the first layer of the barrel of other tracker
        elif tr != 0 and layer == 0 and sys == 0:
            nextBarrel = [tr, layer+1, 0]
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            myself = [tr, layer, sys]
            previus = [tr-1, len(self.trackers[tr-1])-1, 0]
            self.trackers[tr].barrelLayers[layer].append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].append(myself)
            self.trackers[tr].barrelLayers[layer].append(previous)
       #It's an intermediate layer of the barrel of any tracker
       elif layer != 0 and layer != len(self.trackers[tr])-1 and sys == 0:
            nextBarrel = [tr, layer+1, 0]
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            myself = [tr, layer, sys]
            previus = [tr, layer-1, 0]
            self.trackers[tr].barrelLayers[layer].append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].append(myself)
            self.trackers[tr].barrelLayers[layer].append(previous)
        #It's the last layer of the barrel of any tracker but the last
        elif tr != len(self.trackers) - 1 and layer == len(self.trackers[tr])-1 and sys == 0:
            nextBarrel = [tr+1, 0, 0]
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            nextPEndcap2 = [tr+1, 0, 1]
            nextNEndcap2 = [tr+1, 0, -1]
            myself = [tr, layer, sys]
            previus = [tr, layer-1, 0]
            self.trackers[tr].barrelLayers[layer].append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].append(nextPEndcap2)
            self.trackers[tr].barrelLayers[layer].append(nextNEndcap2)
            self.trackers[tr].barrelLayers[layer].append(myself)
            self.trackers[tr].barrelLayers[layer].append(previous)
        #It's the last layer of the barrel of the last tracker
        elif tr != len(self.trackers) - 1 and layer == len(self.trackers[tr])-1 and sys == 0:
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            self.trackers[tr].barrelLayers[layer].append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].append(nextNEndcap)
        #It's the first disk of the first tracker
        elif tr != len(self.trackers) - 1 and layer == len(self.trackers[tr])-1 and sys == 0:
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            self.trackers[tr].barrelLayers[layer].append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].append(nextNEndcap)
           


        if layerIndex > 0:

            trIndex = int(layerIndex / 500)
            lIndex = layerIndex % 500

        if layerIndex >= 0 and layerIndex < 100:

            #This is a barrel layer
            if layerIndex != 

        elif layerIndex >= 100 and layerIndex < 200:

            #This is a positive endcap layer

        elif layerIndex <= -100 and layerIndex > -200:

            #This is a negative endcap layer

        else:

            return []




