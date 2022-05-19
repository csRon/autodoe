import re
import pandas as pd

# open file with results
with open('simulation.log') as logFile:
    resultDict = {}

    # loop through file that contains the results
    for line in logFile:
        # filter lines with result and store value in resultDict as str
        if 'output1' in line:
            resultDict['output1'] = float(re.findall(r'-?\d+\.\d+', line)[0])
        if 'output2' in line:
            resultDict['output2'] = float(re.findall(r'-?\d+\.\d+', line)[0])

# write resultDict to csv file filteredResults.csv
pd.DataFrame.from_dict([resultDict]).to_csv(r'filteredResults.csv', index=False, header=True)
