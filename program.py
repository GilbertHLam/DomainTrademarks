from urllib.request import urlopen
import csv
import time
import sys

	
def readTxtFiles():
	with open('words.txt') as f:
		listOfWords = f.readlines()
		listOfWords = [x.strip() for x in listOfWords] 

	with open('domains.txt') as f:
		listOfDomains = f.readlines()
		listOfDomains = [x.strip() for x in listOfDomains] 
		sep = '.'
		listOfDomains = [x.split(sep,1)[0] for x in listOfDomains] 
	f.close()
	goThroughList(listOfDomains, listOfWords)

def goThroughList(listOfDomains, listOfWords):
	i = 0
	for domain in listOfDomains:
		i = i +1
		determineTrademark(domain,domain)
		trial(domain, listOfWords)
		sys.stdout.write("\r%d%% done" % (listOfDomains.index(domain)*100/len(listOfDomains)))
		sys.stdout.flush()
	sys.stdout.write("\r100% done")
	sys.stdout.flush()

def determineTrademark(domain, term):
	try:
		url = "http://www.trademarkia.com/trademarks-search.aspx?tn=" + term
		fp = urlopen(url)
		mybytes = fp.read()
		html = mybytes.decode("utf8")
		if('This name is not found in our database of U.S. trademarks, so Apply for it Now.' not in html):
			outDomains.append(domain)
			outLinks.append(url)
		fp.close()
	except:
		print(term,': error')
		pass
	

def trial(domain, listOfWords):
	s = ''
	for i in range(0, len(domain)):
		if(domain[0:i] in listOfWords):
			s = ''
			s+=domain[0:i]
			s+='+'
			s+=domain[i:len(domain)]
			determineTrademark(domain,s)

outDomains = []
outLinks = []




readTxtFiles()
with open('out.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(outDomains, outLinks))

print('\nOpen out.csv to get your results')
