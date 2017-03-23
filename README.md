# SimpleStats
Class project for ECS 240 programming languages

Requires Python Version 3.5+

Deploy Instructions:
Open console or terminal
   Run the following command in terminal `python main.py`
   Running `python main.py -d` can run the program in debug mode
   Either provide a dataset or use our dummydata set 
    (dataset should be a .csv and in the same dir as main.py)
   Ask your questions

Example commands would be:

To initialize a data set:
open sample.csv
read sample.csv

To view the data set:
show me everything
show the spreadsheet

To view a particular column/row/cell:
column 1
row 0
what is cell b4

set commands -- changing a cell won't save to file:
set a0 to 0
set a0 to the average of column 2 and 3

stat commands -- supports median, mean, std deviation, min, and max:
get the average of column 1
get the median of column 2,3 and 4
what is the standard deviation of row 0 and 1
what is the maximum of row 0
min of row 0

