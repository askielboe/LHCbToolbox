#! /usr/bin/env python

import re
import sys
import string
import array

# Define the logfiles you want to compare
logfiles = ['trial.log'
            ]

# Define the lines you are interested in
relines = ["Hlt1SingleMuonNoIP",
           "Hlt1SingleMuonIP",
           "Hlt1MuonPrep",
           "Hlt1DiMuon"
           ]

# Define class for analysis
## class Data:
##     a = 3.1415
##     for i in range(len(logfiles)):
##         vars()["file"+str(i)] = i


## print Data.a
## print Data.file1


# ------------ FUNCTIONS --------------

def FindConf(file):
    f = open(file, 'r')
    f.readline()
    EOF = EOF(line)
    while not EOF:
        m = re.search("(Using trigger threshold settings \")(.+)(\" )",line)
        if m:
            print "# ------------------------------------------------ #"
            print "# Configuration file: ", m.group(2)
            print "# ------------------------------------------------ #"
        else:
            return False
        
        while notEOF:
            if FindConf(line):
                print FindConf(line)
                break
            else:
                line = f.readline()

def FindLines(line):
    global relines
    result = False
    # Find trigger lines of interest and parse their contents
    for regex in relines:
        m = re.search("(^" + regex + "[a-zA-Z0-9]+)",line)
        if m and re.search("SUCCESS",line):
            result =  m.group(0) # If we get a match print the whole line
            break # No need to parse the rest of the regexpressions
    return result

def FindAccept(line):
    m = re.search("(\#accept\"\s+)(.+)(-------   \|   ------)",line)
    if m:
        return m.group(2)
    else:
        return False

def EOF(line):
    # Break if EOF
    if len(line) == 0:
        return True
    else:
        return False
    
def main():
    global logfiles
    for file in logfiles:
        print "Opening file: ", file
        
        f = open(file, 'r')
        
        line = f.readline()
        
        while not EOF(line):

            if FindLines(line):
                LineName = FindLines(line)
                f.readline() # Skip a line
                while not EOF(line):
                    if FindAccept(line) == False:
                        line = f.readline()
                    else:
                        space = 50-len(LineName)
                        print LineName + " " * space   + FindAccept(line)
                        break

            line = f.readline()

if __name__ == "__main__":
    main()
