import os
import shutil

#Project status: code finds all relevant directories. No copying yet.

#Find all directories in this path (recursive):
def listDirectories(bp, dl):
	a = os.listdir()
	for i in range(0, len(a)):
		if(os.path.isdir(a[i])):
			dl.append(bp+a[i])
			#print('Found: '+bp+a[i])
			os.chdir(a[i])
			listDirectories('/'+a[i]+'/', dl)
			os.chdir('..')
	#print(dirList)
	return dl

def numOfDotH():
	n = 0
	for file in os.listdir():
		if file.endswith(".h"):
			n = n+1
	return n

#Takes a list of directories. If they have .h files keep them, otherwise remove them from the list
def removeDirWithoutHeaders(d):
	c = []
	entryPath = os.getcwd()
	#print('\n\n >>> removeDirWithoutHeaders:')
	for u in range (0, len(d)):
		#print("Calling chdir on:", d[u][1:])
		os.chdir(d[u][1:])
		currPath = os.getcwd()
		#print("Searching in", currPath)
		if numOfDotH():
			c.append(d[u])
		os.chdir('..')
		os.chdir(entryPath) #Make sure to exit at the level we entered
	return c
	#print('<<<<<<<<<<<')

#Creates new directories based on list
def createNewDirectories(destPath, subm, d):
	entryPath = os.getcwd()
	os.chdir(destPath)
	if not os.path.exists(subm):
		os.makedirs(subm)
	
	os.chdir(subm)
	currPath = os.getcwd()
	print("Working in", currPath)
	#At this point the submodule folder exists. Create sub-folders:
	for u in range (0, len(d)):
		if not os.path.exists(d[u][1:]):
			os.makedirs(d[u][1:])
	
	os.chdir(entryPath) #Make sure to exit at the level we entered

#Main:
#===============================================

print("\n>>> Populate Header Folder v0.1 <<<\n")
basePath = os.getcwd()
print(basePath)

submodulesDir = ['flexsea-comm', 'flexsea-shared', 'flexsea-system', 'flexsea-projects']

#Prepare destination:
directory = 'Headers'
if not os.path.exists(directory):
	print('Created new directory')
	os.makedirs(directory)
else:
	print('Deleting existing directory and creating new (empty) version')
	shutil.rmtree(directory)
	os.makedirs(directory)

os.chdir(directory)
destPath = os.getcwd()
print('Destination path: ' + destPath + '\n')
os.chdir('..\..')	#Move to base folder

#Main program: go through all submodules, find headers, and copy them to destination
for x in range(0,len(submodulesDir)):
	os.chdir(submodulesDir[x])
	currPath = os.getcwd()
	print("Searching in", currPath)
	dirList = []
	d = listDirectories('/',dirList)
	#print('dirList:',d)
	cleanList = removeDirWithoutHeaders(d)
	print('Clean list:',cleanList)
	createNewDirectories(destPath, submodulesDir[x], cleanList)
	os.chdir('..')
	print('\n')
