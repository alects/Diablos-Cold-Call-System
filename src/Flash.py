from tkinter import *
import sqlite3
import os
import random 

class Flash(Frame):
	"""
	This window will be used to quiz the instructor
	on students names via their photos.

	"""
	
	def __init__(self, name=None, master=None):
		'''
		Constructor
		'''
		Frame.__init__(self, master)
		self.name = name
		self.master = master
		self.conn = sqlite3.connect('diablos.sqlite') #connect to database
		cur = self.conn.cursor()
		cur.execute("SELECT * FROM photos WHERE course=?", (self.name,)) #first query to return the path of the photo directory associated with chose course
		row = cur.fetchall()
		self.path = row[0][1] #sets our class variable path equal to the photo directory path gets called later to find photos
		
		self.photos = [] #array variable that will eventually hold our full paths to each photo for a class

		self.ids = [] #will be used to store the ids from the course that we will eventually query 
		table_name = self.name.replace(" ", "_")

		#Create a list of uoids from course table. 
		id_list = cur.execute('SELECT uoid FROM {}'.format(table_name)).fetchall() #queries diablos for all 95 numbers
		for id in id_list:
			self.ids.append(id[0]) #adds the id numbers to our previously defined array 'ids'

		#Create a list of photo directories for course students. 		
		for filename in os.listdir(self.path):
			if filename.endswith(".png"):
				f = os.path.splitext(filename)[0]
				if f[-9:] in self.ids: #checks the self.ids array to make sure that a photo is in our class before adding it to the list of class photos 
					self.photos.append(self.path+"/"+filename)

		random.shuffle(self.photos) #we add some randomness to ensure the teacher never gets used to the same three faces next to each other
		self.pic = PhotoImage(master=master,file=self.photos[0]) #this renders the photo at the photo absolute path that we saved previously
		self.pic1 = PhotoImage(master=master,file=self.photos[1])#the photo after it after being randomized
		self.pic2 = PhotoImage(master=master,file=self.photos[2])#the photo after that
		self.flipped = True #This global variable helps implement the 'reveal' feature of the game 
		self.pack()
		self.createWidgets()
		master.bind('q', self.BACK['command'])
		master.bind('<space>', self.flip['command'])
		master.protocol("WM_DELETE_WINDOW", self.quit)
		# master.bind('1', self.rosterS['command'])


	def update_names(self):
		#random.shuffle(self.photos)
		first = os.path.splitext(self.photos[0])[0]
		first = first[-9:]
		second = os.path.splitext(self.photos[1])[0]
		second = second[-9:]
		third = os.path.splitext(self.photos[2])[0]
		third = third[-9:]
		output = []
		output1 = []
		output2 = []
		cur = self.conn.cursor()
		table_name = self.name.replace(" ", "_")
		cur.execute("SELECT * FROM {} WHERE uoid=?".format(table_name), (first,))
		rows = cur.fetchall()
		output.append(rows[0][0]+ " ")
		output.append(rows[0][1]+ " ")
		output.append(rows[0][4])
		cur.execute("SELECT * FROM {} WHERE uoid=?".format(table_name), (second,))
		rows = cur.fetchall()
		output1.append(rows[0][0]+ " ")
		output1.append(rows[0][1]+ " ")
		output1.append(rows[0][4])
		cur.execute("SELECT * FROM {} WHERE uoid=?".format(table_name), (third,))
		rows = cur.fetchall()
		output2.append(rows[0][0]+ " ")
		output2.append(rows[0][1]+ " ")
		output2.append(rows[0][4])

		return [output, output1, output2]


	def flip_deck(self, event=None):
		if self.flipped == False:
			random.shuffle(self.photos)
			self.pic = PhotoImage(master=self,file=self.photos[0])
			self.pic1 = PhotoImage(master=self,file=self.photos[1])
			self.pic2 = PhotoImage(master=self,file=self.photos[2])
			self.card0.config(image=self.pic, text="")
			self.card1.config(image=self.pic1, text="")
			self.card2.config(image=self.pic2, text="")
			self.flipped = True
		else:
			output = self.update_names()
			first = output[0]
			second = output[1]
			third = output[2]
			self.card0.config(text=first[0]+first[1]+"\n"+first[2])
			self.card1.config(text=second[0]+second[1]+"\n"+second[2])
			self.card2.config(text=third[0]+third[1]+"\n"+third[2])
			self.flipped = False

	def createWidgets(self):
		'''
		Creates the buttons for this Frame and organizes them
		'''
		self.header = Label(self, text = "FLASH CARDS", font = ("Courier",20))

		self.flip = Button(self, text = "FLIP DECK", command = lambda: self.flip_deck())
		self.card0 = Button(self,image= self.pic, text = None, compound = TOP)
		self.card1 = Button(self,image= self.pic1, text = None, compound = TOP)
		self.card2 = Button(self,image= self.pic2, text = None, compound = TOP)
		# Quit button
		self.BACK = Button(self, text = "BACK <q>", command = self.quit)
		self.BACK["fg"]   = "blue"
		
		# Organize the elements
		self.header.pack({"side": "top"})
		self.card0.pack(padx=10, pady=10, side=LEFT)
		self.card1.pack(padx=10, pady=10, side=LEFT)
		self.card2.pack(padx=10, pady=10, side=LEFT)
		self.BACK.pack({"side": "left"})
