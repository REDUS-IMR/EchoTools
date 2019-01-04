#!/usr/bin/python

import sys, getopt
import csv
import os

import EchoConvProcess

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'EchoConvRun.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

   if inputfile == '':
      print "You must specify an input file"
      sys.exit(3)
   
   cruiseNumber=[]
   outPath=[]
   lsssFile=[]
   dbDir=[]
   ek60File=[]
   workFile=[]
   IMParam = []
   EMParam = []

   processRaw = True if os.environ['PROCESS_RAW'] == '1' else False
   overwrite = True if os.environ['OVERWRITE_OUTPUT'] == '1' else False

   print "Process RAW: " + str(processRaw)
   print "Overwrite: " + str(overwrite)

   with open(inputfile, 'rb') as csvfile:
      creader = csv.reader(csvfile, delimiter=',')
      for row in creader:
        cruiseNumber.append(row[3])
        outPath.append(row[2])
        lsssFile.append(row[1])
        dbDir.append(row[0])
        ek60File.append(row[5])
        workFile.append(row[4])
        if 6 < len(row):
            IMParam.append(row[6])
        else:
            IMParam.append("False")

        if 7 < len(row):
            EMParam.append(row[7])
        else:
            EMParam.append("False")



   i = 0
   for abc in cruiseNumber:
      print cruiseNumber[i]
      print outPath[i]
      print lsssFile[i]
      print dbDir[i]
      print ek60File[i]
      print workFile[i]
      print IMParam[i]
      print EMParam[i]
      print "---\n"
      i = i + 1

   EchoConvProcess.processLSSS(cruiseNumber, outPath, lsssFile, dbDir, ek60File, workFile, IMParam, EMParam, processRaw, overwrite) 

if __name__ == "__main__":
   main(sys.argv[1:])

