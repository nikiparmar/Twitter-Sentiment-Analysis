import re, sys, htmlentitydefs
import os

emoticons_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""#, re.VERBOSE | re.I | re.UNICODE)

html_tags_string = r"""<[^>]+>"""
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"

emoticons_re = re.compile(emoticons_string, re.VERBOSE | re.I | re.UNICODE)
html_tags_re = re.compile(html_tags_string, re.VERBOSE | re.I | re.UNICODE)

def getStopWords(stopWordListFileName):
	stopWords = []
	fp = open(stopWordListFileName, 'r')
	for line in fp:
		line = line.strip()
		stopWords.append(line)
	fp.close()
	return stopWords

def getSlangWords(slangWordListFileName):
	slangWords = dict()
	word = []
	fp = open(slangWordListFileName, 'r')
        for line in fp:
                line = line.strip()
		word = line.split("\t")
		slangWords[word[0]] = word[1]

        fp.close()
	#print(slangWords)
        return slangWords


stopWords = getStopWords(sys.argv[2])
#slangWords = getSlangWords(sys.argv[3])

def html2unicode(self, s):
        """
        Internal metod that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        # First the digits:
	ents = set(html_entity_digit_re.findall(s))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    s = s.replace(ent, unichr(entnum))	
                except:
                    pass
        # Now the alpha versions:
        ents = set(html_entity_alpha_re.findall(s))
        ents = filter((lambda x : x != amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:            
                s = s.replace(ent, unichr(htmlentitydefs.name2codepoint[entname]))
            except:
                pass                    
            s = s.replace(amp, " and ")
        return s

def handleNotWords():
	return

#start process_tweet
def processTweet(tweet):

	#print(stopWords)
	tweet = tweet.strip()
#Convert www.* or https?://* to URL
	tweet = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',tweet)
#Replace #word with word
#	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
#	tweet = re.sub('[!;#$%&"\'()*+,-./:;<=>?\[\]^_`{|}~]', " ", tweet)	

#Convert @username to AT_USER
	tweet = re.sub('@[^\s]+','',tweet)
#Remove additional white spaces

# do something with slangs and apostrophe words!!!
#handle not words
	line = ""
	for word in tweet.split(" "):
		if html_tags_re.search(word):
			continue
		if emoticons_re.search(word):  #check for emoticons
			line += word + " "
			continue
		word = word.strip('!;#$%&"\'()*+,-./:;<=>?@[]^_`{|}~')
		#if word in slangWords:
		#	word = slangWords[word]
		if word in stopWords:
			continue
#elongated words
		word = re.sub(r'(.)\1{2,}',r'\1\1\1', word)
		line = line + word + " "
	line = re.sub('[\s]+', ' ', line)
	return line.strip()

global RETWEET_COUNT, DATE, ORIG_TWEET, TWEET_ID, SCREEN_NAME, NAME
global users, tweets

RETWEET_COUNT = 4
DATE = 2
ORIG_TWEET = 3
TWEET_ID = 1
SCREEN_NAME = 1
NAME = 2
FOLLOWERS = 3
FRIENDS = 4
NO_TWEETS = 5
TWEETS = 6



users = dict()
tweets = dict() 
mypath = sys.argv[1]
onlyfiles = [ f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]
for f in onlyfiles:
	f1 = os.path.join(mypath, f)
	for line in open(f1,'r'):
		line = line.replace("null$$$None$$$None$$$", "")
		line = line.replace("$$None$$$None$$$","").strip()
		fields = line.split("\t")
		length = len(fields)
		if length < 23:
			continue

		fields[19] = fields[19].replace("RT","")
		processed = processTweet(fields[19])
		created_date = fields[1]
				# remove RT and users
		if processed in tweets:
			if created_date < tweets[processed][DATE]:
				tweets[processed][DATE] = created_date
				tweets[processed][TWEET_ID] = fields[7]
				tweets[processed][ORIG_TWEET] = fields[10]
		else:
			tweets[processed] = dict()
			tweets[processed][RETWEET_COUNT] = 0
			tweets[processed][DATE] = created_date
                        tweets[processed][TWEET_ID] = fields[7]
			tweets[processed][ORIG_TWEET] = fields[19]
		#if "RT" in fields[10]:
		tweets[processed][RETWEET_COUNT] +=1

		if fields[21] not in users:
			users[fields[21]] = dict()
			users[fields[21]][SCREEN_NAME] = fields[20]
			users[fields[21]][NAME] = fields[22]
			users[fields[21]][NO_TWEETS] = 0
			users[fields[21]][TWEETS] = []
		#users[fields[21]][FOLLOWERS] = int(fields[length -1])
		#users[fields[21]][FRIENDS] = int(fields[length-2])
		users[fields[21]][NO_TWEETS] +=1
		users[fields[21]][TWEETS].append(processed)
		#friends and followers count, number of tweets

f1 = open(sys.argv[4],'w')
for twt in tweets:
	f1.write(twt + "\t" + tweets[twt][TWEET_ID] + "\t" +  tweets[twt][DATE]+  "\t" + tweets[twt][ORIG_TWEET] + "\t" +  str(tweets[twt][RETWEET_COUNT]) + "\n")
	f1.flush()

f1.close()

f2 = open(sys.argv[5],'w')
for u in users:
	f2.write(u + "\t" + users[u][SCREEN_NAME] + "\t" + users[u][NAME] + "\t" + str(users[u][NO_TWEETS]) + "\t" + str(users[u][TWEETS])+"\n")
	f2.flush()
f2.close()


found = 0
total =0
training = open(sys.argv[3],'r')
for line in training:
	line = line.strip()
	pos = line.find("{")
	twt = line[0:pos]
	val = line[pos:]
	val = eval(val.replace("array([[","").replace("]])",""))
	twt = twt.replace("RT","").replace("AT_USER","")
	twt = re.sub('[\s]+', ' ', twt)
	if twt in tweets:
		print twt + "\t" + tweets[twt][TWEET_ID] + "\t" +  tweets[twt][DATE] +  "\t" + tweets[twt][ORIG_TWEET] + "\t" +  str(tweets[twt][RETWEET_COUNT]) + "\t" + str(val[1]) + "\t" + str(val[2]) + "\t" + str(val[3]) + "\t" + str(val[4]) + "\t" + str(val[5]) + "\t" + str(val[6]) + "\t" + str(val[7]) + "\t" + str(val[8]) + "\t" + str(val[9]) + "\t" + str(val[10]) + "\t" + str(val[12])
		found +=1
	total +=1
print total
		
