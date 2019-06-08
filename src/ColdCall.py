from tkinter import *
from Table import *

class ColdCall(Frame):
	def __init__(self, name=None, master=None):
		'''
		Constructor
		'''
		self.name = name.replace(' ', '_')
		self.roster = Table(self.name)
		#self.roster.build_queue()
		Frame.__init__(self, master)
		self.q = self.roster.raise_queue()
		self.deck1, self.deck2, self.deck3 = self.q[0][0], self.q[1][0], self.q[2][0]
		self.pack()
		self.createWidgets()

		# Assign keybinds
		master.bind('1', self.slot1['command'])
		master.bind('2', self.slot2['command'])
		master.bind('3', self.slot3['command'])
		master.bind('q', self.BACK['command'])
		master.protocol("WM_DELETE_WINDOW", self.quit)

	def remove(self, n, event=None) :
		'''
		Function that gets called when you click a student in the queue
		or press their associated hotkey
		'''
		student, uoid = self.q.pop(n)
		self.roster.remove_student(uoid)
		self.update_names()		
		#used for debugging
		#print('{} has been removed from the queue!'.format(student))

	def createWidgets(self):
		'''
		Creates the buttons and orders them in the Frame
		'''
		# First queue position
		self.slot1 = Button(self, text = "1. "+self.deck1, command = lambda: self.remove(0))
		# Second queue position
		self.slot2 = Button(self, text = "2. "+self.deck2, command = lambda: self.remove(1))
		# Third queue position
		self.slot3 = Button(self, text = "3. "+self.deck3, command = lambda: self.remove(2))
		
		# Quit/Back button
		self.BACK = Button(self, text = "<q>", command = self.quit)
		self.BACK["fg"]   = "blue"
		
		# Organize the elements
		self.slot1.pack(padx=10, pady=10, side=LEFT)
		self.slot2.pack(padx=10, pady=10, side=LEFT)
		self.slot3.pack(padx=10, pady=10, side=LEFT)
		self.BACK.pack(side=RIGHT)

	def update_names(self) :
		'''
		Updates the student names on the three buttons
		'''
		# Get the updated queue
		self.q = self.roster.raise_queue()
		# Get new names on deck
		self.deck1, self.deck2, self.deck3 = '1. '+self.q[0][0], '2. '+self.q[1][0], '3. '+self.q[2][0]
		# Update button names
		self.slot1.config(text=self.deck1)
		self.slot2.config(text=self.deck2)
		self.slot3.config(text=self.deck3)