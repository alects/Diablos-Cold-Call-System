from CourseSelect import *

def main():
	root = Tk()
	root.title("DIABLOS")
	w=200
	h=180
	ws = root.winfo_screenwidth() # width of the screen
	hs = root.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	root.geometry("%dx%d+%d+%d" % (w, h, x, y))
	rostHome = CourseSelect(master=root)
	rostHome.mainloop()
	root.destroy()
    

if __name__=="__main__":
    main()
