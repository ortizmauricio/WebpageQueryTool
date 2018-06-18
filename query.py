from HTMLParser import HTMLParser
import string
import math
import zipfile
import re

currentFile = ''        
master_dictionary =  {}
doc_length = {}
doc_calculations = {}
doc_rank = {}

#Checks if string only contains letters
def only_letters(tested_string):
    if tested_string.isalpha():
        return True
    else:
        return False

#Inner structure for map
class Documents(object):
	def __init__(self):
		self.df = 1
		self.documents = {}

#Parses html file and filters out words, checks if the word has
#been registered, and either adds a document name if it hasn't been 
#registered, or increases a word/document frequency
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        p = re.compile(r"<.*?>|\W+|,\W*?|;\W*?")         
        data = p.split(data)
        for word in data:
            if only_letters(word):
                #print("Passed as word", word)
                if word in master_dictionary:
                	if currentFile in master_dictionary[word].documents:
	                    master_dictionary[word].documents[currentFile]+=1.0
	                else:
	                	master_dictionary[word].documents[currentFile] = 1.0
	                	master_dictionary[word].df+=1.0
                else:
                    master_dictionary[word] = Documents();
                    master_dictionary[word].documents[currentFile] = 1.0

parser = MyHTMLParser()

zip = zipfile.ZipFile('rhf.zip', 'r')

#Goes through every file and information to data structures
for fname in  zip.namelist():
	if fname.endswith(".html"):
	    currentFile = fname
	    doc_length[fname] = 0.0
	    doc_calculations[fname] = 0.0
	    doc_rank[fname] = 0.0
	    file = zip.open(fname, 'r')
	    lines = file.read().lower()
	    parser.feed(lines)

#Calculates document length, square root still needs to be taken
for word in master_dictionary:
	for file in master_dictionary[word].documents:
		doc_length[file] += math.pow((master_dictionary[word].documents[file] / master_dictionary[word].df), 2)

#Calculate numerator for ranked calculation
query = raw_input("Enter a query:")
query = query.split()
query_length = len(query)
for word in query:
	for file in master_dictionary[word].documents:
		doc_calculations[file] += (master_dictionary[word].documents[file] / master_dictionary[word].df)

#Calculates distance for specific file
for fname in doc_rank:
	doc_rank[fname] = (doc_calculations[fname]/(math.sqrt(doc_length[fname]) * math.sqrt(query_length)))

#Puts values into list of tuples for sorting and display in ranked order
ranked_values = []
for fname in doc_rank:
	if not doc_rank[fname] == 0:
		tup1 = (doc_rank[fname], fname)
		ranked_values.append(tup1)

ranked_values = sorted(ranked_values, reverse = True)

for value in ranked_values:
	print value