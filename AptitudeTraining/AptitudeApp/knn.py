import nltk
# nltk.download()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.neighbors import KNeighborsClassifier
fullword=[]
dclass=[]
import csv
# import these modules
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
ps = PorterStemmer()
# choose some words to be stemmed
# words = ["program", "programs", "programmer", "programming", "programmers"]
#
# for w in words:
# 	print(w, " : ", ps.stem(w))
file = open(r'C:\Users\ronsi\OneDrive\Desktop\Main Project\AptitudeTraining\static\skill.csv',encoding='utf-8')
type(file)
csvreader = csv.reader(file)
header = []
header = next(csvreader)
#print(header)
result_row=[]
num=['0','1','2','3','4','5','6','7','8','9','10']
rows = []
i=0
for row in csvreader:
    if i!=0:
        rows.append([row[0],row[1].lower().replace("-"," ")])
    i=i+1
#print(rows)
ii=0
for i in rows:

    example_sent = i[1]
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(example_sent)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            lis=[]
            my_string = w
            only_characters = ""
            for char in my_string:
                if char.isalpha():
                    if char!="-" and char!="-" and char not in num:
                        only_characters += char
                    else:
                        lis.append(only_characters)
                        only_characters = ""
                elif char==" ":
                    lis.append(only_characters)
                    only_characters=""
            else:
                lis.append(only_characters)
            #print(only_characters)
            # Output: "HelloWorld"
            for ww in lis:
                if len(ww)>=3:
                    w=ps.stem(w)
                    if w not in fullword:
                        fullword.append(w)
                    filtered_sentence.append(w)

    #print(word_tokens)
    print(i[0],"---->",' '.join(filtered_sentence))
    rr=[i[0],' '.join(filtered_sentence)]
    if i[0] not in dclass:
        dclass.append(i[0])
    result_row.append(rr)

import csv
# Define the data to be written to the CSV file
# Define the file name and location
filename = 'C://Users//ronsi//OneDrive//Desktop//Main Project//AptitudeTraining//static//example.csv'
# Open the file in write mode
with open(filename, 'w', newline='',encoding='utf-8') as file:
    # Create a CSV writer object
    writer = csv.writer(file)
    # Write the data to the CSV file
    writer.writerows(result_row)
# Print a message to confirm that the file has been written
print('The file "{filename}" has been written successfully!')
print(fullword)
print(dclass)
print(len(fullword))
print(len(dclass))
x=[]
y=[]
for i in result_row:
    y.append(dclass.index(i[0]))
    row=i[1].split(" ")
    xrow=[]
    for j in fullword:
        if j in row:
            xrow.append(1)
        else:
            xrow.append(0)
    x.append(xrow)
print((x[0]))
print(len(x))
import numpy as np
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(x,y, test_size=0.20)
model = KNeighborsClassifier(n_neighbors=2)

model.fit(X_train, y_train)

model.fit(X_train, y_train)

y=model.predict(X_test)
y2=model.predict(X_train)

from sklearn.metrics import accuracy_score
score =accuracy_score(y, y_test)
print(score)

score2 =accuracy_score(y2, y_train)
print(score2)

from sklearn.metrics import classification_report,confusion_matrix

cm = confusion_matrix(y_test, y)
print("confusion_matrix")
print(cm)

print("\nCR by library method=\n",
      classification_report(y_test, y))

def predict(txt):

    checkwd=[]
    word_tokens = word_tokenize(txt)

    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            lis = []
            my_string = w
            only_characters = ""

            for char in my_string:
                if char.isalpha():
                    if char != "-" and char != "-" and char not in num:
                        only_characters += char
                    else:
                        lis.append(only_characters)
                        only_characters = ""
                elif char == " ":
                    lis.append(only_characters)
                    only_characters = ""
            else:
                lis.append(only_characters)
            # print(only_characters)
            # Output: "HelloWorld"
            for ww in lis:
                if len(ww) >= 3:
                    w = ps.stem(w)
                    checkwd.append(w)

    xrow = []
    for j in fullword:
        if j in checkwd:
            xrow.append(1)
        else:
            xrow.append(0)
    y2 = model.predict([xrow])
    return dclass[y2[0]]


# print(predict("area interest deep learn c ontrol system design program python electr machineri web develop analyt technic activ hindustan aeronaut limit bangalor week guidanc satish senior engin hangar mirag fighter aircraft technic skill program matlab python java labview python webframework django flask ltspice intermedi languag mipow intermedi github gitbash jupyt notebook xampp mysql basic python softwar packag interpret anaconda python2 python3 pycharm java ide eclips oper system window ubuntu debian kali linux educ detail januari b.tech electr electron engin manip institut technolog januari deeksha center januari littl flower public school august manip academi higher data scienc data scienc electr enthusiast skill detail data analysi exprienc less year month excel exprienc less year month machin learn exprienc less year month mathemat exprienc less year month python exprienc less year month matlab exprienc less year month electr engin exprienc less year month sql exprienc less year monthscompani detail compani themathcompani descript current work casino base oper name disclos macau.i need segment custom visit properti base valu patron bring company.bas prove segment done much better way current system proper number back up.henceforth implement target market strategi attract custom add valu busi"))