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

def findLSSSraw(lsssFile):
    # Go to cruise's root directory
    cruiseRoot = '/'.join(lsssFile.split("/")[0:5])

    # Prepare magic
    #m = magic.Magic(mime=True, magic_file="./ekmagic.mgc")

    # Sample work files
    workFiles=[]
    workFile=""
    rawFiles=[]
    rawFile=""
    #wSamples=""

    # Now find sample work files (sort by time modified)
    for root, dirs, files in os.walk(cruiseRoot.encode('utf-8').strip()):
        for file in sorted(files, key=lambda name: os.path.getmtime(os.path.join(root, name))):
            if file.endswith(".work") and not root.find("OTHER") > -1 and not root.find("ertikal") > -1 and not root.find("BEI") > -1 and not root.find("promus") > -1 and not root.find("MS70") > -1:
                print(os.path.join(root, file))
                workFiles.append(os.path.join(root, file))
                break

    # Sort the work files by modification time
    workFiles = sorted(workFiles, key=lambda name: os.path.getmtime(os.path.join(root, name)))

    # If not work files, just exit)
    if len(workFiles)<1:
        return(None)
    else:
        workFile=workFiles[0]

    # Sample work name
    #for wf in workFiles:
    #    print(os.path.basename(wf).split(".")[0])
    #    wSamples = os.path.basename(wf).split(".")[0]
    #    # Sometimes not enough, splice again
    #    wSamples = wSamples.split("-")[0] + "-" + wSamples.split("-")[1]
    #    print("Sample: "+wSamples)

    # Find paired raw files (sort by time modified)
    for root, dirs, files in os.walk(cruiseRoot.encode('utf-8').strip()):
        for file in sorted(files, key=lambda name: os.path.getmtime(os.path.join(root, name))):
            # Triple check, name start with sample, ends with raw, and directory contains EK 
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
                	rawFiles.append(os.path.join(root, file))
                	break
    
    # Sort all by time
    rawFiles = sorted(rawFiles, key=lambda name: os.path.getmtime(os.path.join(root, name)))
    
    if len(rawFiles)<1:
        return(None)
    else:
        rawFile=rawFiles[0]
 
    return([os.path.dirname(workFile), os.path.dirname(rawFile)])
    #sys.exit(0)


def decodeName(name):
    if type(name) == str: # leave unicode ones alone
        try:
            name = name.decode('utf8')
        except:
            name = name.decode('windows-1252')
    return name

def batchLSSSsearch():

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

       # For each loop process
       cruiseNumber=[]
       outPath=[]
       lsssFile=[]
       dbDir=[]
       ek60File=[]
       workFile=[]
       ctr = 0
       # END

       print(os.path.basename(root))
       #cruiseNo = re.search("(?<=\_S)\d{7}", root)
       cruiseNo = re.search("\d{7}", root)
       #print(cruiseNo)
       if cruiseNo==None:
          continue
       # prepare line
       cruiseFiles = ""
       LSSScsv = io.open(os.environ['LSSSDB_CSV'], "r", encoding="latin-1", errors='ignore')
       for line in LSSScsv:
          #print(line)
          # Search for matching cruise lines
          if re.search(cruiseNo.group(0), line): #and not re.search("/diverse/", line):
             cruiseFiles = cruiseFiles + "\n" + line
       DB = ""
       LSSS = ""
       for line in cruiseFiles.split("\n"):
          if re.search("lsssExportDb", line):
             DB = line.split(",")
             break
       for line in cruiseFiles.split("\n"):
          if re.search("[.]lsss", line):
             LSSS = line.split(",")
             break

       # If we have LSSS file
       if len(LSSS)>0:

        lf = LSSS[1]+"/"+LSSS[2]
        print(lf)
        # Find EK and .work files
        #if re.search("2014", str(cruiseNo)):
        EkWork = findLSSSraw(lf)
        print(EkWork)

        # Check either DB or ek + work is available
        if len(DB)>0 or EkWork is not None:
            # ctr can be incremented here
            ctr = ctr + 1
            lsssFile.append(lf.encode('utf-8').strip())
            cruiseNumber.append(cruiseNo.group(0))
            outPath.append(root.encode('utf-8').strip())
        else:
            continue

        # If we have LSSS DB
        if len(DB)>0:
	  dbTmp = DB[1]+"/"+DB[2]
          dbDir.append(dbTmp.encode('utf-8').strip())
        else:
          dbDir.append(False)
        
        # If we have either (EK + .work) or DB
        if EkWork is not None:
            workFile.append(EkWork[0].encode('utf-8').strip())
            ek60File.append(EkWork[1].encode('utf-8').strip())
        else:
            workFile.append(False)
            ek60File.append(False)

        print("Record:\n")
        print(dbDir[ctr-1], lsssFile[ctr-1], cruiseNumber[ctr-1], outPath[ctr-1], workFile[ctr-1], ek60File[ctr-1])
        print("\n")
	myFile = open(os.environ['CES_LSSS_CSV'], 'a')
	with myFile:
   		writer = csv.writer(myFile)
        	writer.writerow([dbDir[ctr-1], lsssFile[ctr-1], cruiseNumber[ctr-1], outPath[ctr-1], workFile[ctr-1], ek60File[ctr-1]])
        #processLSSS(cruiseNumber, outPath, lsssFile, dbDir, ek60File, workFile, processRawOpt, overwriteOpt)
    # Stop after 10, just for testing
    #if ctr==10: 
    #    break

  print(len(dbDir))
  print(len(lsssFile))
  print(len(cruiseNumber))
  print(len(outPath))
  print(len(workFile))
  print(len(ek60File))

  #processLSSS(cruiseNumber, outPath, lsssFile, dbDir, ek60File, workFile, processRawOpt, overwriteOpt)


if __name__ == "__main__":
   batchLSSSsearch()

