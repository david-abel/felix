# Elliot Mitchell and Dave Abel | Carleton College | note.py |
# Implementation for note class

class Note():
	def __init__(self,time,channel,pitch,duration,volume):
		self.time = time # Note: this is relative to this notes measure, not the global time
		self.channel = channel
		self.pitch = pitch
		self.duration = duration
		self.volume = volume

	def getTime(self):
		return self.time

	def getChannel(self):
		return self.channel

	def getDuration(self):
		return self.duration

	def getPitch(self):
		return self.pitch

	def getVolume(self):
		return self.volume

	def setTime(self,new_time):
		self.time = new_time

	def setChannel(self,new_channel):
		self.channel = new_channel

	def setPitch(self,new_pitch):
		self.pitch = new_pitch

	def setDuration(self,new_duration):
		self.duration = new_duration

	def setVolume(self,new_volume):
		self.volume = new_volume
