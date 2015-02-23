import sys

f1 = open(sys.argv[1])
f1.readline()
f1.readline()
training = open(sys.argv[2])
for line in training:
        line = line.strip()
	line1 = f1.readline().strip()
        words = line1.split("\t")
	if len(words)<2:
		continue
        val = eval(words[1].replace("array([[","").replace("]])",""))
	line = line.replace(",","")
	words2 = line.split("\t")
	if len(words2) != 5:
		continue
        print words2[0] +"," + words2[1] + "," + words2[2] + "," + words2[4] + "," + str(val[1]) + "," + str(val[2]) + "," + str(val[3]) + "," + str(val[4]) + "," + str(val[5]) + "," + str(val[6]) + "," + str(val[7]) + "," + str(val[8]) + "," + str(val[9]) + "," + str(val[10]) + "," + str(val[12])

