from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
from tkinter import messagebox
from Table import * 
import os

class Roster(Frame):
        """
        The roster window shows the roster, course info,
        and allows the roster to be edited.

        """
        def __init__(self, name = None, master=None):
                '''
                Constructor
                '''
                self.name = name
                Frame.__init__(self, master)
                self.pack()
                self.conn = sqlite3.connect('diablos.sqlite')
                self.createWidgets()
                # Assign keybinds
                master.bind('1', self.rosterE['command'])
                master.bind('2', self.importPhotos['command'])
                master.bind('3', self.removeE['command'])
                master.bind('4', self.exportE['command'])
                master.bind('q', self.BACK['command']) 
                master.protocol("WM_DELETE_WINDOW", self.quit)

        def createWidgets(self):
                '''
                Creates the buttons for this Frame and organizes them
                '''
                if self.name == None:
                        header = "Create New"
                else:
                        header = "{}".format(self.name)
                self.header = Label(self, text = header, font = ("Courier", 16))
                # Create Buttons
                self.rosterE = Button(self, text = "1. Edit Roster", command = lambda: self.edit_roster("dummy"))
                self.importPhotos = Button(self, text = "2. Import Photos", command = lambda: self.import_photos("dummy"))
                self.removeE = Button(self, text= "3. Remove Course", command = lambda: self.remove_course("dummy"))
                self.exportE = Button(self, text= "4. Export Roster", command = lambda: self.export_roster("dummy"))
                
                # Quit button
                self.BACK = Button(self, text = "BACK <q>", command = self.quit)
                self.BACK["fg"]   = "blue"
                
                # Organize the elements
                self.header.pack({"side": "top"})
                self.rosterE.pack({"side": "top"})
                self.importPhotos.pack({"side": "top"})
                self.removeE.pack({"side": "top"})
                self.exportE.pack({"side": "top"})
                self.BACK.pack({"side": "top"})

        def edit_roster(self, value, event=None): #find file path and extract data
                '''
                1. Edit/create new course name (optional).
                2. Import roster (optional).
                '''
                old_name = self.name 
                temp_name = simpledialog.askstring("Course Name", "Enter the name of the course:\n(ex. CIS 422)\n If you are not updating name select cancel to import roster.")
                #Check if course name is being updated, update course name only at first.
                if temp_name:
                        self.name = temp_name
                        if old_name!=None: 
                                cur = self.conn.cursor()
                                table_name = old_name.replace(" ", "_")
                                cur.execute('SELECT name FROM sqlite_master WHERE type=? AND name=?;', ['table', table_name]);
                                table = cur.fetchall()
                                if table:
                                        new_name = self.name.replace(" ", "_")
                                        cur.execute('ALTER TABLE {} RENAME TO {}'.format(table_name, new_name))        
                                        self.conn.commit()
                                cur.close()
                
                #Need a course name when initializing course. 
                if self.name == None:
                        messagebox._show("OOPS", "Need a course name to import roster!")
                
                #Importing roster file at path to table self.name.
                else:
                        path = filedialog.askopenfilename(initialdir = "src/", title = "Choose roster file(.txt) for {}.".format(self.name), filetypes =[('text files','.txt')])
                        if len(path) != 0:
                                course_table = Table(self.name)
                                course_table.import_roster(path)
                                messagebox.showinfo("Information", "Please restart Diablos to implement changes.")
                        #No path was entered/ roster imported.
                        elif self.name == old_name:
                                messagebox._show("OOPS!", "No changes being made!")
                        elif old_name==None:
                                messagebox._show("OOPS!", "Import a roster to add course! \nNo changes being made!")
                        else:
                                #Just renaming course here. 
                                messagebox._show("OOPS!", "No import roster selected!")
                                messagebox.showinfo("Information", "Please restart Diablos to implement changes.")

        def import_photos(self, value, event=None):
                '''
                Asks the user to select the folder containing the student photos
                '''
                print("Import Photos: {}".format(value))
                # Get the photo directory
                path = askdirectory()
                cur = self.conn.cursor()
                # Store the photo directory
                cur.execute('CREATE TABLE IF NOT EXISTS photos (course TEXT, dir TEXT)')
                #Check to see if you need to replace pre-existing path in photos.
                cur.execute('SELECT * FROM photos WHERE course=?', (self.name,))
                pre_pho = cur.fetchall()
                if len(pre_pho) != 0:
                        cur.execute('DELETE FROM photos WHERE course=?', (self.name,))
                cur.execute('INSERT INTO photos VALUES (?, ?)', (self.name, path))
                self.conn.commit()
                cur.close()
                #files = os.listdir(path)
                #for file in files :
                #       if file[-4:] != '.jpg' :
                #               files.remove(file)

        def remove_course(self, event=None) :
                '''
                Remove course table from database.
                '''
                if (self.name == None):
                        messagebox.showwarning("Warning", "There is no course to remove!")
                else:
                        pos = messagebox.askokcancel("Question", "Are you sure you want to remove {}?".format(self.name))
                        if (pos):
                                cur = self.conn.cursor()
                                table_name = self.name.replace(" ", "_")
                                cur.executescript('DROP TABLE IF EXISTS ' +table_name)
                                self.conn.commit()
                                
                                #Remove course photo directory.
                                cur.executescript('SELECT * FROM photos WHERE course=?', (self.name,))
                                pre_pho = cur.fetchall()
                                if len(pre_pho) != 0:
                                        cur.execute('DELETE FROM photos WHERE course=?', (self.name,))
                                        self.conn.commit()
                                
                                cur.close()
                        messagebox.showinfo("Information", "Please restart Diablos to implement changes.")
        
        def export_roster(self, event=None):
                '''
                Export Roster from db table self.name to .txt file in local path. 
                '''
                if (self.name!=None):
                        path = askdirectory()
                        if len(path)!= 0:
                                file_name = self.name.replace(" ", "_")
                                messagebox.showinfo("Information", "Your roster path: \n {}/{}".format(path, file_name))
                                course_table = Table(self.name)
                                course_table.export_roster(path)
                        else:
                                messagebox._show("OOPS!", "No file path selected!")
                else:
                        messagebox._show("OOPS!", "No roster to export!")                