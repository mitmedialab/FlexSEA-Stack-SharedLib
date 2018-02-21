import os
import shutil

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
	#print('\n\n >>> removeDirWithoutHeaders:')
	for u in range (0, len(d)):
		os.chdir(d[u][1:])
		currPath = os.getcwd()
		#print("Searching in", currPath)
		if numOfDotH():
			c.append(d[u])
		os.chdir('..')
	return c
	#print('<<<<<<<<<<<')

print("\nPopulate Header Folder v0.1\n")
basePath = os.getcwd()
print(basePath)

submodulesDir = ['flexsea-comm', 'flexsea-shared', 'flexsea-system', 'flexsea-user']

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
	print('dirList:',d)
	cleanList = removeDirWithoutHeaders(d)
	print('Clean list:',cleanList)
	os.chdir('..')
	print('\n')
