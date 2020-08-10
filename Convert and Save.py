# -*- coding: utf-8 -*-
"""
Python File Converter for Bodie

Created on Tue May  7 15:13:03 2019

@author: yeesh

Made for Python 3.7
"""

import os
import csv
import json
import base64

cwd = os.getcwd()
csvFolder = "CSVs"
picturesFolder = "Pictures"
folderNames = [f for f in os.listdir(os.getcwd()) if os.path.isdir(f)]

for folder in folderNames:
    
    if (folder == csvFolder or folder == picturesFolder):
        continue;
   
    try:
        os.mkdir(os.path.join(cwd, folder, picturesFolder))
        os.mkdir(os.path.join(cwd, folder, csvFolder))
    except OSError:
        print ("Creation of the directory failed")
    else:
        print ("Successfully created the directory")

    #Imports the names of all of the json files
    txt_files = [f for f in os.listdir(folder) if f.endswith('.json')]
    
    with open(os.path.join(cwd, "{}.json".format(folder)), "w") as manifest:
        
        manifestData = {}
        manifestData["data"] = []
#        manifestInitialized = False;
        
        #Iterates through each file
        for fileName in txt_files:
            
           #Reads from the file
            with open(os.path.join(cwd, folder, fileName), "r") as jsonFile:
                
                #load file into a dictionary and load name for filewriting
                data = json.load(jsonFile)
                objectName = data["Identifer"]
                
                #Remove the base64 image data and then remove it from the json
                objectPicture = data["Picture"]
                pictureBytes = objectPicture.encode('utf-8')
                del data["Picture"]
                
#                if (not manifestInitialized):
#                    manifestData = data
#                    manifestInitialized = True
#                else:
#                    manifestData.update(data)
                
                manifestData["data"].append(data)                
                jsonFile.close()
                
                #Write the png to the folder
                with open(os.path.join(cwd, folder, picturesFolder, "{}.png".format(objectName)), "wb") as savedPicture:
                    savedPicture.write(base64.decodebytes(pictureBytes))
                    savedPicture.close()
                    
                #Write the csv to the folder
                with open(os.path.join(cwd, folder, csvFolder, "{}.csv".format(objectName)), "w") as csvFile:
                    csvWriter = csv.writer(csvFile)
                    header = data.keys()
                    csvWriter.writerow(header)
                    #count += 1
                    csvWriter.writerow(data.values())
                    csvFile.close()
                
        with open(os.path.join(cwd, "{}.csv".format(folder)), "w", newline = '\n', encoding='utf-8') as dataSet:
            csvWriter = csv.DictWriter(dataSet, fieldnames = manifestData["data"][0].keys())
            csvWriter.writeheader()
            count = 0
            for item in manifestData["data"]:
                count += 1
                csvWriter.writerow(item)
                continue
            dataSet.close()
        json.dump(manifestData, manifest)