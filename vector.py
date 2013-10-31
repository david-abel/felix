# Elliot Mitchell and Dave Abel | Carleton College | vector.py |
# Implementation for vector class

import random
import math

class Vector():
	def __init__(self,type="Random"):	
		'''	Vectors are a list of Musical Properties in the following order:	
			[NOTE_DISTANCE,REPETITION,OCTAVE_CHANCE,145_to_2367 (called good_note_ratio below),ONE_vs_CHORD,VARIETY_DURATION]
		'''
		if type == "Random" or type == "random":
			self = self.buildRandomVector()
		elif type == "Master" or type == "master":
			self = self.buildFromFile(".master.vct") 
		elif type == "User" or "user":
			self = self.buildFromFile(".user_vectors.vct")
			
	def normalize(self):
		magnitude = self.getMagnitude()
		if magnitude != 1.0:
			for i in range(6):
				self[i] = self[i]/magnitude

	def getMagnitude(self):
		mag = 0
		for i in range(6):
			mag += self[i]**2
		mag = math.sqrt(mag)
		return mag

	def update(self,learning_vector,learning_rate,user_opinion):
		'''	Shifts the current vector based on the user_opinion and, learning_rate, and learning_vector (which generated the song).
			Assumes that current vector (self) and learning_vector are already normalized
			learning_vector is a vector pulled from the .user_vectors.vct file. 
			learning_rate is a value that determines how quickly we are learning.
			user_opinion is a value from 1-10 that reflects how much the user liked the measure that was generated with the learning vector
		'''
		self.normalize()
		learning_vector.normalize()
		for i in range(6):
			mapped_user_opinion = float(user_opinion - 5)/2.5
			self[i] = self[i] + learning_rate*mapped_user_opinion*(learning_vector[i] - self[i])
		self.normalize()

	def buildRandomVector(self):
		self.note_distance = random.random()
		self.repetition = random.random()
		self.octave_chance = random.random()
		self.good_note_ratio = random.random()
		self.one_vs_chord = random.random()
		self.variety_duration = random.random()

	def buildFromFile(self,filename):
		try:
			f = open(filename)
			vector_list = f.read().strip().split("\n")
			properties = random.choice(vector_list).split()
			the_vector = self.buildFromList(properties)
			f.close()
			return the_vector
		except IndexError:
			print "File Contents Empty!\nfile: ", filename
			return None
			
	def buildFromList(self,props):
		self.note_distance = float(props[0])
		self.repetition = float(props[1])
		self.octave_chance = float(props[2])
		self.good_note_ratio = float(props[3])
		self.one_vs_chord = float(props[4])
		self.variety_duration = float(props[5])

	def writeToFile(self,filename):
		if filename == ".master.vct":
			f = open(filename,"w")	
		elif filename == ".user_vectors.vct":
			f = open(filename,"a")	
		file_vector = ""
		for i in range(6):
			file_vector += str(self[i]) + " "
		file_vector = file_vector[:-1] + "\n"
		f.write(file_vector)
		f.close()
		
	def __getitem__(self,index):
		if index == 0:
			return self.note_distance
		elif index == 1:
			return self.repetition
		elif index == 2:
			return self.octave_chance
		elif index == 3:
			return self.good_note_ratio
		elif index == 4:
			return self.one_vs_chord
		elif index == 5:
			return self.variety_duration
	def __setitem__(self,index,new_val):
		if index == 0:
			self.note_distance = new_val	
		elif index == 1:
			self.repetition = new_val
		elif index == 2:
			self.octave_chance = new_val
		elif index == 3:
			self.good_note_ratio = new_val
		elif index == 4:
			self.one_vs_chord = new_val
		elif index == 5:
			self.variety_duration = new_val
				
	def __str__(self):
		to_string = "< "
		for i in range(6):
			to_string +=  str(self[i]) + ", "
		to_string = to_string[:-2]
		to_string += " >"
		return to_string

	def getNoteDistance(self):
		return self[0]
	def getRepetition(self):
		return self[1]
	def getOctaveChance(self):
		return self[2]
	def getGoodNoteRatio(self):
		return self[3]
	def getOneVsChord(self):
		return self[4]
	def getVarietyDuration(self):
		return self[5]
	
	def setNoteDistance(self,new_note_distance):
		self[0] = new_note_distance
	def setRepetition(self,new_repetition):
		self[1] = new_repetition
	def setOctaveChance(self,new_octave_chance):
		self[2] = new_octave_chance
	def setGoodNoteRatio(self,new_good_note_ratio):
		self[3] = new_good_note_ratio
	def setOneVsChord(self,new_one_vs_chord):
		self[4] = new_one_vs_chord
	def setVarietyDuration(self,new_variety_duration):
		self[5] = new_variety_duration
	
