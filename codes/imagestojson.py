from subprocess import call
idd=""
text=""
with open("../dataset/long_new.json","r") as fi:
	for line in fi:
		if "\"@id" in line:
			idd=line[44:]
			idd=idd[:-3]
		elif "\"@value" in line:
			text=line[27:]
			text=text[:-2]
		print idd
		
		