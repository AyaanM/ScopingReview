'''
title: sort article data
author: Ayaan Merchant (ayaan.merchant08@gmail.com)
date-created: 2024-06-06
'''

import sqlite3
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

def createDB():
    # connect to the database
    DB_name = input("What would you like to call your Database File? ")
    DB_exists = False # assume db doesn't exist

    while not DB_exists:
        if (Path.cwd() / DB_name).exists() == True: #if db exists, can't use it
            print("DB already exists, ether delete that or give another name\n")
            DB_name = input("What would you like to call your Database File? ")
        else:
            DB_exists = True # if db doesn't exit create it

    return DB_name