
MAJOR=0
MINOR=0
PATCH=01
DATA="20110518"
def getversion():
	return "%d.%02d.%04d"%(MAJOR,MINOR,PATCH)
def getlongversion():
	#TODO: add here some information
	return "uniPRCsim version %d.%02d.%04d (%s)"%(MAJOR,MINOR,PATCH,DATA)
