import pandas as pd
class StatsOp:
   
    #constructor
    def __init__(self):
        self.columns = []
        self.rows = []
    
    #update value
    def updateCell(self, col, row, value):
        df = self.data
        df.set_value(row, col, value)
        self.data = df
    
    #append value (row) into given column
    def insertRow(self, col, value):
        df = self.data
        dfTemp = pd.DataFrame(df.iloc[[0]])
        for i, row in dfTemp.iterrows():
            for colName in list(df):
                dfTemp.loc[i, colName] = np.nan
        dfTemp.set_value(0, col, value)
        df = df.append(dfTemp)
        df = df.reset_index(drop=True)
        self.data = df
    
    
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
    #consider formats to handle...
    def setData(self, fName):
        self.data = pd.read_csv(fName)
    
    def getData(self):
        return self.data
    
    def calculateColumnsMean(self):
        dataframe = self.data
        columns = self.columns
        result = []
        for col in columns:
            mean = dataframe[col].mean()
            result.append(mean)
            print(col + " " + str(mean))
        return result
       
    def describeColumn(self):
        dataframe = self.data
        columns = self.columns
        result = []
        for col in columns:
            #description is a dataframe
            description = dataframe[col].describe()
            result.append(description)
        return result    
    
    def calculateRowsMean(self):
        dataframe = self.data
        rows = self.rows
        result = []
        for row in rows:
            mean = dataframe.iloc[row].mean()
            result.append(mean)
        return result
    
    #print column
    def printColumn(self,col):
        df = self.data
        print(df[col])
    
    
    #print row
    def printRow(self,row):
        df = self.data
        print(df.iloc[[row]])
        
    #List of all column and row names
    def getColumnNames(self):
        df = self.data
        return list(df)
    
    def getRowNames(self):
        df = self.data
        return list(df.index)
    
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
    