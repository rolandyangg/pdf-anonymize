# imports
import os.path
from os import path

active = True

# anonymize data for pdf files
def anonymizePDF(filename):
    print("PDF")

# anonymize data for txt files
def anonymizeTXT(filename):
    print("TXT")

# choice 1
def anonymizeData():
    invalid = True
    print("Place your file that you want to anonymize inside the root folder then enter the exact filename below (.pdf and .txt supported) (type 'exit' to exit)")
    while invalid:
        filename = input()
        filename = filename.lower().strip()
        if len(filename) > 4 and path.exists(filename): # make sure the len is enough and the file exists so no wacky slicing errors happen
            if filename[-4::] == ".txt":
                anonymizeTXT(filename)
                break
            elif filename[-4::] == ".pdf":
                anonymizePDF(filename)
                break
        elif filename == "exit":
            break
        print("Please enter a valid filename! (.pdf and .txt supported) (type 'exit' to exit)")

# main meat of the program
while active:
    print("Welcome to Data-Anonymizer!\nChoose a choice from the menu below:")
    print("1. Anonymize File Data")
    print("2. Exit")
    choice = input().strip()
    if choice == "1":
        anonymizeData()
    elif choice == "2":
        print("\nGoodbye!\n")
        active = False
    else:
        print("\nPlease input a valid input!\n")