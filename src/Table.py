import sqlite3

class Table :
	# Constructor
	def __init__(self, name) :
		'''
		name is the name that the table will have
		'''
		self.conn = sqlite3.connect('diablos.sqlite')
		self.name = name
		table_name = self.name.replace(" ", "_")
		self.name = table_name

	def data_entry(self, data) :
		'''
		Inserts the given data into a row in the table
		[first_name, last_name, uiod, phonetic, email, reveal_code, photo, queue, backup]
		          0          1     2         3      4            5      6      7       8
		'''
		cur = self.conn.cursor()
		# Insert data into the course table
		cur.execute('INSERT INTO '+self.name+' VALUES (?,?,?,?,?,?,NULL, NULL, NULL)',(data[0], data[1], data[2], data[3], data[4], data[5]))
		self.conn.commit()
		cur.close()

	def import_roster(self, file) :
		'''
		Reads the roster from the file
		'''
		cur = self.conn.cursor()		
		# Create new table for the roster
		cur.execute('DROP TABLE IF EXISTS '+self.name)
		cur.execute('CREATE TABLE '+self.name+'(first TEXT, last TEXT, uoid TEXT, phonetic TEXT, email TEXT, reveal_code TEXT, photo TEXT, queue INTEGER, backup INTEGER)')

		with open(file, 'r') as f :
			# skip the first line
			for i, line in enumerate(f, 1) :
				# split the line up into individual attributes
				data = line.rstrip().split('\t')
				# check if there are enough data points
				if (len(data) == 6) :
					self.data_entry(data)
		cur.close()

	def export_roster(self, path) :
		'''
		Creates a .txt file by the name of the table 
		'''
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM '+self.name)
		file_name = self.name.replace(" ", "_")
		file_path ="{}/{}.txt".format(path, file_name)
		print(file_path) 
		with open(file_path, 'w') as w :
			w.write('{}\n'.format(self.name))
			for row in cur :
				# Don't store photos or queue position in the .txt
				w.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(row[0], row[1], row[2], row[3], row[4], row[5]))
		cur.close()

	def build_queue(self, backup=False) :
		'''
		Randomly assigns values to the queue fields based on each student's position in queue
		'''
		cur = self.conn.cursor()
		# Move current queue to backup queue if called for
		if backup :
			cur.execute('SELECT * FROM '+self.name+' WHERE queue NOT NULL ORDER BY queue')
			out = cur.fetchall()
			for row in out :
				print(row)
				cur.execute('UPDATE '+self.name+' SET backup = (?) where uoid = (?)', (row[7],row[2]))
				self.conn.commit()
		# Create the primary queue
		cur.execute('SELECT * FROM '+self.name+' ORDER BY RANDOM()')
		out = cur.fetchall()
		for i, row in enumerate(out) :
			cur.execute('UPDATE '+self.name+' SET queue = (?) WHERE uoid = (?)', (i, row[2]))
			self.conn.commit()
		cur.close()

	def raise_queue(self) :
		'''
		Returns a list of student names that is ordered by their queue position in the database
		'''
		cur = self.conn.cursor()
		cur.execute('SELECT * FROM '+self.name+' WHERE backup NOT NULL ORDER BY backup')
		out = cur.fetchall()
		backup_queue = [('{} {}'.format(row[0], row[1]), row[2]) for row in out]

		# Create  list from queue column
		cur.execute('SELECT * FROM '+self.name+' WHERE queue NOT NULL ORDER BY queue')
		out = cur.fetchall()
		queue = [('{} {}'.format(row[0], row[1]), row[2]) for row in out]
		
		backup_queue.extend(queue)

		# Populate a new queue when there are three or fewer students remaining
		if len(queue) <= 3 : 
			self.build_queue(backup=True)
			# Create list from the backup queue
			cur.execute('SELECT * FROM '+self.name+' WHERE backup NOT NULL ORDER BY backup')
			out = cur.fetchall()
			backup_queue = [('{} {}'.format(row[0], row[1]), row[2]) for row in out]
			
			cur.execute('SELECT * FROM '+self.name+' WHERE queue NOT NULL ORDER BY queue')
			out = cur.fetchall()
			queue = [('{} {}'.format(row[0], row[1]), row[2]) for row in out]
			
			print("BACKUP", backup_queue)
			print('QUEUE', queue)
			backup_queue.extend(queue)
			cur.close()
			return backup_queue
		cur.close()
		return backup_queue

	def remove_student(self, uoid) :
		'''
		Removes a student from the queue
		'''
		cur = self.conn.cursor()
		cur.execute('SELECT backup FROM '+self.name+' WHERE uoid = (?)', (uoid,))
		out = cur.fetchall()
		if out[0][0] == None :
			cur.execute('UPDATE '+self.name+' SET queue = NULL WHERE uoid = (?)', (uoid,))
		else :
			cur.execute('UPDATE '+self.name+' SET backup = NULL WHERE uoid = (?)', (uoid,))
		self.conn.commit()
		cur.close()
		
