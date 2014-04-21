"""
    A map-reduce that calculates the density for each
    of a set of tracks.  The track density is the average
    number of segments per segment for a track.
"""

from yaafelib import *

import sys, os, inspect
from features import mfcc_1


class Analyzer:

    SAMPLERATE = 22050
    featureList = mfcc_1.FEATURE
    dataflow_file = None
    toCSV = False

    
    #init for loading from a featureList array
    def __init__(self, samplerate, featureList, toCSV):
        self.SAMPLERATE = samplerate       
        self.featureList = featureList
        self.toCSV = toCSV

    #init for loading from an existing datafile
    def __init__(self, samplerate, dataflow_file, toCSV):
        self.SAMPLERATE = samplerate
        self.dataflow_file = dataflow_file
        self.toCSV = toCSV


    #parses dataflow from featureList array given at __init__
    def dataFlowCreator(self):
        fp = FeaturePlan(sample_rate=self.SAMPLERATE)
        for i in range(len(self.featureList)):
            fp.addFeature(self.featureList[i])

        df = fp.getDataFlow()
        return df


    #loads an existing dataflow from file
    def dataFlowLoader(self):
        if self.dataflow_file is not None:
            df = DataFlow()
            df.load(self.dataflow_file)
            return df

    
    #processes audio given specified dataflow
    def process_mp3(self, mp3, dataflow):
        engine = Engine()
        engine.load(dataflow)
        afp = AudioFileProcessor()
        
        afp.processFile(engine, mp3)
        feats = engine.readAllOutputs()
        if self.toCSV:
            afp.setOutputFormat('csv', '../output', {'Precision': '8'})
            if afp.processFile(engine, mp3) is False:
                return True
            else:
                return False
        #[DEBUG]
        #print(feats)


if __name__ == '__main__':
    featureList = mfcc_1.FEATURE
    print(featureList)          #[DEBUG]
    analyzer = analyzer(22050, featureList, True)
    df = analyzer.dataFlowCreator()
    mp3 = sys.argv[1]
    analyzer.process_mp3(mp3, df)
