
MAJOR=0
MINOR=0
PATCH=15
DATE="20110531"
def getversion():
	return "%d.%02d.%04d"%(MAJOR,MINOR,PATCH)
def getlongversion():
	#TODO: add here some information
	return "uniPRCsim version %d.%02d.%04d (%s)"%(MAJOR,MINOR,PATCH,DATE)


if __name__ == "__main__":
	import time, re, os, sys
	import uniprcsimversion
	if 	os.system("zip -9 uniPRCsim-update%s.zip *.pyc *.py"%getversion()):
		sys.stderr.write("Cannot create zip file\n\n")
		sys.exit(1)
	if os.system("git commit -a"):
		sys.stderr.write("Cannot commit current version\n\n")
		sys.exit(1)
	if os.system("git tag \\\"v%s\\\""%getversion()):
		sys.stderr.write("Cannot tag current version\n\n")
		sys.exit(1)
	PATCH += 1
	DATE = time.strftime("%Y%m%d",time.localtime())
	fdr = open ("uniprcsimversion.py", "r")
	fdw = open ("nuniprcsimversion.py", "w")
	for line in fdr.readlines():
		fdw.write( re.sub("^DATE=\"\\d*\"","DATE=\"%s\""%DATE, re.sub("^PATCH=\\d*", "PATCH=%d"%PATCH,line ) ) )
	
	fdr.close()
	fdw.close()
	os.rename("nuniprcsimversion.py","uniprcsimversion.py")
