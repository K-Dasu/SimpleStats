import pandas as pd
class StatsOp:
   
    #constructor
    def __init__(self):
        self.columns = []
        self.rows = []
    
    #getter and setter for operation
    def setOperation(self, op):
        self.operation = op
        
    def getOperation(self):
        return self.operation
    
    #getter & setter for columns
    #set column array = array
    def setColumns(self, cols):
        self.columns = cols
    #add columns to the array
    def addColumn(self, col):
        self.columns.append(col)
    
    def getColumns(self):
        return self.columns
    
    #getter & setter for row
    #set array = array
    def setRows(self, rows):
        self.rows = rows
    #add individual rows    
    def addRow(self, row):
        self.rows.append(row)
        
    def getRows(self):
        return self.rows
    
    #getter & setter for the filename
    def setFilename(self, fName):
        self.fileName = fName
    
    def getFilename(self):
        return self.fileName
    
    #reads in csv file into a dataframe and stores that df as data
    #TODO: handle cases where the file is not in the format of csv...
    #consider formats to handle...
    def setData(self, fName):
        self.data = pd.read_csv(fName)
    
    def getData(self):
        return self.data
    
    def calculateColumnsMean(self):
        dataframe = self.data
        columns = self.columns
        for col in columns:
            print(col + " " + str(dataframe[col].mean()))
                       
    def calculateRowsMean(self):
        dataframe = self.data
        rows = self.rows
        for row in rows:
            print("Row " + str(row)+ " " + str(dataframe.iloc[row].mean()))
    
        
    #example function    
    def testFunc(self):
        return 'hello world'
    