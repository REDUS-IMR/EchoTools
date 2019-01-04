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

import EchoConvUtils

#reload(sys)  
#sys.setdefaultencoding('utf8')

URLprefix = os.environ['LSSS_URL']

MainDir = os.environ['MAIN_SCRATCH_DIR']

def processLSSS(cruiseNumber, outPath, lsssFile, dbDir, ek60File, workFile, IMParam, EMParam, processRaw, overwrite):

  for i in range(len(cruiseNumber)):

    print("\nNow processing " + outPath[i])
    print("=================================================\n")

    rawExists = False
    dbExists = False

    # If either work and raw files not exist or processRaw is False, then no raw processing will take place
    if ek60File[i] != "False" and workFile[i] != "False" and processRaw:
        rawExists = True
    else:
        rawExist = False
    
    if dbDir[i] != "False":
        dbExists = True
    else:
        dbExists = False

    print("Raw exists: "+ str(rawExists)) 
    print("Raw file: "+ ek60File[i] + "\nWork file: " + workFile[i])

    # Generate names
    reportFileDB = outPath[i] + "/lsssDb_cruiseNumber_" + cruiseNumber[i] + ".xml"
    reportFileRaw = outPath[i] + "/lsssRaw_cruiseNumber_" + cruiseNumber[i] + ".xml"
    
    # Check whether we want to proceed (overwrite)
    if (not (dbExists is True and (overwrite is True or os.path.isfile(reportFileDB) is False))) and \
            (not (rawExists is True and (overwrite is True or os.path.isfile(reportFileRaw) is False))):
        continue
    #if overwrite is not True:
    #    if os.path.isfile(reportFileDB) is True and os.path.isfile(reportFileRaw) is True:
    #        continue

    # Disconnect the current database
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':False})
    print("Database disconnect: " + str(r.status_code))

    # First we copy DB from CES into our local DB
    # Linking directly to the DB in CES won't work as
    # LSSS always want to upgrade the (read-only) database before continuing
    shutil.rmtree(os.path.join(MainDir, "lsss_DB.old"), ignore_errors=True)
    if os.path.exists(os.path.join(MainDir,"lsss_DB")):
        os.rename(os.path.join(MainDir,"lsss_DB"), os.path.join(MainDir, "lsss_DB.old"))
    
    # Catch error to proceed
    try:
        shutil.copytree(dbDir[i], MainDir + "/lsss_DB")
    except EnvironmentError:
        print("Unable to copy file "+dbDir[i])
        continue

    # Get the current config XML and process it as XML object (not necessary though, 
    # but might come in handy later)
    r = requests.get(URLprefix + "/lsss/application/config/xml")
    root = etree.fromstring(r.content)
    #print(etree.tostring(root))

    # Modify the application XML with DB points to our <MainDir>/lsss_DB
    nodeVal = root.xpath("/unit[@name='ApplicationConfiguration']/unit[@name='DatabaseConf']/configuration/connection/parameters/parameter[@name='Directory']")
    nodeVal[0].text = MainDir
    print(root.xpath("/unit[@name='ApplicationConfiguration']/unit[@name='DatabaseConf']/configuration/connection/parameters/parameter[@name='Directory']/text()"))

    # Send the modified application XML, in which DB points to our <MainDir>/lsss_DB
    # This is also connect the newly copied DB
    r = requests.post(URLprefix + "/lsss/application/config/xml", data=etree.tostring(root))
    print("Updating configuration: " + str(r.status_code))

    # Again, get the config XML and process it, might come in handy to check whether
    # modified XML is properly uploaded
    r = requests.get(URLprefix + "/lsss/application/config/xml")
    root = etree.fromstring(r.content)
    #print(etree.tostring(root))

    # Connect DB
    r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':True})
    print("Database connect: " + str(r.status_code))

    # Open the survey file
    #print(lsssFile[i])
    r = requests.post(URLprefix+'/lsss/survey/open', json={'value':lsssFile[i]})
    print("Opening survey file " + lsssFile[i] + ": " + str(r.status_code))

    # Generate from DB first
    if dbExists is True and (overwrite is True or os.path.isfile(reportFileDB) is False):

        # Change vertical & horizontal resolution?
        ## Set interpretation module parameters (default to 0.1 resoluition and 38kHz frequency)
   #     if IMParam[i] == "False":
   #         imParam = {'resolution':.1,'quality':1,'frequencies':[38, 38]}
   #     else:
   #         imParam = ast.literal_eval(IMParam[i])

        ## Set vertical res (default to 5)
   #     if EMParam[i] == "False":
   #         emParam = 5
   #     else:
   #         emParam = EMParam[i]

   #    r = requests.post(URLprefix + '/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizePelagic', json={'value':emParam})

        # Generate LUF20 Report
        r = requests.get(URLprefix + '/lsss/database/report/20')
        print("Generating LUF20 from DB: " + str(r.status_code))

        # Write it to disk
        if r.status_code == 200:
            with open(reportFileDB, 'w+') as f:
                f.write(r.text)
            print "Saved " + reportFileDB
    else:
        print("Not processing DB ", dbExists is True , overwrite is True , os.path.isfile(reportFileDB) is False)


    # Generate from Raw + Work files
    if rawExists is True and (overwrite is True or os.path.isfile(reportFileRaw) is False):

        # We should get the vertical grid size, resolution and quality from the existing NMDechosounder
        NMDfile = EchoConvUtils.find("echosounder*", outPath[i])

        pel_ch_thickness = ""
        bot_ch_thickness = ""
        integrator_dist = ""

	if(len(NMDfile) > 0):
            print("NMDfile: " + NMDfile[0])

            NMDfiletree = etree.parse(NMDfile[0])

            elem = NMDfiletree.xpath('//*[local-name()="pel_ch_thickness"]/text()')
            if(len(elem) > 0):
               pel_ch_thickness = elem[0]

            elem = NMDfiletree.xpath('//*[local-name()="bot_ch_thickness"]/text()')
            if(len(elem) > 0):
                bot_ch_thickness = elem[0]

            elem = NMDfiletree.xpath('//*[local-name()="integrator_dist"]/text()')
            if(len(elem) > 0):
                integrator_dist = elem[0]

            print("pel_ch_thickness bot_ch_thickness integrator_dist from existing NMDEchosounder:")

        print(pel_ch_thickness + ", " + bot_ch_thickness + ", " + integrator_dist)

        # Disconnect DB again
        r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':False})
        print("Database disconnect: " + str(r.status_code))

        # Move old DB
        shutil.rmtree(os.path.join(MainDir, "lsss_DB.old"), ignore_errors=True)
        if os.path.exists(os.path.join(MainDir,"lsss_DB")):
           os.rename(os.path.join(MainDir,"lsss_DB"), os.path.join(MainDir, "lsss_DB.old"))

        # Issue a create DB, this is to make sure that we start from an empty DB
        r = requests.post(URLprefix + '/lsss/application/config/unit/DatabaseConf/create') #, json={'empty':True})
        print "Emptying DB: " + str(r.status_code)

        # Connect DB again
        r = requests.post(URLprefix + "/lsss/application/config/unit/DatabaseConf/connected", json={'value':True})
        print("Database connect: " + str(r.status_code))

        # Open the survey file
        print(lsssFile[i])
        r = requests.post(URLprefix+'/lsss/survey/open', json={'value':lsssFile[i]})
        print(r.status_code)

        # EK60 files
        print "Raw Dir: " + str(ek60File[i])
        r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/DataDir', json={'value':ek60File[i]})
        print "Raw Dir status: " + str(r.status_code)

        # Work files
        print "Work Dir: " + str(workFile[i])
        r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/WorkDir', json={'value':workFile[i]})
        print "Work Dir status: " + str(r.status_code)

        # List of raw files from the .lsss to extract the index number
        r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConf/files')
        print(r.status_code)        
        listFile = r.json()
        print listFile

        # Get the first and the last selected files
        #r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/FirstSelectedFile')
        #firstFile = r.json()
        #print(firstFile)

        #r = requests.get(URLprefix + '/lsss/survey/config/unit/DataConf/parameter/LastSelectedFile')
        #lastFile = r.json()
        #print(lastFile)

        # Find actual first and last indexes from the LSSS file
        #idx = 0
        #for j in range (0 , len(listFile)-1):
        #    if (firstFile["value"] + ".raw") == listFile[j]["file"]:
        #        idx = j
        #        break
        #firstIndex = idx
        #for j in range (idx , len(listFile)-1):
        #    if (lastFile["value"] + ".raw") == listFile[j]["file"]:
        #        idx = j
        #        break
        #lastIndex = idx

        #print firstFile["value"] + " " + lastFile["value"]
        #print "First: " + listFile[firstIndex]["file"]
        #print "Last: " + listFile[lastIndex]["file"]
        #print("First:" + str(firstIndex) + ", Last:" + str(lastIndex))

        # To use all the available raw files
        # Get the last index
        firstIndex = 0
        lastIndex = len(listFile) - 1
        print("First:" + str(firstIndex) + ", Last:" + str(lastIndex))

        # Send index selection
        r = requests.post(URLprefix + '/lsss/survey/config/unit/DataConf/files/selection', json={'firstIndex':firstIndex, 'lastIndex':lastIndex})
        print("Selecting all files: " + str(r.status_code))

        # Wait until the program is ready for further processing
        r = requests.get(URLprefix + '/lsss/data/wait')
        print("Finish waiting: " + str(r.content))

        # Change vertical & horizontal resolution?
        ## Set vertical res (default to 5)
        if EMParam[i] == "False":
            emParam = 5
        else:
            emParam = EMParam[i]

        r = requests.post(URLprefix + '/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizePelagic', json={'value':pel_ch_thickness})
        print "Set vertical resolution (pelagic):" + str(r.status_code)
        r = requests.post(URLprefix + '/lsss/survey/config/unit/GridConf/parameter/VerticalGridSizeBottom', json={'value':bot_ch_thickness})
        print "Set vertical resolution (bottom): " + str(r.status_code)

        ## Set interpretation module parameters (default to 0.1 resolution and 38kHz frequency)
        if IMParam[i] == "False":
            imParam = {'resolution':integrator_dist,'quality':1,'frequencies':[38, 38]}
        else:
            imParam = IMParam[i]

        # Store to local LSSS DB
        r = requests.post(URLprefix + '/lsss/module/InterpretationModule/database', json=imParam)
        print "Set Interpretation Module parameters (and saving to DB): " + str(r.status_code)

        # Generate LUF20 Report
        r = requests.get(URLprefix + '/lsss/database/report/20')
        print("Generating LUF20 from RAW: " + str(r.status_code))

        # Write it to disk
        if r.status_code == 200:
            with open(reportFileRaw, 'w+') as f:
                f.write(r.text)
    else:
        print("Not processing RAW ", rawExists is True ,overwrite is True ,os.path.isfile(reportFileRaw) is False)

  return
