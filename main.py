import sys
import os

from src.config.config import Config
from src.preProcessor.preProcessor import PreProcessor

def main(argv):
    print('automizedDoE started')

    # get path to working dir cli input and set it to working dir
    pathToWorkingDir = str(argv[0])
    os.chdir(pathToWorkingDir)
    print('\tWorking dir is: %s'%pathToWorkingDir)

    config = Config()
    if config.preProcessing==True:
        preProcessor = PreProcessor(config)

    print('automizedDoE done')

if __name__ == "__main__":
    main(sys.argv[1:])