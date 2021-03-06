# measure class, stores a list of notes that  

from MidiFile import MIDIFile
from note import Note
import os
import felixNamespace

class Measure(list):
    def __init__(self):
        self = []

    def getVector(self):
	    return self.vector

    def setVector(self,the_vector):
	    self.vector = the_vector

    def addNote(self,note):
        self.append(note)

    def playMeasure(self,song_name,measure_num=0,tempo=120):
        measure = MIDIFile(1)
        track, time, channel = 0, 0, 0
        measure.addTrackName(track,time,"Measure")
        measure.addTempo(track,time, tempo)

        # Add notes to measure.
        for note in self:
            pitch = note.pitch
            duration = note.getDuration()
            time = note.getTime()
            volume = note.getVolume()
            measure.addNote(track,channel,pitch,time,duration,volume)
    	measure_num = str(measure_num)

        # Write the song to a file.
    	os.system("touch .songs/" + song_name + "/measure" + measure_num + ".mid")
        binfile = open(".songs/" + song_name + "/measure" + measure_num + ".mid", 'wb')
        measure.writeFile(binfile)
        binfile.close()
        os.system("fluidsynth -i " + felixNamespace.fluidsynthPath + " .songs/" + song_name + "/measure" + measure_num + ".mid > .dump")
