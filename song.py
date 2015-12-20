# Dave Abel and Elliot Mitchell | Carleton College | song.py
# Implementation for song class

from MidiFile import MIDIFile
from measure import Measure
from note import Note
import os
import random
import felixNamespace


class Song():
	# Class that controls 
	def __init__(self,root,mode,song_name):
		self.song_name = song_name
		self.measures = []
		self.current_measure = 0
		self.root = int(root)
		self.mode = mode
		self.buildMode()
		self.buildOctaves()
		os.system("mkdir .songs/" + self.song_name)
		os.system("touch .songs/" +  self.song_name + "/" + self.song_name + ".mid")
	
	def playMeasure(self,song_name,measure_num=None):
		if measure_num == None:
			measure_num = self.current_measure
		self.measures[measure_num].playMeasure(song_name,measure_num)

	def playSong(self):
		the_song = MIDIFile(1) # Note: 1 here is the number of tracks.
		time = 0 # Initialize time
		track = 0
		the_song.addTrackName(track,time,self.song_name) # Track = 0
		the_song.addTempo(track,time,120) # 120 is the tempo.
		for measure in self.measures:
			for note in measure:
				the_song.addNote(track,note.getChannel(),note.getPitch(),time+note.getTime(),note.getDuration(),note.getVolume())
			time += 4
		song_file = open(".songs/" + self.song_name + "/" + self.song_name + ".mid","wb")
		the_song.writeFile(song_file)
		song_file.close()
		os.system("fluidsynth -i " + felixNamespace.fluidsynthPath + " .songs/" + self.song_name + "/" + self.song_name + ".mid > .dump")

	def buildMode(self):
		# 60 is middle C
		if self.mode == 1: # Ionian mode. (Major scale)
			self.scale = [self.root,self.root+2,self.root+4,self.root+5,self.root+7,self.root+9,self.root+11,self.root+12]
		elif self.mode == 2: # Dorian mode.
			self.scale = [self.root,self.root+2,self.root+3,self.root+5,self.root+7,self.root+9,self.root+11,self.root+12]
		elif self.mode == 3: # Phrygian mode.
			self.scale = [self.root,self.root+1,self.root+3,self.root+5,self.root+7,self.root+8,self.root+10,self.root+12]
		elif self.mode == 4: # Lydian mode.
			self.scale = [self.root,self.root+2,self.root+4,self.root+6,self.root+7,self.root+9,self.root+11,self.root+12]
		elif self.mode == 5: # Mixolydian mode.
			self.scale = [self.root,self.root+2,self.root+3,self.root+5,self.root+7,self.root+9,self.root+10,self.root+12]
		elif self.mode == 6: # Aeolian mode. (Minor scale)
			self.scale = [self.root,self.root+2,self.root+3,self.root+5,self.root+7,self.root+9,self.root+10,self.root+12]
		elif self.mode == 7: # Locrian mode.
			self.scale = [self.root,self.root+1,self.root+3,self.root+5,self.root+6,self.root+8,self.root+10,self.root+12]

	
	def buildOctaves(self):
		double_scale = self.scale[:-1]
		i = 0
		for pitch in self.scale:
			double_scale.insert(i,pitch-12)
			double_scale.append(pitch+12)
			i += 1
		self.octaves = double_scale
			
	def addMeasure(self,vector,length=4):
		# Takes in a vector and generates a measure based on the features of the vector
		self.current_measure +=1	
		if self.binaryProbability(vector.getRepetition()) == True:
			if self.current_measure > 1:
				measure_index = random.choice(range(len(self.measures)))
				the_measure = self.measures[measure_index]
				new_vec = the_measure.getVector() # If we're repeating, we want the user's opinion to reflect on the randomly selected vector's properties, except for the repetition property. This should reflect upon the current vectors (called 'vector') repetition property. So we make a new vector that has the randomly selected vector's properties except for repetition, which is taken from the current vector that caused us to repeat
				new_vec.setRepetition(vector.getRepetition())
				the_measure.setVector(new_vec)
				self.measures.append(the_measure) # Add the first measure.	
				return
		measure = Measure()
		measure.setVector(vector)
		time_left = float(length)
		self.chanceToChangeOctave(vector.getOctaveChance())
		while time_left > 0:
			pitch_list = self.buildNoteRatioList(vector.getGoodNoteRatio())
			if measure == []:
				# First note in the measure, just choose an item from our possible pitches randomly. <- Could be improved
				pitch = random.choice(pitch_list)
			else:
				# otherwise, incorporate the variety distance weight.
				pitch_list.extend(self.buildDistanceRatio(measure[-1],vector.getNoteDistance()))
				pitch = random.choice(pitch_list)
			if time_left != 4:
				duration = self.pickDuration(vector.getVarietyDuration(),time_left,measure)
			else:
				duration = random.choice([.25,.5,1,2,4]) # First note, choose a duration randomly
			note = Note(4-time_left,1,pitch,duration,100)
			measure.addNote(note)

			# Check to see if adding a chord
			if self.binaryProbability(vector.getOneVsChord()):
				# We rolled a chord.
				pitches_in_chord = self.chordList(pitch)
				for chord_pitch in pitches_in_chord:
					chord_note = Note(4-time_left,1,chord_pitch,duration,100)
					measure.addNote(chord_note)	
			time_left -= duration
		self.measures.append(measure)
		
	def chordList(self,pitch):
		temp_scale = self.scale[:-1] # Our scale without the 2nd root
		pitch_index = self.octaves.index(pitch)
		chord_list = [[temp_scale[(pitch_index + 2) % 7]],[temp_scale[(pitch_index + 3) % 7]],[temp_scale[(pitch_index + 4) % 7]],[temp_scale[(pitch_index + 2) % 7],temp_scale[(pitch_index + 4) % 7]],[temp_scale[(pitch_index + 2) % 7],temp_scale[(pitch_index + 4) % 7],temp_scale[(pitch_index + 6) % 7]]]
		return random.choice(chord_list)

	def pickDuration(self,vector_val,time_left,measure):
		# Takes in time_left to determine which notes we can play in the remaining time. Takes in measure so we know what notes we have played so far this measure (which dictates which notes we can play based on the 'varietyDuration' of the vector_val).
		duration_list = [.25,.5,1,2,4]
		# this loop removes not durations that will not fit in the remaining part of the measure
		for item in [.25,.5,1,2,4]:
			if item > time_left:
				duration_list.remove(item)
		if len(duration_list) == 1:
			return duration_list[0]
		duration_list = duration_list * (len(measure)+1) 
		for note_index in range(len(measure)):
			if self.binaryProbability(vector_val): # variety HIGH! we want to remove durations that have been played already, and add those that have not
				if measure[note_index].getDuration() < time_left:
					duration_list.remove(measure[note_index].getDuration()) # remove duration that's already been played
				random_dur = random.choice(duration_list)
				while random_dur > time_left and random_dur == measure[note_index].getDuration():
					random_dur = random.choice(duration_list)
				duration_list.append(random_dur) # Adding a duration that's not been played yet
			elif self.binaryProbability(1-vector_val): # variety LOW! we want to remove durations that have not been played yet, and add those that have.
				random_dur = random.choice(duration_list) 
				while random_dur == measure[note_index].getDuration():
					random_dur = random.choice(duration_list)
				duration_list.remove(random_dur) # remove a duration that's already been played
				duration_list.append(measure[note_index].getDuration()) # add a duration that hasn't been played yet. 
		return random.choice(duration_list)

	def binaryProbability(self,vector_val):
		''' Takes in a weight from a vectors repetition value and compares it to a randomly generated value between 0 and 1. If initial value is bigger, return True, else return False. Used to determine if we should repeat or not, given a probablity from 0.0 to 1.0'''
	
		r =	random.random()
		if vector_val > r:
			return True
		else:
			return False
	
	def buildNoteRatioList(self,vector_val):
		''' Given a value from 0 to 1, build a note list based off the scale where the number of 1's,4's, 5's,8's is weighted with respect to the 100*vector_val, and the 2's,3's,6's,7's are weighted with respect to 100 - vector_val'''
		note_list = []
		good_note_val = vector_val * 100
		bad_note_val = 100 - good_note_val
		for i in [0,3,4,7]: # Change the 1 the 4, the 5 and the 8
			note_list.extend(self.scale[i] for j in range(int(good_note_val)))
		for i in [1,2,5,6]:
			note_list.extend(self.scale[i] for j in range(int(bad_note_val)))
		return note_list
	
	def buildDistanceRatio(self,note,vector_val):
		note_list = []
		old_pitch = note.getPitch()
		root_index = self.octaves.index(note.getPitch())
		
		max_index = min((root_index + 7), (len(self.octaves)-1))
		min_index = max((root_index - 7), 0)
		above_scale = self.octaves[root_index:max_index]
		below_scale = self.octaves[min_index:root_index]
		if vector_val > .5: #if note distance is HIGH we want to weight the further notes more than the closer notes. we change the order of the scales so that the first notes in the list are the ones we want to have the highest probability of playing.
			above_scale.reverse()
		else:
			vector_val = (1 - vector_val)
			below_scale.reverse()
		multiplier = int(vector_val*150)
		for note in above_scale:
			note_list.extend(note for j in range(multiplier))
			multiplier = int(multiplier/len(above_scale))
		for note in below_scale:
			note_list.extend(note for j in range(multiplier))
			multiplier = int(multiplier/len(below_scale))
		return note_list
		
	def chanceToChangeOctave(self,vector_val):
		if self.root > 80 or self.root < 35:
			return
		if self.binaryProbability(vector_val):
			delta = random.choice([12,-12,12,-12])	#this is due to the suspicion that random.choice doesn't select uniformly
			for index in range(len(self.scale)):
				self.scale[index] += delta
			self.root += delta
			self.buildOctaves()
