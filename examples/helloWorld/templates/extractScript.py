import re
import pandas as pd

# open file with results
with open('simulation.log') as logFile:
    resultDict = {}

    # loop through file that contains the results
    for line in logFile:
        # filter lines with result and store value in resultDict as str
        if 'f1' in line:
            resultDict['f1'] = float(re.findall(r'-?\d+\.\d+', line)[0])
        if 'f2' in line:
            resultDict['f2'] = float(re.findall(r'-?\d+\.\d+', line)[0])

# write resultDict to csv file filteredResults.csv
print(resultDict)
pd.DataFrame.from_dict([resultDict]).to_csv(r'filteredResults.csv', index=False, header=True)
