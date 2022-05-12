
from flask import Flask, render_template, request
import pandas as pd
import os
import json
import pandas as pd
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker
import language_tool_python 
import collections
from collections import defaultdict

app = Flask(__name__)
# new_model = load_model('./models/best_model.h5')

@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


# @app.route('/features')
# def features():
#     return render_template('features.html')


def getPDFinfo():
    # imagefile = request.files['imagefile']
    # image_path = "./images/img/" + imagefile.filename
    # read_pdf = PyPDF2.PdfFileReader("./images/img/" + imagefile.filename)
    folder_path = (r'./images/img/')
    print('FOlder Path is: ')

    test = os.listdir(folder_path)
    for pdf in test:
        if pdf.endswith(".pdf"):
            os.remove(os.path.join(folder_path, pdf))

    imagefile = request.files['imagefile']
    image_path = "./images/img/" + imagefile.filename
    imagefile.save(image_path)

    print(imagefile)
    per = 'Done with post'

    imagefile = request.files['imagefile']
    image_path = "./images/img/" + imagefile.filename
    print(image_path)
    return {'imagefile':imagefile,'image_path':image_path,'read_pdf':read_pdf}


@app.route('/', methods=['POST'])
def detect():
    
    # folder_path = (r'./images/img/')

    # test = os.listdir(folder_path)
    # for pdf in test:
    #     if pdf.endswith(".pdf"):
    #         os.remove(os.path.join(folder_path, pdf))

    # imagefile = request.files['imagefile']
    # image_path = "./images/img/" + imagefile.filename
    # imagefile.save(image_path)

    # print(imagefile)
    # per = 'Done with post'

    # pdf_file = open('Project/Aditya_resume_new.pdf', 'rb')
    
    # return render_template('index.html', prediction=per)
    folder_path = (r'./images/img/')

    test = os.listdir(folder_path)
    for pdf in test:
        if pdf.endswith(".pdf"):
            os.remove(os.path.join(folder_path, pdf))

    imagefile = request.files['imagefile']
    image_path = "./images/img/" + imagefile.filename
    imagefile.save(image_path)

    print(imagefile)
    per = 'Done with post'

    imagefile = request.files['imagefile']
    image_path = "./images/img/" + imagefile.filename
    print(image_path)

    # pdf_file = open('images/img/Aditya_resume_new.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader("./images/img/" + imagefile.filename)
    num_of_pages = read_pdf.getNumPages()
    print(num_of_pages)
    
    return render_template('index.html', prediction=num_of_pages)

@app.route('/deepfakeapi', methods=['POST'])
def detect_deepfake():
    
    folder_path = (r'./images/img/')

    test = os.listdir(folder_path)
    for images in test:
        if images.endswith(".pdf"):
            os.remove(os.path.join(folder_path, images))

    imagefile = request.files['imagefile']
    image_path = "./images/" + imagefile.filename
    imagefile.save(image_path)

    # test_datagen1 = ImageDataGenerator(
    #     rescale = 1/255  
    # )

    # test_generator1 = test_datagen1.flow_from_directory(
    #     directory = './images/',
    #     classes=['img'],
    #     target_size = (128, 128),
    #     color_mode = "rgb",
    #     class_mode = None,
    #     batch_size = 1,
    #     shuffle = False
    #     )

    # test_generator1.reset()

    # preds = new_model.predict(
    #     test_generator1,
    #     verbose = 1
    # )

    # test_results = pd.DataFrame({
    #     "Filename": test_generator1.filenames,
    #     "Prediction": preds.flatten()
    # })    

    # per = str(float(test_results['Prediction'][0]) * 100)
    per = 'Done again'
    
    return json.dumps({'Percentage': "{}".format(per)})

@app.route('/stopwords', methods=['GET'])
def model_info():
    return json.dumps(stopwords.words('english'))

# @app.route('/getpdfinfo', methods=['GET'])
# def getpdfData():
#     getinfo = getPDFinfo()
#     # print()
#     # read_pdf = PyPDF2.PdfFileReader("./images/img/" + imagefile.filename)
#     # page = read_pdf.getPage(0)
#     # page_content = page.extractText()
#     # print(page_content)
#     return getinfo


@app.route('/getpdfinfo', methods=['POST'])
def getpdfData():

    folder_path = (r'./images/img/')

    test = os.listdir(folder_path)
    for images in test:
        if images.endswith(".pdf"):
            os.remove(os.path.join(folder_path, images))

    imagefile = request.files['imagefile']
    image_path = "./images/img/" + imagefile.filename
    imagefile.save(image_path)

    pdf_file = open(image_path, 'rb')

    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    
    page = read_pdf.getPage(0)
    page_content = page.extractText()

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~ŁŒ'''

    for ele in page_content:
        if ele in punc:
            page_content = page_content.replace(ele, "")

    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(page_content)

    filtered_resume = [w for w in word_tokens if not w.lower() in stop_words]

    filtered_resume = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_resume.append(w)

    spell = SpellChecker()

    misspelled = spell.unknown(word_tokens)

    misspelled_words = {}

    for word in misspelled:
        misspelled_words[word] = spell.correction(word)

    # print(misspelled_words)

    #grammar check
    my_tool = language_tool_python.LanguageTool('en-US')  
    my_text = page_content
    # getting the matches  
    my_matches = my_tool.check(my_text)  
    
    # defining some variables  
    myMistakes = []  
    myCorrections = []  
    startPositions = []  
    endPositions = []  
    grammarchk_dict = {}
    
    # using the for-loop  
    for rules in my_matches:  
        if len(rules.replacements) > 0:  
            startPositions.append(rules.offset)  
            endPositions.append(rules.errorLength + rules.offset)  
            myMistakes.append(my_text[rules.offset : rules.errorLength + rules.offset])  
            myCorrections.append(rules.replacements[0])  
            
    
    # creating new object  
    my_NewText = list(my_text)   
    
    # rewriting the correct passage  
    for n in range(len(startPositions)):  
        for i in range(len(my_text)):  
            my_NewText[startPositions[n]] = myCorrections[n]  
            if (i > startPositions[n] and i < endPositions[n]):  
                my_NewText[i] = ""  
    
    my_NewText = "".join(my_NewText)  

    grammar_list = list(zip(myMistakes, myCorrections))

    for mistake,correction in grammar_list:
        grammarchk_dict[mistake] = spell.correction(correction)

    # print(grammarchk_dict)


    #repetitive words
    a = page_content

    # Instantiate a dictionary, and for every word in the file, 
    # Add to the dictionary if it doesn't exist. If it does, increase the count.
    wordcount = {}
    # To eliminate duplicates, remember to split by punctuation, and use case demiliters.
    for word in a.lower().split():
        if word not in stop_words:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    # Print most common word
    # n_print = int(input("How many most common words to print: "))
    # print("\nThe {} most common words are as follows\n".format(n_print))
    common_words = {}
    word_counter = collections.Counter(wordcount)
    for word, count in word_counter.most_common(10):
        common_words[word] = count

    # print(common_words)

    #quantitative words
    # quan_dict = {"Quantitative_words": []}
    quan_list = []
    # d = defaultdict(list)
    a = page_content

    quan_stopwords = set(line.strip() for line in open('stopwords_quan.txt'))

    for word in a.lower().split():
        if word in quan_stopwords:
            # quan_stopwords['Quantitative_words'].append(word)
            quan_list.append(word)

    print(quan_list)

    return json.dumps(misspelled_words)


# @app.route('/modeloverview', methods=['GET'])
# def model_chart_info():
#     stringlist = []
#     new_model.summary(print_fn=lambda x: stringlist.append(x))
#     short_model_summary = "\n".join(stringlist)
#     return json.dumps(stringlist)


if __name__ == '__main__':
    app.run(port=4000, debug=True)