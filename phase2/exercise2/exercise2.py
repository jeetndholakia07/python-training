import csv
import threading
import os

fileName = "SQLSERVER-Person_BusinessEntity-last-20777.csv"
folders = ["incoming","inprocess","processed","generated","errored"]
exitFolder = folders[4]
CHUNK_SIZE = 150 # 150 records

def is_empty(value):
    return value.strip()==""

def initializeFolders():
    for folder in folders:
        try:
            os.mkdir(folder)
        except FileExistsError:
            continue

def moveFile(startDirectory,endDirectory):
    try:
        os.rename(f"{startDirectory}/{fileName}",f"{endDirectory}/{fileName}")
    except (FileNotFoundError,OSError) as e:
        print(f"Unable to move file from {startDirectory} to {endDirectory}:",e)

def fetchFileData(filePath):
    try:
        with open(filePath,"r") as file:
            data = file.read()
            return data
    except (FileNotFoundError, OSError) as e:
        print(f"Unable to access file from {filePath}:",e)

def initializeCSVFile(folderName):
    try:
        with open(f"{folderName}/{fileName}","w") as file:
            fileData = fetchFileData(fileName)
            file.write(fileData)
    except (FileNotFoundError,OSError) as e:
        print(f"Unable to initialize CSV file to folder {folderName}:",e)

def generateChunks(reader):
    chunk=[]
    for i,row in enumerate(reader):
        if(i%CHUNK_SIZE==0 and i>0):
            yield chunk
            chunk = []
        chunk.append(row)
    yield chunk

def processFile(readFolder,writeFolder):
    try:
        with open(f"{readFolder}/{fileName}",newline='') as file:
            csvFile = csv.reader(file)
            header = next(csvFile)
            threads=[]
            for i,chunk in enumerate(generateChunks(csvFile),start=1):
                    if any(is_empty(value) for row in chunk for value in row):
                            raise ValueError(f"Invalid value found. Empty strings are not allowed.")
                    writeThread = threading.Thread(target=writeChunk,args=(f"{writeFolder}/chunk-{i}.csv",header, chunk))
                    threads.append(writeThread)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        moveFile(readFolder,folders[2])
        print("Completed processing successfully.")
    except (FileNotFoundError,OSError,ValueError,TypeError) as e:
        print("Unable to process file:",e)
        moveFile(readFolder,exitFolder)

def writeChunk(writeFolder,header,chunk):
    try:
        with open(f"{writeFolder}","w",newline='') as file:
            csvWriter = csv.writer(file)
            csvWriter.writerow(header)
            csvWriter.writerows(chunk)
    except (FileNotFoundError,OSError) as e:
        print(f"Unable to write to file in folder {writeFolder}:",e)

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