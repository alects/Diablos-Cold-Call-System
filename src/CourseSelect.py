from tkinter import filedialog
from tkinter import *
from CourseHome import *
from Table import *
import sqlite3 

class CourseSelect(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		
		self.pack()
		
		self.conn = sqlite3.connect('diablos.sqlite')
		cur = self.conn.cursor()
		cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
		alltables = cur.fetchall()
		self.one = "Add Class" #name of the first button
		self.two = "Add Class"
		self.three = "Add Class"
		tablenames = []
		cur.close()

		for table in alltables:
			if(table[0] != "photos"):
				tablenames.append(table[0].replace("_", " "))
		name_count = len(tablenames)
		if(name_count > 0):
			self.one = tablenames[0]
		if(name_count > 1):
			self.two = tablenames[1]
		if(name_count > 2):
			self.three = tablenames[2]
		# Create Widgets must be called AFTTER
		# All attributes are made
		self.createWidgets()

		#print(alltables)
		# Assign keybinds
		master.bind('1', self.slot1['command'])
		master.bind('2', self.slot2['command'])
		master.bind('3', self.slot3['command'])
		master.bind('q', self.QUIT['command'])
		master.protocol("WM_DELETE_WINDOW", self.quit)

	def course(self, name, event=None) :
		'''
		Function that gets called when you select a course. If adding course go to Roster window.  If clicking on preexisting course got to the CourseHome. 
		'''
		if (name=="Add Class"):
			self.createRoster()
		else:
			self.createCourseHome(name)
		
	def createRoster(self):
		'''
		Builds the Edit Roster Frame
		'''
		# Hide this Frame
		self.master.withdraw()
		# Build Edit Roster
		root = Tk()
		root.title("Create Course")

		#Center frame to window.
		w=200
		h=210
		ws = root.winfo_screenwidth() # width of the screen
		hs = root.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		root.geometry("%dx%d+%d+%d" % (w, h, x, y))

		app = Roster(master=root)
		app.mainloop()
		root.destroy()
		self.master.deiconify()	
	
	def createCourseHome(self, name):
		'''
		Builds the Course Home Frame
		'''
		# Hide this Frame
		self.master.withdraw()
		root = Tk()
		root.title("Course Home")

			#Center frame to window.
		w=200
		h=180
		ws = root.winfo_screenwidth() # width of the screen
		hs = root.winfo_screenheight()
		x = (ws/2) - (w/2)
		y = (hs/2) - (h/2)
		root.geometry("%dx%d+%d+%d" % (w, h, x, y))
		
		rostHome = CourseHome(master=root, name=name)
		rostHome.mainloop() 
		root.destroy()
		self.master.deiconify()

	def createWidgets(self):
                '''
                Creates the buttons for this Frame and organizes them
                '''
                self.header = Label(self, text = "Select Course:", font = ("Courier",16))

                # Course 1
                self.slot1 = Button(self, text = "1. "+self.one, command = lambda: self.course(self.one))
                # Course 2
                self.slot2 = Button(self, text = "2. "+self.two, command = lambda: self.course(self.two))
                # Course 3
                self.slot3 = Button(self, text ="3. "+ self.three, command = lambda: self.course(self.three))
                # Quit button
                self.QUIT = Button(self, text = "QUIT <q>", command = self.quit)
                self.QUIT["fg"]   = "red"
                
                # Organize elements
                self.header.pack({"side": "top"})
                self.slot1.pack({"side": "top"})
                self.slot2.pack({"side": "top"})
                self.slot3.pack({"side": "top"})
                # Note that while the syntax is different, it does
                # the exact same thing as the above
                self.QUIT.pack({"side": "top"})
           
