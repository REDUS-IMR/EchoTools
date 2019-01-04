import sys
import os
from lxml import etree
import requests
import shutil
import glob
import re
import csv
import io
import ast
import fnmatch

def findLSSSall(cruiseRoot, outputPath, cruiseNo):
    # Go to cruise's root directory
    #cruiseRoot = '/'.join(lsssFile.split("/")[0:5])

    # Prepare magic
    #m = magic.Magic(mime=True, magic_file="./ekmagic.mgc")

    # Sets
    workFiles=[]
    workFile=""

    rawFiles=[]
    rawFile=""

    lsssFiles=[]
    lsssFile=""

    lsssDBDirs=[]
    lsssDBDir=""

    for root, dirs, files in os.walk(cruiseRoot.encode('utf-8').strip()):
        for dir in dirs:
            # Find
            if dir == "lsssExportDb":
                print(os.path.join(root, dir))
                lsssDBDirs.append((os.path.join(root, dir), os.path.getmtime(os.path.join(root, dir))))
        for file in files:
            # Find LSSS Files
            if file.endswith(".lsss"):
                print(os.path.join(root, file))
                lsssFiles.append((os.path.join(root, file), os.path.getmtime(os.path.join(root, file))))
            # Find Work Files
            if file.endswith(".work") and not root.find("OTHER") > -1 and not root.find("ertikal") > -1 and not root.find("BEI") > -1 and not root.find("promus") > -1 and not root.find("MS70") > -1:
                print(os.path.join(root, file))
                workFiles.append((os.path.join(root, file), os.path.getmtime(os.path.join(root, file))))
            # Find Raw Files
            if file.endswith("raw") and not root.find("OTHER") > -1 and not root.find("alibr") > -1 and not root.find("CALIB") > -1:
                irec = re.compile(r'EK.*[0-9]+[0-9]+',  re.IGNORECASE)
                #root.find("KORONA") == -1 and root.find("CALIBRATION") == -1 and root.find("MS70") == -1:
                # Check for file magic
                #if m.from_file(os.path.join(root, file))=='echosounder/ek60':
                    # Now we check for RAW pattern
                #    print("magic OK:" + os.path.join(root, file))
                    #pattern = re.compile(b'RAW')
                    #f = open(os.path.join(root, file), "rb")
                    #data = f.read()
                    #found = pattern.search(data)
                    #if(found is not None):
                if irec.search(root) is not None:
                        print(os.path.join(root, file))
                        rawFiles.append((os.path.join(root, file), os.path.getmtime(os.path.join(root, file))))


    # Sort the files by modification time
    # If not any files, say none
    if len(workFiles)<1:
        workFile = "False"
    else:
        workFiles = sorted(workFiles, key=lambda name: name[1])
        workFile = os.path.dirname(workFiles[0][0])

    if len(rawFiles)<1:
        rawFile = "False"
    else:
        rawFiles = sorted(rawFiles, key=lambda name: name[1])
        rawFile = os.path.dirname(rawFiles[0][0])
    
    if len(lsssFiles)<1:
        lsssFile = "False"
    else:
        lsssFiles = sorted(lsssFiles, key=lambda name: name[1])
        lsssFile = lsssFiles[0][0]

    if len(lsssDBDirs)<1:
        lsssDBDir = "False"
    else:
        lsssDBDirs = sorted(lsssDBDirs, key=lambda name: name[1])
        lsssDBDir = lsssDBDirs[0][0]

 
    return([lsssDBDir, lsssFile, outputPath, cruiseNo, workFile, rawFile])

def decodeName(name):
    if type(name) == str: # leave unicode ones alone
        try:
            name = name.decode('utf8')
        except:
            name = name.decode('windows-1252')
    return name

def batchLSSSsearch():

  # Prepare output
  CSVout = os.environ['CES_LSSS_CSV']
  open(CSVout, 'w').close

  # Set the comparator system directory 
  NMDQualityRoot = os.environ['NMD_QUALITY_ROOT']

  # Set the options
  overwriteOpt = False
  processRawOpt = True

  exclude = set([".git"])

  ctr = 0
  # traverse root directory, and list directories as dirs and files as files
  for root, dirs, files in os.walk(NMDQualityRoot):
    [dirs.remove(d) for d in list(dirs) if d in exclude]
    files = [decodeName(f) for f in files]
    cruiseNo = ""
    if len(dirs)==0:

       print(os.path.basename(root))
    
       cruiseNo = re.search("\d{7}", root)

       # TODO: Unconventional cruise numbers
       if cruiseNo == None:
          continue
       else:
          cruiseNo = cruiseNo.group(0)

       print(cruiseNo)

       cYear = cruiseNo[:4]

       print(cYear)

       regex = re.compile(r'^echosounder\_.+xml$', re.UNICODE)
       cruiseShips = filter(regex.search, files)

       print(cruiseShips)
       if not cruiseShips:
          continue

       # Compose path to cruise data
       cruiseYearPath = os.environ['CRUISE_DATA_ROOT'] + '/' + cYear

       print(cruiseYearPath)

       cruiseYearList = filter(lambda x: os.path.isdir(cruiseYearPath + '/' + x), os.listdir(cruiseYearPath))

       print(cruiseYearList)

       for cruiseShip in cruiseShips:
          sName = (os.path.splitext(cruiseShip)[0]).split('_')[-1]
          # Strip everything, change to uppercase, and add P at the beginning
          regex = re.compile('[\W_]+', re.UNICODE)
          sName = regex.sub('', sName)
          sName = 'P' + sName.upper()

          # Find directory
          regex = re.compile(cruiseNo + '.+' + sName, re.UNICODE)
          cruiseD = filter(regex.search, cruiseYearList)
          
          if not cruiseD:
              continue

          cruiseD = cruiseD[0]

          cruisePath = cruiseYearPath + "/" + cruiseD
          allInfo = findLSSSall(cruisePath, root, cruiseNo)

          print(allInfo)
          
	  with open(CSVout, "a") as myFile:
              writer = csv.writer(myFile)
              writer.writerow(allInfo)

if __name__ == "__main__":
   batchLSSSsearch()

