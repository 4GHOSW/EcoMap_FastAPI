import os,sys


f = open("pid.txt", "r")
lines = f.readlines()
f.close()

for line in lines:
	buf = line.split()[1]
	os.system("kill -9 "+buf)
	print(buf + " is killed !!")

f = open("pid.txt", "w")
f.writelines([])
f.close()

print("All gunicorn services are killed..")
