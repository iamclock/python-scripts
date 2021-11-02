#! /usr/bin/python3
import os


path = input("Enter path to folder: ")
listOfFiles = os.listdir(path)
os.chdir(path)
for curFileName in listOfFiles:
    os.rename(curFileName, '0'+curFileName)