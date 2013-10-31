Felix© is an Artificial Intelligence that learns to create music. It was developed in Spring of 2012 by Dave Abel and Elliot Mitchell.

---Table Of Contents---

1. How to Run Felix

2. How Does Felix work?


---How To Run Felix---

You must have python installed, and you must have a built in media player for .mid files (Quicktime will do just fine). Additionally, you must call felix.py from BASH, as there are hardcoded bash commands to manipulate files. To run Felix©, simply run felix.py by enterring the command "python felix.py" in Terminal.

Options:

	Listening - Here you will be able to Listen to Felix create music dynamically, based on what is has learned from hundreds of past users.

	Training - Here you can contribute to the project! Felix will generate some measures for you, and you can provide feedback (either positive or negative) on those measures. Ultimately, these measures will be pasted into a song, and you will determine whether or not you like the song Felix has created for you. Felix will adjust its music making algorithm slightly based on your opinions.


---How Does Felix Work?---

Felix is based on a variant of a Self-Organizing Map, where each Vector in the map consists of weights from 0.0 - 1.0. Each weight (so each dimension of all vectors), represents a property of music that Felix uses to generate each measure. The properties we created were 'note_distance', 'repetition', 'chance to change octave', the ratio of 1's, 4's and 5's (of the scale) to 2's, 3's, 6's, and 7's, the chance to be a single note vs a chord, and the variety of the duration of notes per measure.

We provided implementation for converting a vector of property weights into a musical measure. No sound files were hard coded prior to Felix's creation.

We have stored several past 'good music' vectors from previous training trials in a past_vector File (called .user_vectors.vct). Each time Felix trains, it generates a random vector which we will call here the 'training_vector'. Then, Felix generates a measure based on a random vector from the past_vector File (these are vectors that previous users stated were 'good'). The trainer then listens to the measure created by that past_vector, and gives their opinion on that measure (a value from 0-10). Then, based on the trainer's opinion of that measure (and thus the past_vector), we shift the training_vector closer to (or further away from) the past_vector proprtionately to the trainer's likes (or dislikes). Then, Felix picks another random past_vector and generates another measure (based on the new past_vector). The trainer provides feedback once again, and shifts the training vector accordingly. This process repeats based on the number of measures, specified by the trainer. At the end, we play the full song (all the generated measures concatenated together) and prompt the trainer for their opinion. We then shift the master vector closer to (or farther away from) the training vector, proptionately to the users opinion of the song. If the user really enjoyed the song, their training vector will also be added to the list of user_vectors.vct.
