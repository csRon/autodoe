import sys
import os

from src.config.config import Config
from src.preProcessor.preProcessor import PreProcessor
from src.processor.processor import Processor


def main(argv):
    print('automizedDoE started')

    # get path to working dir cli input and set it to working dir
    pathToWorkingDir = str(argv[0])
    os.chdir(pathToWorkingDir)
    print('\tWorking dir is: %s'%pathToWorkingDir)

    config = Config()
    if config.preProcessing==True:
        preProcessor = PreProcessor(config)

    if config.processing == True:
        processor = Processor(config)

if __name__ == "__main__":
    main(sys.argv[1:])