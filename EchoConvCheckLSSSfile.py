# -*- coding: utf-8 -*-
"""
@author: Sindre Vatnehol
@institute: Institute of marine reserach, norway
@group: Pelagic fish group
@project: REDUS
@contact_mail: sindre.vatnehol@hi.no
@contact_cell: +47 900 79 376

"""


#import library
import xml.etree.ElementTree
import os





def checkLSSSPaths(file_path,survey_dir,LSSS_folder):
    '''
    checkLSSSPaths.py
    
    
    Purpose: 
        One of the outputs from the LSSS software is the .LSSS file. 
        Within this XML file, there are several of variables thats links to a path location. 
        These path should be relative to the survey location on the server; however,
        often these are sett to a particular folder on a specific computer/server location. 
        
        This script reads all of these paths, and test if they exist (if treated as relative) on the server
        It also test if the relative path, assuming a fixed structure, exist.
        At last, it check if there is files within these folders
        
    
    
    
    Usage: 
        Out = checkLSSSPaths(file_path,survey_dir,LSSS_folder)
        
        
            Input
                - file_path : file name with full path
                - survey_dir : path to the top-level cruice directory on the server
                - LSSS_folder : path to the LSSS top level folder
                
            
            Output: 
                - Out: Struktured data, i.e. 
                    Out.DataDir
                    Out.KoronaDir
                    Out.TrawlDataDir
                    Out.CTDDataDir
                    Out.RefLogDataDir
                    Out.WorkDir
                    Out.ReportsDir
                    Out.ExportDir
                    
    '''
    
    
    
    
    #Define a structure type 
    class structtype(): 
        pass
    
    
    
    
    
    
    def check(directory,xml): 
        "Return TRUE if folder exist in structure"
        if directory[-1]=='\\' or  directory[-1]=='/': 
            LSSS_path = directory+xml
        else: 
            LSSS_path = directory+'/'+xml
        return os.path.isdir(LSSS_path),LSSS_path





    
    def checkIfFiles(directory,xml,filetype): 
        "Return TRUE if there is correct files within"
        if directory[-1]=='\\' or  directory[-1]=='/': 
            LSSS_path = directory+xml
        else: 
            LSSS_path = directory+'/'+xml
            
        files = os.listdir(LSSS_path)
        if filetype == False: 
            if len(files)>0: 
                return(True)
            else: 
                return(False)
        else: 
            if any(fname.endswith(filetype) for fname in files): 
                return(True)
            else: 
                return(False)
        
        
        
        
        
    def main(folder,xml,relative,file): 
        '''
        function to initialize check and checkIfFile functions
        '''
        
        #check if the LSSS path is correct
        if_LSSS,path = check(folder,xml)
        
        #check if relative path exist
        if_ADDED,path = check(folder,relative)
        
        if if_ADDED == True: 
            if_files = checkIfFiles(folder,relative,file)
        else: 
            if_files = False
            path = False
        
        return{'LSSS':if_LSSS, 'Relative':if_ADDED,'Files':if_files,'FullPath':path}
        
    
    
    
    

    #Make the Out structurable
    Out = structtype()    
        
    
    
    
    if file_path.endswith('.lsss'): 
        
        #Open file
        file = open(file_path)
        
        
        #Parse the xml file
        filen = xml.etree.ElementTree.parse(file).getroot()
        
        
        
        
        #Go through all the file and add paths to directories. 
        #If new paths are avaliable, this should be added in the script below
        A = filen[0].findall('./unit/unit')
        for a in A: 
            
            
            #Go through the data configuration file
            if a.attrib['name'] == 'DataConf':  
                
                
                B = a.findall('configuration/parameters/parameter')
                
                
                
                for b in B: 
                    
                    
                    #Check the .raw directories if they exist (either for ek60 or ek80)
                    if b.attrib['name'] == 'DataDir': 
                        Out.DataDir_EK80 = main(survey_dir,b.text.replace('..\\',''),'ACOUSTIC/EK80/EK80_RAWDATA','.raw')
                        Out.DataDir_EK60 = main(survey_dir,b.text.replace('..\\',''),'ACOUSTIC/EK60/EK60_RAWDATA','.raw')
                        
                        
                    elif b.attrib['name'] == 'KoronaDataDir': 
                        Out.KoronaDir = main(LSSS_folder,b.text.replace('..\\',''),'KORONA',False)
                        
                        
                    elif b.attrib['name'] == 'TrawlDataDir': 
                        Out.TrawlDataDir = main(survey_dir,b.text.replace('..\\',''),'BIOLOGY/CATCH_MEASUREMENTS/BIOTIC/','.spd')
        
                        
                    elif b.attrib['name'] == 'TowfishDataDir': 
                        Out.TowfishDataDir = b.text
                        
                        
                    elif b.attrib['name'] == 'CTDDataDir': 
                        Out.CTDDataDir = main(survey_dir,b.text.replace('..\\',''),'PHYSICS/CTD/CTD_DATA/','.cnv')
                        
                        
                    elif b.attrib['name'] == 'FileDrawDataDir': 
                        Out.FileDrawDataDir = b.text
                        
                    elif b.attrib['name'] == 'RefLogDataDir': 
                        Out.RefLogDataDir = main(survey_dir,b.text.replace('..\\',''),'CRUISE_LOG\TRACK','.csv')
                        
                    elif b.attrib['name'] == 'ReportsDir': 
                        Out.ReportsDir = b.text
                        Out.ReportsDir = main(LSSS_folder,b.text.replace('..\\',''),'REPORTS','.txt')
                        
                        
                    elif b.attrib['name'] == 'WorkDir': 
                        Out.WorkDir = main(LSSS_folder,b.text.replace('..\\',''),'WORK','.work')
                        
                        
                    elif b.attrib['name'] == 'ExportDir': 
                        Out.ExportDir = main(LSSS_folder,b.text.replace('..\\',''),'EXPORT','.txt')
        
        
        #close file
        file.close()
        
    
    #return output
    return Out



