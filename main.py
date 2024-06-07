'''
title: sort article data
author: Ayaan Merchant (ayaan.merchant08@gmail.com)
date-created: 2024-06-06
notes:
    This program assumes the given CSV file was exported from Zoterro, has not yet been cleaned or sanitized in any way 
    and is in the table format: 
    ["Key","Item Type","Publication Year","Author","Title","Publication Title","ISBN","ISSN","DOI","Url","Abstract Note","Date","Date Added","Date Modified","Access Date","Pages","Num Pages","Issue","Volume","Number Of Volumes","Journal Abbreviation","Short Title","Series","Series Number","Series Text","Series Title","Publisher","Place","Language","Rights","Type","Archive","Archive Location","Library Catalog","Call Number","Extra","Notes","File Attachments","Link Attachments","Manual Tags","Automatic Tags","Editor","Series Editor","Translator","Contributor","Attorney Agent","Book Author","Cast Member","Commenter","Composer","Cosponsor","Counsel","Interviewer","Producer","Recipient","Reviewed Author","Scriptwriter","Words By","Guest","Number","Edition","Running Time","Scale","Medium","Artwork Size","Filing Date","Application Number","Assignee","Issuing Authority","Country","Meeting Name","Conference Name","Court","References","Reporter","Legal Status","Priority Numbers","Programming Language","Version","System","Code","Code Number","Section","Session","Committee","History","Legislative Body"]

    This program will remove unnessesary types and only store:
    [Item Type, Publication Year, Author(s), Title, Publication Title, DOI, URL, Abstract Note, Date Added, Pages, Issue, Volume, Short Title, Library Catologue, Link Attachments]

    Clicking on the DOI in the CSV will take you to the article

    This program discards all scoping, systematic, and literature reviews, as well as any meta-analyses and any theory studies
'''

from pathlib import Path
import pandas as pd

def checkFile():
    # Take file name input check if exists
    fileName = input("File Name: ")
    print("\n")
    fileExists = False

    while not fileExists:
        my_file = Path(fileName)
        if my_file.is_file():
            fileExists = True
        else:
            print("File doesn't exist, check the spelling\n")
            fileName = input("File Name: ")

    return fileName

def readFile(fileName):
    data = pd.read_csv(fileName)

    data_to_pop = ["Key","ISBN","ISSN","Date","Date Modified","Access Date","Number Of Volumes","Journal Abbreviation","Series","Series Number","Series Text","Series Title","Publisher","Place","Language","Rights","Type","Archive","Archive Location","Call Number","Extra","Notes","File Attachments","Manual Tags","Automatic Tags","Editor","Series Editor","Translator","Contributor","Attorney Agent","Book Author","Cast Member","Commenter","Composer","Cosponsor","Counsel","Interviewer","Producer","Recipient","Reviewed Author","Scriptwriter","Words By","Guest","Number","Edition","Running Time","Scale","Medium","Artwork Size","Filing Date","Application Number","Assignee","Issuing Authority","Country","Meeting Name","Conference Name","Court","References","Reporter","Legal Status","Priority Numbers","Programming Language","Version","System","Code","Code Number","Section","Session","Committee","History","Legislative Body"]

    data = data.drop(columns=[col for col in data_to_pop if col in data.columns])

    return data

def containsKeywords(filterType, text, keywords):
    if filterType == "title":
        if "review" in str(text).lower() or "meta-analyses" in str(text).lower() or "theory" in str(text).lower():
            return False
        return any(keyword.lower() in str(text).lower() for keyword in keywords)
    return any(keyword.lower() in str(text).lower() for keyword in keywords) #any keyword elem is in text for all kewords

def filterDB(data, keywordsTitle, keywordsAbstract):
    filteredTitles = data['Title'].apply(lambda x: containsKeywords("title", x, keywordsTitle)) #each x elem in db has x keyword x from keywords
    filteredAbstracts = data['Abstract Note'].apply(lambda x: containsKeywords("abstract", x, keywordsAbstract))

    filteredData = data[filteredTitles & filteredAbstracts] #combine both

    return filteredData

def enableDOI(data):
    data['DOI'] = data['DOI'].apply(lambda x: "https://doi.org/" + x) # every x entity in dataset
    
    return data

if __name__ == "__main__":
    # validate file get data
    fileName = checkFile()
    data = readFile(fileName)
    
    nonDuplicatedData = data.drop_duplicates(subset=['Title', 'Author']) # remove all duplicates from dataset

    #filter dataset
    keywordsTitles = {"early childhood education", "children", "kindergarden", "preschool", "toddlers",}
    keywordsAbstract = {"ai literacy", "artificial intellegence", "robotics", "machine learning", "augmented reality", "emergent technology", "robots", "computers", "computer science", "AI Literacy", }
    filteredData = filterDB(data, keywordsTitles, keywordsAbstract)

    completeData = enableDOI(filteredData) #make doi a clickable link

    print(f"{completeData}\n")

    #print numbers
    print(f'''Records from CSV file: {len(data)}
Duplicates present in dataset: {len(data) - len(nonDuplicatedData)}
Records after duplicates removed from dataset: {len(nonDuplicatedData)}
Records after filtering dataset with given keywords: {len(filteredData)}\n''')

    #save the csv file
    save = input("Save Data to CSV (Y/N)? ")
    if save.lower() == "y" or save.lower == "yes":
        completeData.to_csv(f"filteredStudies{fileName}", index=False)
        print(f"The filterd data has been saved to filteredStudies{fileName}.")

    
