#Course Roster Generator
#Creates 3 random rosters to be used as sample_input for Diablos cold call program. 
#Team Diablos 04/15/19
#Random names generated from: https://randomwordgenerator.com/name.php.
#Random photos generated from https://google.github.io/cartoonset/download.html

import random
import os

first = []
last = []
students = []
uoids = []
i = 0
y = 0

#Create a list of first and a list of last names from random_names.txt
with open("random_names.txt", "r") as names:
    for name in names:
        name = name.split(' ')
        first.append(name[0])
        last.append(name[1])

#Builds an extremely large list of random studens with unique ids.

for f in first:
    for l in last:
        student = "{}\t{}\t{}{:06d}\t{}\t{}\t{}\t".format(f, l[:-1], "951", i, "sample@uni.edu","phonetic-spelling", "rev_cd")
        students.append(student)
        i+=1  

#Choose to have three courses generated randomly, or create custom sized/named courses to test edge cases.
print(len(students))
r = input("Generate three randomly named/sized rosters? Y/N\n")
for i in range(3): 
    if r =='N':
        n = input("Enter course number/name.\n")
        size = int(input("Enter number of students in course.\n"))
    else:
        n = "CIS_{}".format(random.randint(100, 599))
        size = random.randint(1, 100)
    name = "Sample_Roster_{}.txt".format(i+1)
    
    #Writing out sample course rosters to current folder.
     
    with open(name, "w+") as roster:
        roster.write(n+'\n')
        for i in range(size):
            stud= random.choice(students)
            roster.write(stud+"\n")
            s = stud.split("\t")
            uoids.append(s[2])
            
    print("Random sample roster generated and exported as {}:\n {}, {} students\n".format(name, n, size))

#Access random photos and rename them with all used uoids.

for filename in os.listdir("random_photos"):
    dst = "{}.png".format(uoids[y])
    src = 'random_photos/' + filename
    dst = 'random_photos/' + dst
    os.rename(src, dst)
    y+=1
    if y == len(uoids): break

print("All finished, find your sample rosters in current path.")






