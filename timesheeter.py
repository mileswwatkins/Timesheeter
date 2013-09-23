#features left to add:
##allow use of HH:MM time in newentry()
##suggest user prints timesheet at 4:15 PM
##make robust to crashes from "bad" user input


from datetime import datetime, time, timedelta
from pprint import pprint
from copy import deepcopy

def calctimespent(start, end):
	timediff = round((end - start).seconds / 60. / 60., 1)
	return timediff
	
def printsheet (begintime, currentproj, timedict):
	temptimedict = deepcopy(timedict)
	timespent    = calctimespent(begintime, datetime.now())

	if temptimedict.has_key(currentproj):
		temptimedict[currentproj] = temptimedict[currentproj] + timespent
	else:
		temptimedict[currentproj] = timespent

	if temptimedict[currentproj] > 20:
		del(temptimedict[currentproj])
	
	pprint(temptimedict, width = 5)

def newentry (begintime, currentproj, timedict, recentprojs):
	temprecentprojs = recentprojs[:]
	temprecentprojs.append("Project not listed here")
	temprecentprojs.append("Take a break from work")
	print "\nWhat project are you starting to work on now? (Enter number)"
	for i in range(len(temprecentprojs)):
		print "%i) %s" % (i + 1, temprecentprojs[i])
	
	newproj = temprecentprojs[int(raw_input()) - 1]
	if newproj == "Project not listed here":
		newproj = raw_input("\nWhat is the name of the new project? ")
		recentprojs.append(newproj)
	if newproj == "Take a break from work":
		newproj = 'Break'
		
	newtime = int(raw_input("\nHow many minutes from now are you starting it? "))
		
	endtime = datetime.now() + timedelta(minutes = newtime)
	timespent = calctimespent(begintime, endtime)
	
	if timedict.has_key(currentproj):
		timedict[currentproj] = timedict[currentproj] + timespent
	else:
		timedict[currentproj] = timespent
		
	return (endtime, newproj, timedict, recentprojs)

def endofday (begintime, currentproj, timedict):
	finishtime = datetime.strptime(raw_input("\nWhat time are you going to leave? "), "%H:%M")
	timespent = calctimespent(begintime, finishtime)

	if timedict.has_key(currentproj):
		timedict[currentproj] = timedict[currentproj] + timespent
	else:
		timedict[currentproj] = timespent
	
	# try:
	# 	del(timedict['Break'])
	
	print "\n Here's your timesheet!\n"
	pprint(timedict, width = 5)

	print "\nHave a nice night!\n"
	return True


print "\nGood morning!"
begintime = datetime.strptime(raw_input("\nWhat time did you come in today? "), "%H:%M")
currentproj = raw_input("\nWhat project did you work on first? ")

timedict = {}
recentprojs = [currentproj]
isitover = False

while isitover == False:
	whichfunction = raw_input("""
What would you like to do? (Enter number)
1) Start work on a new project
2) Print current timesheet
3) Leave for the day
""")
	if whichfunction == '1':
		begintime, currentproj, timedict, recentprojs = newentry(begintime, currentproj, timedict, recentprojs)
	elif whichfunction == '2':
		printsheet(begintime, currentproj, timedict)
	elif whichfunction == '3':
		isitover = endofday(begintime, currentproj, timedict)
