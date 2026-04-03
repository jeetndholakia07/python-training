import os
import threading
from datetime import datetime
import re
import csv

fileName = "TRINET-EMPLOYEE-1128.csv"
folders=["incoming","inprocess","processed","generated","errored"]
exitFolder = folders[4]
birthdate_regex = r"^\d{4}-\d{2}-\d{2}$"
jsonRegex = r"""
^\[ # must have starting bracket
(?:\{"\w+":"\w+"\})+ # match starting json object e.g. {"role":"CDM"}
(?:,\{"\w+":"\w+"\})* # match optional comma separated roles e.g. {"role":"CDM"}, {"role":"PFD"}
\]$ # must have closing bracket
"""
roles_regex = r"""("\w+":"\w+")"""

def is_null(value):
    return value.lower().strip()=="null"

def is_empty(value):
    return value.strip()==""

def formatDate(date):
    dateObj = datetime.strptime(date,"%Y-%m-%d")
    formatted = dateObj.strftime("%B %Y, %d")
    return formatted

def formatRoles(roles):
    roleList = []
    for item in roles:
        for word in item.split(":"):
            if("role" not in word):
                roleList.append(word.replace('"',""))
    return " ".join(roleList)

def initializeFolders():
    for folder in folders:
        try:
            os.mkdir(folder)
        except (FileExistsError,OSError):
            continue

def fetchFileData(filePath):
    try:
        with open(filePath,"r") as file:
            data = file.read()
            return data
    except OSError as e:
        print(f"Unable to access file from {filePath}:",e)        

def initializeCSVFile(folderName):
    try:
        with open(f"{folderName}/{fileName}","w") as createFile:
            data = fetchFileData(fileName)
            createFile.write(data)
    except (FileNotFoundError,OSError) as e:
        print(f"Unable to initialize CSV File to {folderName} folder:",e)

def moveFile(startDirectory,endDirectory):
    try:
        os.rename(f"{startDirectory}/{fileName}",f"{endDirectory}/{fileName}")
    except FileNotFoundError as e:
        print(f"Unable to move file from {startDirectory} to {endDirectory} :",e)

def processFile(readFolder, writeFolder):
    try:
        input_path = f"{readFolder}/{fileName}"
        output_path = f"{writeFolder}/{fileName}"
        with open(input_path,"r",newline='') as file:
            csvFile = csv.DictReader(file)
            columns = csvFile.fieldnames
            tempRows = []
            for line in csvFile:
                birthdate = line.get("BIRTH_DATE")
                roles = line.get("ROLES")

                if(not is_null(birthdate)):
                    if is_empty(birthdate) or not re.match(birthdate_regex,birthdate):
                        raise ValueError(f"Invalid birthdate format: {birthdate}")
                    line["BIRTH_DATE"] = formatDate(birthdate)

                if(not is_null(roles)):
                    if is_empty(birthdate):
                        raise ValueError(f"Invalid roles: {roles}")
                    jsonMatch = re.findall(jsonRegex,roles,re.VERBOSE)
                    if len(jsonMatch)==0:
                        raise ValueError(f"Invalid roles: {roles}")
                    rolesMatches = re.findall(roles_regex,roles)
                    line["ROLES"] = formatRoles(rolesMatches)
                
                tempRows.append(line)
        with open(output_path,"w",newline='') as generatedFile:
            writer = csv.DictWriter(generatedFile,fieldnames=columns)
            writer.writeheader()
            writer.writerows(tempRows)
            moveFile(readFolder,folders[2])
        print("Completed processing successfully.")
    except (ValueError, TypeError, FileNotFoundError, OSError) as e:
        print("Error processing file:",e)
        moveFile(readFolder,exitFolder)

createFolders = threading.Thread(target=initializeFolders)
initializeFile = threading.Thread(target=initializeCSVFile,args=(folders[0],))
moveToInProcess = threading.Thread(target=moveFile,args=(folders[0],folders[1]))
mainProcess = threading.Thread(target=processFile,args=(folders[1],folders[3]))
print("Creating Folders...")
createFolders.start()
createFolders.join()
print("Initializing file to incoming folder...")
initializeFile.start()
initializeFile.join()
print("Moving file to inprocess folder...")
moveToInProcess.start()
moveToInProcess.join()
print("Processing the file...")
mainProcess.start()
mainProcess.join()