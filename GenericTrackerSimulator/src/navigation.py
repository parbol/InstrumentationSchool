

class navigation:

    def __init__(self, trackers):

        self.trackers = trackers
        for tr in range(len(self.trackers)):
            for layer in range(len(self.trackers[tr].barrelLayers)):
                self.defineConnections(tr, layer, 0)
            for layer in range(len(self.trackers[tr].pEndcapLayers)):
                self.defineConnections(tr, layer, 1)
            for layer in range(len(self.trackers[tr].mEndcapLayers)):
                self.defineConnections(tr, layer, -1)
    
    
    ############################################################################
    def defineConnections(self, tr, layer, sys):

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
            previous = [tr-1, len(self.trackers[tr-1])-1, 0]
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
        #It's a disk of a tracker but not the last disk and not the last tracker
        elif tr != len(self.trackers)-1 and layer != len(self.trackers[tr])-1 and abs(sys) == 1:
            nextEndcap = [tr, layer+1, sys]
            nextBarrel = [tr+1, 0, 0]
            nextPossibleEndcap =[tr+1, 0, sys]
            if sys == 1:
                self.trackers[tr].pEndcapLayers[layer].append(nextEndcap)
                self.trackers[tr].pEndcapLayers[layer].append(nextBarrel)
                self.trackers[tr].pEndcapLayers[layer].append(nextPossibleEndcap)
            else:
                self.trackers[tr].nEndcapLayers[layer].append(nextEndcap)
                self.trackers[tr].nEndcapLayers[layer].append(nextBarrel)
                self.trackers[tr].nEndcapLayers[layer].append(nextPossibleEndcap)
        #It's the last disk of a tracker but not the last tracker
        elif tr != len(self.trackers)-1 and layer == len(self.trackers[tr])-1 and abs(sys) == 1:
            nextBarrel = [tr+1, 0, 0]
            nextPossibleEndcap =[tr+1, 0, sys]
            if sys == 1:
                self.trackers[tr].pEndcapLayers[layer].append(nextBarrel)
                self.trackers[tr].pEndcapLayers[layer].append(nextPossibleEndcap)
            else:
                self.trackers[tr].nEndcapLayers[layer].append(nextBarrel)
                self.trackers[tr].nEndcapLayers[layer].append(nextPossibleEndcap)
        #It's a disk of the last tracker but not the last disk 
        elif tr == len(self.trackers)-1 and layer == len(self.trackers[tr])-1 and abs(sys) == 1:
            print('Last tracker everything') 
        else:
            print('Other cases')


      



