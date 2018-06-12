#Run this script after compiling the library. It will prepare the 'lib' folder
#needed by the host program.

import os
import shutil

#Folders:
incFolder = 'inc'
libFolder = 'lib'
submodulesFolders = ['flexsea-comm', 'flexsea-shared', 'flexsea-system', 'flexsea-projects', 'flexsea-dephy']
#Specific files:
specFileNameList = ['flexsea_board.h', 'flexsea_config.h', 'libFlexSEA-Stack-Plan.a']
specFileLocList = ['inc', 'inc', 'Release_static']

#Find all directories in this path (recursive):
def listDirectories(bp, dl):
	a = os.listdir()
	for i in range(0, len(a)):
		if(os.path.isdir(a[i]) and a[i] != '.git'):
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

def copyHeaderFiles(destPath, subm, d):
	entryPath = os.getcwd()	
	for u in range (0, len(d)):
		print("Calling chdir on:", d[u][1:])
		os.chdir(d[u][1:])
		currPath = os.getcwd()
		#print("Searching in", currPath)
		for file in os.listdir():
			if file.endswith(".h"):
				p = destPath + '\\' + subm + '\\' + d[u][1:]
				p = p.replace('/','\\')
				shutil.copy(file,p)
				print("Copied:", file, "to", p)
		
		os.chdir('..')
		os.chdir(entryPath) #Make sure to exit at the level we entered
	
#Main:
#===============================================

print("\n>>> Populate Lib Folder v0.1 <<<")
print("\n>>> ======================== <<<\n")
basePath = os.getcwd()
print(basePath)

#Prepare destination:
if not os.path.exists(libFolder):
	print('Created new libFolder')
	os.makedirs(libFolder)
else:
	print('Deleting existing libFolder and creating new (empty) version')
	shutil.rmtree(libFolder)
	os.makedirs(libFolder)

os.chdir(libFolder)
destPath = os.getcwd()
print('Destination path: ' + destPath + '\n')
os.chdir('..\..')	#Move to base folder

#Go through all submodules, find headers, and copy them to destination
print("\n>> Copy headers from submodules: <<\n")
for x in range(0,len(submodulesFolders)):
	os.chdir(submodulesFolders[x])
	currPath = os.getcwd()
	print("Searching in", currPath)
	dirList = []
	d = listDirectories('/',dirList)
	#print('dirList:',d)
	cleanList = removeDirWithoutHeaders(d)
	print('Directories with headers:',cleanList)
	createNewDirectories(destPath, submodulesFolders[x], cleanList)
	copyHeaderFiles(destPath, submodulesFolders[x], cleanList)
	os.chdir('..')
	print('\n')

#Handle specific file list:
os.chdir(basePath)
os.chdir('..')
#print(os.getcwd())
for y in range (0, len(specFileLocList)):
	f = specFileLocList[y] + '\\' + specFileNameList[y] 
	shutil.copy(f,destPath)

print("Done!")