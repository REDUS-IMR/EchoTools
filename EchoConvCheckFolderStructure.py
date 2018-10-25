# -*- coding: utf-8 -*-
"""
@author: Sindre Vatnehol
@institute: Institute of marine reserach, norway
@group: Pelagic fish group
@project: REDUS
@contact_mail: sindre.vatnehol@hi.no
@contact_cell: +47 900 79 376
"""




def checkIfRootIsValid(root): 
    
    '''
    Description:
        Check if the relative paths from the IMR data structure is ok. 
        It assumes a fixed structure that can be modified within this text. 
        
    
    Usage: 
        
        error_msg = checkIfRootIsValid(relativ_path)
        
        
        input: the relative path of the directory, i.e. /ACOUSTIC/EK60/
        
        output: error_msg (the relative path that does not follow the structure
                            i.e, /ACOUSTIC/SU90/raw)
                
        
                returns False if the folder is correctly named and within the correct level
            
        
        
        
        (eksample within loop)
        
        
        path = path to the survey folder, i.e. //ces.imr.no/2018/CruiceFolder/
        
        for root, dirs, files in os.walk(path):
            
            error_msg = checkIfRootIsValid(root.replace(path,''))
        
    '''
    
    
    #
    # Top-level information
    #
    
    ValidRoot_first = ['ACOUSTIC',
                       'BIOLOGY',
                       'CRUISE_DOCUMENTS',
                       'CRUISE_LOG',
                       'EXPERIMENTS',
                       'GEOLOGY_AND_GEOPHYSICS',
                       'ICES',
                       'METEROLOGY',
                       'OBSERVATION_PLATFORMS',
                       'PHYSICS',
                       'POLLUTION']
    
    ###############Acoustic ##################################
    
    ValidAcoustic_second = ['EK60', 
                            'EK80', 
                            'SU90',
                            'POSTPROCESSING',
                            'SH90', 
                            'SX90', 
                            'SN90', 
                            'MS70',
                            'ME70',
                            'MULTIBEAM_ECHOSOUNDERS',
                            'SUB_BOTTOM_PROFILERS']
    
    
    ValidAcoustic_third = ['CALIBRATION',
                           'LOG',
                           'ORIGINALRAWDATA',
                           'RAWDATA',
                           'SCREEN_DUMP',
                           'LSSS',
                           'PYSONAR']
    
    
    ValidAcoustic_forth = ['ECHOSOUNDER',
                           'PROFOS',
                           'PROMUS',
                           'PROBE',
                           'SU90',
                           'SX90',
                           'SH90']
    
    
    ValidAcoustic_fifth = ['EXPORT',
                           'KORONA',
                           'LSSS_FILES',
                           'REPORTS',
                           'WORK',
                           'src']
    
    
    ###############Biology ##################################
    
    
    
    ValidBiology_second = ['CATCH_MEASUREMENTS',
                           'BENTHOS',
                           'PLANKTON',
                           'SEA_MAMMALS',
                           'TRAWL_SENSORS']
    
    
    ValidBiology_third = ['BIOTIC',
                          'MARBUNN',
                          'DEEP_VISION',
                          'FISHMETER',
                          'MOCNESS',
                          'MULTI_NET',
                          'MULTI_SAMPLER',
                          'PLANKTON_DATABASE',
                          'SEAL',
                          'WHALE',
                          'OTHER',
                          'SCANMAR',
                          'SIMRAD',
                          'TRAWL_SONAR']
        
    
    
    ValidCruiceLog_second = ['ACTIVITY',
                             'SUBSEA_POSITION',
                             'TRACK',
                             'TECHSAS']
    
    
    error_msg = False
    
    
    if root != '': 
        
        
        #Split the directory into peaces
        A = root.split('\\')
        
        
        if len(A) == 1:
            if not A[0] in ValidRoot_first: 
                error_msg = '/'+root+'\n'
            
        
        
        if len(A)>=2: 
            
            
            #Check if this is an acoustic folder
            if A[0] == 'ACOUSTIC' or A[0] == 'ACOUSTIC_DATA': 
                
                
                #Check if the acoustic stuff is ok
                if not A[1] in ValidAcoustic_second:
                    error_msg = '/'+root+'\n'
                    
                    
                
                #Check third level
                if len(A)>=3:
                    if not A[2].split('_')[0] in ValidAcoustic_third:
                        if len(A[2].split('_'))>=2: 
                            if not A[2].split('_')[1] in ValidAcoustic_third:
                                error_msg = '/'+root+'\n'
                        else: 
                            error_msg = '/'+root+'\n'
                            
                #Check forth level
                if len(A)>=4:
                    if not A[3] in ValidAcoustic_forth: 
                        error_msg = '/'+root+'\n'
                        
                        
                        
                #Check fifth level
                if len(A)>=5:
                    if not A[4] in ValidAcoustic_fifth: 
                        error_msg = '/'+root+'\n'
                        
                 
                    
                    
            elif A[0] == 'BIOLOGY':
                if not A[1] in ValidBiology_second: 
                    error_msg = '/'+root+'\n'
                    
                if len(A)>=3: 
                    if not A[2] in ValidBiology_third:  
                        error_msg = '/'+root+'\n'
                
                
                
                
                
            elif A[0] == 'CRUISE_LOG': 
                if not A[1] in ValidCruiceLog_second: 
                    error_msg = '/'+root+'\n'
            
            
        
    return error_msg
        