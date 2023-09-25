import re
from string import punctuation
import tqdm
#open all files in the folders and do something to it:
def openFiles(fn=None):
    import os
    problem = []
    # counts = {}
    for dir in os.listdir('datag/Gutenberg'):
        for file in tqdm.tqdm(os.listdir(os.path.join('datag/Gutenberg',dir))):
            file = os.path.join('datag/Gutenberg', dir + '/' + file) 
            with open(file, 'r+') as fp:
                text = fp.read()
                #do some preprocessing
                if fn :
                    fn(text, file, problem, fp)
                
    if problem != []:
        with open("problematic.txt", "a") as fp:
            fp.writelines(problem)
#get the no. of lines of the text 
def getLines(text, file, problem, fp):
    x = re.search("^Lines: *(\d+)", text, flags=re.MULTILINE)
    if not x:
        problem.append(str(file) + "\n")
    else:
        text = text.split("\n")
        text = text[len(text)-int(x.group(1)):]
        fp.seek(0)
        fp.truncate(0)
        fp.write('\n'.join(text))
    

def delEmail(text, file, problem, fp):
    regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    text = regex.sub(" ", text)
    fp.seek(0)
    fp.truncate(0)
    fp.write(text)

    
def delsapos(text,file, problem, fp):
    regex = re.compile(r"'s\W")
    text = regex.sub(" ", text)
    fp.seek(0)
    fp.truncate(0)
    fp.write(text)

def expandShrtfrms(text, file, counts, fp):
    # regex = re.compile(r"\w*n't\W")
    # #searching all the individual n't forms first to expand
    # all_shtfrm = regex.findall(text)
    # for w in all_shtfrm:
    #     try:
    #         counts[w] +=1
    #     except:
    #         counts[w] = 1
    # return counts
    # expanding the shortforms 
    full_forms = {
        r"\Wisn't\W": "is not",
        r"\Wdoesn't\W": "does not",
        r"\Wdon't\W":"do not",
        r"\Wcan't\W": "cannot",
        r"\Waren't\W": "are not",
        r"\Wweren't\W": "were not",
        r"\Wwouldn't\W": "would not",
        r"\Wdidn't\W": "did not",
        r"\Wshouldn't\W": "should not",
        r"\Wwasn't\W":"was not",
        r"\Wwon't\W" : "will not",
        r"\Wpshouldn't\W": "should not",
        r"\Wpdon't\W": "do not",
        r"\Wain't\W" : "I am not",
        r"\Whaven't\W" : "have not",
        r"\Wcouldn't\W": "could not",
        r"\Whasn't\W" : "has not",
        r"\Whadn't\W" : "had not",
        r"\W_didn't\W" : "did not",
        r"\Whavn't\W": "have not",
        r"\Wn't\W" : "",
        r"\Wjoin't\W": "joint",
        r"\Wdodn't\W": "did not",
        r"\Wisin't\W" : "is not",
        r"\Wneedn't\W" : "need not",
        r"\W_doesn't\W" : "does not",
        r"\W_don't\W" : "do not",
        r"\Wcann't\W" : "can not",
        r"\Wmustn't\W" : "must not",
        r"\W_can't\W" : "cannot",
        r"\Wwoundn't\W" : "would not",
    }
    text =text.lower()
    for k, w in full_forms.items():
        text = re.sub(k, " " + w + " ", text)
    fp.seek(0)
    fp.truncate(0)
    fp.write(text)

def removePunc(text, file, problem, fp):
    p = punctuation + '“”’‘'
    for punc in p:
        if (punc != "\\" and punc != "/" and punc != "-" and punc != "—"):
            text = text.replace(punc, "")
        else:
            text = text.replace(punc, " ")
        fp.seek(0)
        fp.truncate(0)
        fp.write(text)
        # print(text)
    
def delnxtLine(text, file, problem, fp):
    regex = re.compile(r"(\w|\W)(\n)")
    text = regex.sub(r'\1 ', text)
    fp.seek(0)
    fp.truncate(0)
    fp.write(text)


def replNo(text, file, problem, fp):
    text = re.sub('\d+', " NNN ", text)
    text = text.lower()
    fp.seek(0)
    fp.truncate(0)
    fp.write(text)
    
def replExtSpaces(text, file, problem, fp):
    text = re.sub('^ ', '', text, flags=re.MULTILINE)
    text = re.sub(' $', '',text, flags = re.MULTILINE)
    # text = re.sub('\t+', ' ', text)
    # text = re.sub('  +', ' ', text)
    fp.seek(0)
    fp.truncate(0)
    fp.write(text)    


def splitSentences():
    from nltk.tokenize import sent_tokenize
    def openFiles(fn=None):
        import os
        for dir in os.listdir('datag/Gutenberg'):
            for file in tqdm.tqdm(os.listdir(os.path.join('datag/Gutenberg',dir))):
                file = os.path.join('datag/Gutenberg', dir + '/' + file)
                with open(file, 'r+') as fp:
                    text = fp.read()
                    text = '\n'.join(sent_tokenize(text))
                    fp.seek(0)
                    fp.truncate(0)
                    fp.write(text)
                                           
    openFiles()
    
# def getFileName():
#     import os
#     files = []
#     for dir in os.listdir('datag/Gutenberg'):
#             for file in tqdm.tqdm(os.listdir(os.path.join('datag/Gutenberg',dir))):
                
#                 files.append(file)
#     for file in os.listdir('Gutenberg_original/Gutenberg/txt'):
#     #     for file in tqdm.tqdm(os.listdir(os.path.join('')))
#         if file not in files:
#             os.remove(os.path.join('Gutenberg_original/Gutenberg/txt/', file))

# getFileName()
# splitSentences()
# openFiles(delnxtLine)
# openFiles(replExtSpaces)
# openFiles(expandShrtfrms)
# openFiles(replNo)
# openFiles(removePunc)

