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
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	tweet = re.sub('[!;#$%&"\'()*+,-./:;<=>?\[\]^_`{|}~]', " ", tweet)	

#Convert @username to AT_USER
	tweet = re.sub('@[^\s]+','AT_USER',tweet)
#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)

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
	return line.strip()

training = []
mypath = sys.argv[1]
onlyfiles = [ f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]
for f in onlyfiles:
	f1 = os.path.join(mypath, f)
	for line in open(f1,'r'):
		line = line.replace("null$$$None$$$None$$$", "")
		line = line.replace("$$None$$$None$$$","").strip()
		processed = processTweet(line)
		training.append(processed)
		print(processed)

