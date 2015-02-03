import sys


f1 = open(sys.argv[1])
for line in f1:
	tweet = line.split(",")[0]
	print tweet
f1.close()
	
