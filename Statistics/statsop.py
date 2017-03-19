import pandas as pd
import os
import os.path
import fnmatch

class StatsOp:
   
    #constructor
    def __init__(self):
        self.isInitialized = False
        self.columns = []
        self.rows = []
    
    #update value
    def updateCell(self, col, row, value):
        if self.isInitialized:
            df = self.data
            df.set_value(row, col, value)
            self.data = df
        else:
            return None
    
    #append value (row) into given column
    def insertRow(self, col, value):
        if self.isInitialized:
            df = self.data
            dfTemp = pd.DataFrame(df.iloc[[0]])
            for i, row in dfTemp.iterrows():
                for colName in list(df):
                    dfTemp.loc[i, colName] = np.nan
            dfTemp.set_value(0, col, value)
            df = df.append(dfTemp)
            df = df.reset_index(drop=True)
            self.data = df
        else:
            return None
    
    
    #getter and setter for operation
    def setOperation(self, op):
        self.operation = op
        
    def getOperation(self):
        return self.operation
 
    
    #getter & setter for the filename
    def setFilename(self, fName):
        self.fileName = fName
    
    def getFilename(self):
        return self.fileName
    
    #reads in csv file into a dataframe and stores that df as data
    #TODO: handle cases where the file is not in the format of csv...
    def setData(self, fName):
        #name.csv
        hasExtension = fName.find(".")
        status = False
        if hasExtension < 0:
            filename = fName + ".csv"
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, '*.csv'):
                    if filename == file:
                        fName = filename
                        status = True
        else:
            status = os.path.isfile(fName)

        if status:
            self.data = pd.read_csv(fName)
            self.isInitialized = True
        else:
            print("404 File:" + fName +" Not Found")
        self.isInitialized = status
        return status
    
    def checkInitialized(self):
        return self.isInitialized
    
    def getData(self):
        if self.isInitialized:
            return self.data
        else:
            return None
    
    def calculateColumnsMean(self):
        if self.isInitialized:
            dataframe = self.data
            columns = self.columns
            result = []
            for col in columns:
                mean = dataframe[col].mean()
                result.append(mean)
                print(col + " " + str(mean))
            return result
        else:
            return None
       
    def describeColumn(self):
        if self.isInitialized:
            dataframe = self.data
            columns = self.columns
            result = []
            for col in columns:
                #description is a dataframe
                description = dataframe[col].describe()
                result.append(description)
            return result
        else:
            return None
    
    def calculateRowsMean(self):
        if self.isInitialized:
            dataframe = self.data
            rows = self.rows
            result = []
            for row in rows:
                mean = dataframe.iloc[row].mean()
                result.append(mean)
            return result
        else:
            return None
    
    #print column
    def printColumn(self,col):
        if self.isInitialized:
            df = self.data
            print(df[col])
        else:
            print("No Data Available")
    
    
    #print row
    def printRow(self,row):
        if self.isInitialized:
            df = self.data
            print(df.iloc[[row]])
        else:
            print("No Data Available")
        
    #List of all column and row names
    def getColumnNames(self):
        if self.isInitialized:
            df = self.data
            return list(df)
        else:
            return None
    
    def getRowNames(self):
        if self.isInitialized:
            df = self.data
            return list(df.index)
        else:
            return None
    
    #Unused for now...
    
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
    
        
    #example function    
    def testFunc(self):
        return 'hello world'
    