
# coding: utf-8


import pandas as pd
import sys


def checkArgsize():
    argLen = len(sys.argv)
    if argLen <= 1:
        print("Not enough arguements exiting...")
        return False
    
    print(sys.argv)
    return argLen

def runStatsOperation(arguements):
    datasource = pd.read_csv(arguements["filename"])
#     datasource = pd.read_csv("dummydata.csv")
    if arguements["operation"] == "boxplot":
        print("calculating boxplot values....")
    print(datasource)

def simplestats():
    #read in file to process
    argLen = checkArgsize()
    arguements = {"operation":"", "filename":"", "columns":"", "rows":""}
    if argLen:
        #TODO think of a better solution...
        for idx, arg in enumerate(sys.argv):
            if idx == 1:
                arguements["operation"] = arg
            elif idx == 2:
                arguements["filename"] = arg
            elif idx == 3:
                arguements["columns"] = arg
            elif idx == 4:
                arguements["rows"] = arg
            print(arg)
    print(arguements)
    runStatsOperation(arguements)   
        
        
simplestats()