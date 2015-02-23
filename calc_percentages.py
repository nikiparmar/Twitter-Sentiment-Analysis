import sys
from decimal import Decimal

f1 = open(sys.argv[1],'r')
i =0
max_val = 0.0
max_topic = 0
topics = dict()
for i in range(0, 41):
	topics[i] = 0
no = 0
vals = 1
k =0
total = 0
for line in f1:
	k+=1
	#print line
	if k < 2124:
		continue
	line = line.strip()
	if vals> 40:
		#print max_topic
		vals =1
		topics[max_topic] +=1
		max_topic = 0
		max_val = 0
		total +=1
	line = line.replace("[","").replace("]","")
	words = line.split()
	j = 1
	for w in words:
		#print w
		if w == "":
			continue
		if float(w) > max_val:
			max_val = float(w)
			max_topic = vals	
		vals +=1
	#vals +=1
#print topics
f1.close()

total+=1
print total
f2 = open(sys.argv[2],'w')
f1 =open(sys.argv[1])
k = 0
vals = 0
tno = 1
for line in f1:
	k +=1
	if k>=2124:
		break
	if k < 4:
		continue
	line = line.strip()
	if line == "":
		continue
	if "TOPIC" in line:
		if tno > 1:
			f2.write("\n")
		f2.write(str(tno) + "," + str((Decimal(topics[tno])*100)/Decimal(total)))
		tno +=1
	else:
		line = line.replace("(","").replace(")","").replace("'","")
		f2.write(","+line)

f2.close()
f1.close()
print tno		
