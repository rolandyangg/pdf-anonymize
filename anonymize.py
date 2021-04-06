# imports
import os
import json
import fitz
from os import path, system, name
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, AnonymizerConfig

# setup variables
active = True
result_path = "./results/"

def clear():
    if name == "nt": # windows
        _ = system('cls')
    else: # mac
        _ = system('clear')

# gets the identified pii from a text
def get_pii(usertext):
    analyzer = AnalyzerEngine()
    detected_pii = analyzer.analyze(text=usertext, language='en')
    return detected_pii

# gets the generators to redact in the pdf
def get_generators(text):
    detected_pii = get_pii(text)
    for pii in detected_pii:
        pii_dict = pii.to_dict()
        pii_text = text[pii_dict['start']:pii_dict['end']]
        yield pii_text

# anonymized text for txt
def get_anonymized_text(usertext):
    engine = AnonymizerEngine()
    detected_pii = get_pii(usertext)
    anonymizer_results = engine.anonymize(text=usertext, analyzer_results=detected_pii)
    results = json.loads(anonymizer_results.to_json())
    return(results["text"])

# anonymize data for pdf files
def anonymize_pdf(filename, filepath):
    print("Anonymizing " + filename + "...")
    doc = fitz.open(filename)
    for page in doc:
        page.wrapContents()
        words_list = page.getText("words", flags=fitz.TEXT_INHIBIT_SPACES) # extract words and just append them together to get rid of weird spacing
        text = ""
        for word in words_list:
            text += word[4] + " "
        pii = get_generators(text)
        for data in pii:
            areas = page.searchFor(data)
            [page.addRedactAnnot(area, fill = (0, 0, 0)) for area in areas]
        page.apply_redactions()
    doc.save(filepath + filename[-len(filename):-4:] + " (REDACTED).pdf")
    print(filename + " has been anonymized! Check your results folder\n")

# anonymize data for txt files
def anonymize_txt(filename, filepath):
    print("Anonymizing " + filename + "...")
    ogFile = open(filename, "r")
    ogText = ogFile.read()
    ogFile.close()
    resultText = get_anonymized_text(ogText)
    resultFile = open(filepath + filename[-len(filename):-4:] + " (REDACTED).txt", "w+")
    resultFile.write(resultText)
    resultFile.close()
    print(filename + " has been anonymized! Check your results folder\n")

# anonymize data in bulk
def anonymize_bulk(foldername, filepath):
    ogPath = "./" + foldername + "/"
    if not path.exists(filepath):
        os.makedirs(filepath)
    for file in os.scandir(ogPath): 
        if file.is_file():
            if file.name.endswith(".pdf"):
                anonymize_pdf(ogPath + file.name, result_path)
            elif file.name.endswith(".txt"):
                anonymize_txt(ogPath + file.name, result_path)
            else:
                print(file.name + " is not a supported file type!\n")
        else:
            print(file.name + " is not a file!\n")

# choice 1
def anonymize_data():
    clear()
    invalid = True
    print("Place the data you want to anonymize in the cloned repo folder then time the filename/folder of data that you want to anonymize")
    print("Currently .pdf and .txt are supported")
    print("If you input a folder, it will only anonymize the supported file types")
    print("(type 'exit' to exit)")
    while invalid:
        choice = input().strip()
        filename = choice.lower()
        if len(filename) > 4 and path.isfile(filename): # make sure the len is enough and the file exists so no wacky slicing errors happen
            if filename[-4::] == ".txt":
                anonymize_txt(filename, result_path)
                break
            elif filename[-4::] == ".pdf":
                anonymize_pdf(filename, result_path)
                break
        elif path.isdir("./" + choice):
            anonymize_bulk(choice, result_path + choice)
            break
        elif filename == "exit":
            break
        clear()
        print("Please enter a valid filename/folder of data! (.pdf and .txt supported) (type 'exit' to exit)")

clear()

# main meat of the program
while active:
    print("Welcome to Data-Anonymizer!\nChoose a choice from the menu below:")
    print("1. Anonymize File Data")
    print("2. Change results folder")
    print("3. Exit")
    choice = input().strip()
    if choice == "1":
        anonymize_data()
    elif choice == "2":
        clear()
        print("WARNING: This may break the program if you input an incorrect file path, proceed with caution (type 'exit' to exit)")
        print("Current path: " + result_path)
        choice = input().strip()
        if len(choice) > 0 and not choice == 'exit':
            result_path = choice
            print("Result folder changed to: " + result_path + "\n")
    elif choice == "3":
        clear()
        print("Goodbye!")
        active = False
    else:
        clear()
        print("Please input a valid input!\n")