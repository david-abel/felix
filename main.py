# Elliot Mitchell and Dave Abel | Carleton College | main.py |
# Main function calls for Felix.

import random
from MidiFile import MIDIFile
import os
from song import Song
from vector import Vector
from measure import Measure
from note import Note

# Global variables
root = 60 
num_measures = 6 
mode = 1
title = "test"

def queryUser():
	global root 
	global num_measures 
	global mode 
	global title 
	root = raw_input("Please select a root node for your song (number from 40-80. 60 is Middle C) ")
	while root.isdigit() != True  or int(root) < 40 or int(root) > 80:
		print "Invalid Selection."
		root = raw_input("Choose an integer (number from 40-80. 60 is Middle C) ")
	root = int(root)
	num_measures = raw_input("How many measures do you want your song to be? ")
	while num_measures.isdigit() != True or int(num_measures) > 100 and int(num_measures) < 0:
		print "Invalid Selection."
		num_measures = int(raw_input("Please select a reasonable number of measures (positive integer less than 100) "))
	num_measures = int(num_measures)
	print
	print "|-----------------|-----|"
	print "|       Mode      | Num |"
	print "|-----------------|-----|"
	print "|                 |     |"
	print "| Ionian (Major)  |  1  |"
	print "|     Dorian      |  2  |"
	print "|     Phrygian    |  3  |"
	print "|     Lydian      |  4  |"
	print "|     Mixolydian  |  5  |"
	print "| Aeolian (Minor) |  6  |"
	print "|     Locrian     |  7  |"
	print "|                 |     |"
	print "|_________________|_____|"
	print
	mode = raw_input("Choose a mode for your song: ")
		
	while mode.isdigit() != True or int(mode) < 0 or int(mode) > 7:
		print "Invalid Selection."
		mode = raw_input("Choose a scale (Please select a number from 1-7): ")
	mode = int(mode)
	title = raw_input("What do you want your song to be called? ")

def listen():
	print
	print "---Listening---"
	print
	queryUser()
	master = Vector("master")
	s = Song(root,mode,title)
	for i in range(num_measures):
		s.addMeasure(master)
	s.playSong()
	print
	print "This is the best song I know how to play!\n"	
	raw_input("Press any key to return to the main menu: ")	

def train():
	print
	print "---Training---"
	print
	queryUser()
	my_vector = Vector()
	s = Song(root,mode,title)
	for i in range(num_measures):
		training_vector = Vector("user")
		s.addMeasure(training_vector)
		s.playMeasure(title,i)
		
		user_opinion = raw_input("What did you think of that measure? (scale from 0-10): ")
		while user_opinion.isdigit() == False or int(user_opinion) < 0 or int(user_opinion) > 10:
			print "Invalid Response (please select a number from 0-10)"
			user_opinion = raw_input("What did you think of that measure? (scale from 0-10): ")
		user_opinion = int(user_opinion)
		training_vector = s.measures[i].getVector() # update in the case that we repeated
		my_vector.update(training_vector,.2,user_opinion)
	print "Here is your song!\n"
	s.playSong()	
	song_opinion = int(raw_input("How much did you like that song? (scale from 0-10): "))
	while song_opinion < 0 or song_opinion > 10:
		print "Please enter an integer between 0 and 10: "
		song_opinion = raw_input("How much did you like that song? (scale from 0-10): ")
		while song_opinion.isdigit() != False or int(song_opinion) < 0 or int(song_opinion) > 10:
			print "Invalid Response (please select a number from 0-10)"
			song_opinion = raw_input("How much did you like that song? (scale from 0-10): ")
		song_opinion = int(song_opinion)
	master = Vector("master")
	master.update(my_vector,.05,song_opinion)
	master.normalize()
	master.writeToFile(".master.vct")
	if user_opinion > 6 and num_measures > 7:
		my_vector.writeToFile(".user_vectors.vct")

def help():
	print
	print
	print
	print "Felix is an Intelligent music maker! If you would like to help Felix become better at making music, you can (T)rain it by offering your opinion on some measures (and ultimately, a song consisting of those measures) that Felix will create. Felix learns by reducing music into a series of properties, which are then used to inform its decision on how to construct each measure. If you like the measure, then Felix says, 'Hey! Those were some nice properties!', and remembers them. It's ultimately a bit more complicated then that, but thats the jist of it. If you would prefer, you can (L)isten to Felix's best representation of 'good' music (based on learning from past users). Felix will create an entire song for you; just sit back and enjoy!."
	print
	print "Created by Dave Abel and Elliot Mitchell at Carleton College"
	print
	print
	raw_input("Press any key to return to the main menu: ")
	main() 

def printMenu():
	print
	print "|--------|-----|"
	print "| Action | Key |"
	print "|--------|---- |"
	print "|        |     |"
	print "| Train  | (T) |"
	print "| Listen | (L) |"
	print "| Help   | (H) |"
	print "| Quit   | (Q) |"
	print "|        |     |"
	print "|________|_____|"
	print

def main():
	selection = raw_input("What would you like to do? ->")
	if selection == "l" or selection == "L" or selection == "listen" or selection == "Listen":
		listen()
		printMenu()
	elif selection == "t" or selection == "T" or selection == "train" or selection == "Train":
		train()
		printMenu()
	elif selection == "q" or selection == "Q" or selection == "quit" or selection == "Quit":
		quit()
	elif selection == "h" or selection == "H" or selection == "help" or selection == "Help":
		help()
		printMenu()
	else:
		print
		print "That was not a valid selection. Enter T to train, L to listen, H for help, or Q to quit. "
		print
	main() # Repeats!

if __name__ == "__main__":
	printMenu()
	print
	print "Welcome to Felix, the intelligent music maker!"
	print
	
	main()

