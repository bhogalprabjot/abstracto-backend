import spacy

nlp = spacy.load('en_core_web_sm') 

f = open("001.txt", "r")
article = f.read()

doc = nlp(article) 


"""
Split into sentences
"""
sentences = [sent.text.strip(' ') for sent in doc.sents if sent.text!=' ']
# sentences.clear(' ')
se = []
for s in sentences:
    if s != "\n\n":
        se.append(s)
    
# print(doc.sents.text)

print(se)
# for s in sentences:
#     print(s)
# print(doc.sents)