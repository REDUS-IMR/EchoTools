# -*- coding: utf-8 -*-
"""
@author: Sindre Vatnehol
@institute: Institute of marine reserach, norway
@group: Pelagic fish group
@project: REDUS
@contact_mail: sindre.vatnehol@hi.no
@contact_cell: +47 900 79 376
"""





def checkFileLocation(files,root): 
    '''
    Description: 
        Check if some of the important files are stored in the correct folder. 
        If not return file type and relative direction
        
        
        
    usage: 
        filetype,directory = checkFileLocation(files,root)
        
        
        input:
        files = list of files within the relative directory
        root = relative directory, i.e. /ACOUSTIC/EK60/
        
        
        output: 
        filetype : i.e. '.work'
        directory : directory of the misplaced file, i.e. ACOUSTIC/EK60/
        
        returns False if the file is located in the correct folder
        
        
        
        example in loop: 
            
            
        path = path to the survey folder, i.e. //ces.imr.no/2018/CruiceFolder/
        
        for root, dirs, files in os.walk(path):
            error_msg = checkFileLocation(files,root.replace(path,''))
        
    '''
    
    
    

    #for boookkeeping
    filetype = False
    directory = False
    
    
    
    #Split the directory 
    A = root.split('\\')
    B = A[0]
    A = A[-1].split('_')
        
    
    
    
    
    #Valid subfolders that the acoustic data are stoored into
    ValidAcoustic_folders = ['CALIBRATION',
                             'ORIGINALRAWDATA',
                             'RAWDATA']
    
    
    
    
    
    #Ignore data located in some of the first-level folder as theese are not part 
    #of the official survey-data
    IgnoreFirstLevel = ['EXPERIMENTS',
                        'OBSERVATION_PLATFORMS']
    
    
    
    
    
    #Check the .raw files if they are in the correct sub-folder
    if any(fname.endswith('.raw') for fname in files):
        if not B in IgnoreFirstLevel: 
            if len(A)>1:
                if not A[-1] in ValidAcoustic_folders: 
                    filetype = '.raw'
                    directory = root
            else: 
                    filetype = '.raw'
                    directory = root
            
            
    
    
    
    #Check the .nc files if they are in the correct sub-folder
    if any(fname.endswith('.nc') for fname in files):
        if not B in IgnoreFirstLevel: 
            if len(A)>1:
                if not A[1].split('_') in ValidAcoustic_folders: 
                    filetype = '.nc'
                    directory = root
            else: 
                    filetype = '.nc'
                    directory = root
            


            
         
    #Check the .lsss files if they are in the correct sub-folder
    if any(fname.endswith('.lsss') for fname in files):
        if not B in IgnoreFirstLevel: 
            if not A[-1] == 'LSSS': 
                    filetype = '.lsss'
                    directory = root
               
            
            
            
    #Check the .work files if they are in the correct sub-folder
    if any(fname.endswith('.work') for fname in files):
        if not B in IgnoreFirstLevel: 
            if not A[-1] == 'WORK': 
                    filetype = '.work'
                    directory = root
               
                
            
            
    #Check the .snap files if they are in the correct sub-folder
    if any(fname.endswith('.snap') for fname in files):
        if not B in IgnoreFirstLevel: 
            if not A[-1] == 'WORK': 
                    filetype = '.snap'
                    directory = root
               
            

    #return
    return filetype,directory

