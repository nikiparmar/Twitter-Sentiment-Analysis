import sys
from datetime import datetime

date1 = datetime.strptime('Oct 2 2014 11:47PM','%b %d %Y %I:%M%p')
date2 = datetime.strptime('Nov 2 2014 12:00PM','%b %d %Y %I:%M%p')
date3 = datetime.strptime('Dec 2 2014 12:00PM','%b %d %Y %I:%M%p')
date4 = datetime.strptime('Jan 2 2014 12:00PM','%b %d %Y %I:%M%p')

tweets = []
tweets.append([])
tweets.append([])
tweets.append([])
tweets.append([])
tweets.append([])

t1 = open('modi_all_tweet1.tsv','w')
t2 = open('modi_all_tweet2.tsv','w')
t3 = open('modi_all_tweet3.tsv','w')
t4 = open('modi_all_tweet4.tsv','w')
t5 = open('modi_all_tweet5.tsv','w')

p1 = open('modi_processed_tweets1.tsv','w')
p2 = open('modi_processed_tweets2.tsv','w')
p3 = open('modi_processed_tweets3.tsv','w')
p4 = open('modi_processed_tweets4.tsv','w')
p5 = open('modi_processed_tweets5.tsv','w')

f1 = open(sys.argv[1])
for line in f1:
	line = line.strip()
	words = line.split("\t")
	if len(words) !=5:
		continue
	cdate = datetime.strptime(words[2], '%a %b %d %H:%M:%S +0000 %Y')
	if cdate < date1:
		t1.write(line +"\n")
		p1.write(words[0] +"\n")
		continue
	if cdate >= date1 and cdate< date2:
		t2.write(line +"\n")
		p2.write(words[0] +"\n")
		continue
	if cdate >= date2 and cdate< date3:
		t3.write(line +"\n")
		p3.write(words[0] +"\n")
		continue
	if cdate >= date3 and cdate<date4:
		t4.write(line +"\n")
		p4.write(words[0] +"\n")
		continue
	if cdate >= date4:
		t5.write(line +"\n")
		p5.write(words[0] +"\n")
		continue
f1.close()
t1.close()
t2.close()
t3.close()
t4.close()
t5.close()
p1.close()
p2.close()
p3.close()
p4.close()
p5.close()

