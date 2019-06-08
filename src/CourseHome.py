from tkinter import *
from ColdCall import *
from Roster import *
from Flash import *


class CourseHome(Frame):

	def __init__(self, name = None, master=None):
		self.name = name
		'''
		Constructor
		'''
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		self.conn = sqlite3.connect('diablos.sqlite')
		master.bind('1', self.coldB['command'])
		master.bind('2', self.flashB['command'])
		master.bind('3', self.rosterB['command'])
		master.bind('q', self.BACK['command'])
		master.protocol("WM_DELETE_WINDOW", self.quit)

	def createWidgets(self):
		'''
		Creates the buttons for this Frame and organizes them
		'''
		self.header = Label(self, text = "{}".format(self.name), font = ("Courier",16))
		self.coldcall = "1. Start ColdCall"
		self.flashOne = "2. Start FlashPhotos"
		self.info = "3. Edit Course Roster"

		# Create the widgets
		self.coldB = Button(self, text = self.coldcall, command = self.createColdCall)
		self.flashB = Button(self, text = self.flashOne, command = self.createFlash)
		self.rosterB = Button(self, text = self.info, command = self.createRoster)
		self.BACK = Button(self, text = "BACK <q>", command = self.quit)
		self.BACK["fg"]   = "blue"

		# Organize the widgets
		self.header.pack({"side": "top"})
		self.coldB.pack({"side": "top"})
		self.flashB.pack({"side": "top"})
		self.rosterB.pack({"side": "top"})
		self.BACK.pack({"side": "top"})

	#Transition from course home to cold call game.
	def createColdCall(self):
		'''
		Creates the Cold Call Frame
		'''
		#Check to make sure the table contains >3 students. 
		cur = self.conn.cursor()
		cur.execute('SELECT count(*) FROM {}'.format(self.name.replace(" ", "_")),)
		rows = cur.fetchall()
		cur.close()

		if rows[0][0] > 3:
    			
			# Hide this Frame
			self.master.withdraw()
			root = Tk()
			root.title("{} ColdCall".format(self.name))

			#Center CC frame to window.
			w=600
			h=50
			ws = root.winfo_screenwidth() # width of the screen
			hs = root.winfo_screenheight()
			x = (ws/2) - (w/2)
			y = (hs) - (h/2)
			root.geometry("%dx%d+%d+%d" % (w, h, x, y))

			app = ColdCall(master=root, name=self.name)
			app.mainloop()
			root.destroy()
			self.master.deiconify()

		else:
    			messagebox.showwarning("OOPS!", "There aren't enough students in the class to benefit from this feature!")

	#Transition from course home to edit roster. 
	def createRoster(self):
		'''
		Same functionality as CourseSelect.createRoster(), but here we pass the course name in)
		'''
		# Hide this Frame
		self.master.withdraw()
		root = Tk()
		root.title("Course Info")

		#Center frame to window.
		w=200
		h=210
		ws = root.winfo_screenwidth() # width of the screen
		hs = root.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		root.geometry("%dx%d+%d+%d" % (w, h, x, y))

		app = Roster(master=root, name=self.name)
		app.mainloop()
		root.destroy()
		self.master.deiconify()

	#Transitions from the course home to Flash Card Game. 
	def createFlash(self):
		'''
		Creates the Flash Card Frame
		'''

		cur = self.conn.cursor()
		cur.execute("SELECT * FROM photos WHERE course=?", (self.name,))
		rows = cur.fetchall()
		cur.close()

		if rows:
			# Hide this Frame
			self.master.withdraw()
			root = Tk()
			root.title("{} FlashPhotos".format(self.name))

			#Center frame to window.
			w=2000
			h=650
			ws = root.winfo_screenwidth() # width of the screen
			hs = root.winfo_screenheight()
			x = (ws/2) - (w/2)
			y = (hs/2) - (h/2)
			root.geometry("%dx%d+%d+%d" % (w, h, x, y))

			app = Flash(master=root, name=self.name)
			app.mainloop()
			root.destroy()
			self.master.deiconify()
		else:
    			messagebox.showerror("OOPS!","Link your course photos to practice with FlashPhotos!")

