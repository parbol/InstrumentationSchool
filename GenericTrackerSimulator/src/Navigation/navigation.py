############################################################################
############################################################################
############################################################################
############################################################################
import sys
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.INFO)

class navigation:

    def __init__(self, trackers):

        self.trackers = trackers
        for tr in range(len(self.trackers)):
            for layer in range(len(self.trackers[tr].barrelLayers)):
                self.defineConnections(tr, layer, 0)
            for layer in range(len(self.trackers[tr].pEndcapDisks)):
                self.defineConnections(tr, layer, 1)
            for layer in range(len(self.trackers[tr].mEndcapDisks)):
                self.defineConnections(tr, layer, -1)
    
    
    ############################################################################
    def defineConnections(self, tr, layer, sys):

        #Vector meaning:
        #[tracker, layer, type]
        #It's the first layer of the barrel of the first tracker
        if tr == 0 and layer == 0 and sys == 0: 
            nextBarrel = [0, 1, 0]
            nextPEndcap = [0, 0, 1]
            nextNEndcap = [0, 0, -1]
            myself = [tr, layer, sys]
            self.trackers[tr].barrelLayers[layer].connections.append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].connections.append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(myself)
        #It's the first layer of the barrel of other tracker
        elif tr != 0 and layer == 0 and sys == 0:
            nextBarrel = [tr, layer+1, 0]
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            myself = [tr, layer, sys]
            previous = [tr-1, 0, 0]
            self.trackers[tr].barrelLayers[layer].connections.append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].connections.append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(myself)
            self.trackers[tr].barrelLayers[layer].connections.append(previous)
       #It's an intermediate layer of the barrel of any tracker
        elif layer != 0 and layer != self.trackers[tr].nBarrelLayers-1 and sys == 0:
            nextBarrel = [tr, layer+1, 0]
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            myself = [tr, layer, sys]
            previous = [tr, layer-1, 0]
            self.trackers[tr].barrelLayers[layer].connections.append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].connections.append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(myself)
            self.trackers[tr].barrelLayers[layer].connections.append(previous)
        #It's the last layer of the barrel of any tracker but the last
        elif tr != len(self.trackers) - 1 and layer == self.trackers[tr].nBarrelLayers-1 and sys == 0:
            nextBarrel = [tr+1, 0, 0]
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            nextPEndcap2 = [tr+1, 0, 1]
            nextNEndcap2 = [tr+1, 0, -1]
            myself = [tr, layer, sys]
            previus = [tr, layer-1, 0]
            self.trackers[tr].barrelLayers[layer].connections.append(nextBarrel)
            self.trackers[tr].barrelLayers[layer].connections.append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(nextNEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(nextPEndcap2)
            self.trackers[tr].barrelLayers[layer].connections.append(nextNEndcap2)
            self.trackers[tr].barrelLayers[layer].connections.append(myself)
            self.trackers[tr].barrelLayers[layer].connections.append(previous)
        #It's the last layer of the barrel of the last tracker
        elif tr != len(self.trackers) - 1 and layer == self.trackers[tr].nBarrelLayers-1 and sys == 0:
            nextPEndcap = [tr, 0, 1]
            nextNEndcap = [tr, 0, -1]
            self.trackers[tr].barrelLayers[layer].connections.append(nextPEndcap)
            self.trackers[tr].barrelLayers[layer].connections.append(nextNEndcap)
        #It's a positive disk of a tracker but not the last disk and not the last tracker
        elif tr != len(self.trackers)-1 and layer != self.trackers[tr].npEndcapDisks-1 and sys == 1:
            nextEndcap = [tr, layer+1, sys]
            nextBarrel = [tr+1, 0, 0]
            nextPossibleEndcap =[tr+1, 0, sys]
            self.trackers[tr].pEndcapDisks[layer].connections.append(nextEndcap)
            self.trackers[tr].pEndcapDisks[layer].connections.append(nextBarrel)
            self.trackers[tr].pEndcapDisks[layer].connections.append(nextPossibleEndcap)
        #It's a negative disk of a tracker but not the last disk and not the last tracker
        elif tr != len(self.trackers)-1 and layer != self.trackers[tr].nmEndcapDisks-1 and sys == -1:
            nextEndcap = [tr, layer+1, sys]
            nextBarrel = [tr+1, 0, 0]
            nextPossibleEndcap =[tr+1, 0, sys]         
            self.trackers[tr].mEndcapDisks[layer].connections.append(nextEndcap)
            self.trackers[tr].mEndcapDisks[layer].connections.append(nextBarrel)
            self.trackers[tr].mEndcapDisks[layer].connections.append(nextPossibleEndcap)
        #It's the last positive disk of a tracker but not the last tracker
        elif tr != len(self.trackers)-1 and layer == self.trackers[tr].npEndcapDisks-1 and sys == 1:
            nextBarrel = [tr+1, 0, 0]
            nextPossibleEndcap =[tr+1, 0, sys]
            self.trackers[tr].pEndcapDisks[layer].connections.append(nextBarrel)
            self.trackers[tr].pEndcapDisks[layer].connections.append(nextPossibleEndcap)
        #It's the last negative disk of a tracker but not the last tracker
        elif tr != len(self.trackers)-1 and layer == self.trackers[tr].nmEndcapDisks-1 and sys == -1:
            nextBarrel = [tr+1, 0, 0]
            nextPossibleEndcap =[tr+1, 0, sys]
            self.trackers[tr].mEndcapDisks[layer].connections.append(nextBarrel)
            self.trackers[tr].mEndcapDisks[layer].connections.append(nextPossibleEndcap)
        #It's a positive disk of the last tracker but not the last disk 
        elif tr == len(self.trackers)-1 and layer != self.trackers[tr].npEndcapDisks-1 and sys == 1:
            nextPossibleEndcap =[tr, layer + 1, sys]
            self.trackers[tr].pEndcapDisks[layer].connections.append(nextPossibleEndcap)
        #It's a negative disk of the last tracker but not the last disk 
        elif tr == len(self.trackers)-1 and layer != self.trackers[tr].nmEndcapDisks-1 and sys == -1:
            nextPossibleEndcap =[tr, layer + 1, sys]
            self.trackers[tr].mEndcapDisks[layer].connections.append(nextPossibleEndcap)  
        

    ############################################################################
    def printConnections(self):
        
        for tr in self.trackers:
            for layer in tr.barrelLayers:
                self.printConnectionsLayer(layer)
            for layer in tr.pEndcapDisks:
                self.printConnectionsLayer(layer)
            for layer in tr.mEndcapDisks:
                self.printConnectionsLayer(layer)


    ############################################################################
    def printConnectionsLayer(self, layer):

        print('--------------------------------------')
        if layer.type == 0:
            print(f'Barrel Layer {layer.barrelIndex} of tracker {layer.trackerIndex} is connected to:')
        elif layer.type == 1:
            print(f'Positive Endcap disk {layer.diskIndex} of tracker {layer.trackerIndex} is connected to:')
        elif layer.type == -1:
            print(f'Negative Endcap disk {layer.diskIndex} of tracker {layer.trackerIndex} is connected to:')
        for p in layer.connections:
            if p[2] == 0:
                print(f'Barrel layer number {p[1]} of tracker {p[0]}')
            elif p[2] == 1:
                print(f'Positive disk number {p[1]} of tracker {p[0]}')
            elif p[2] == -1:
                print(f'Negative disk number {p[1]} of tracker {p[0]}')


