import configparser

class Config():

    def __init__(self):
        self.__checkConfig()

        self.preProcessing = True
        self.processing = True

        self.pathToParameterFile = ''
        self.pathToFactorFile = ''
        self.pathToSimulationFolder = ''

        self.__parseGeneralConfig()

        if self.preProcessing:
            self.planSettings = {}
            self.__parsePreProcessorConfig()

        if self.processing:
            self.processorSettings = self.__parseProcessorConfig()


    def __parseGeneralConfig(self, pathToConfig:str):
        config = configparser.ConfigParser()
        config.read(pathToConfig)

        self.preProcessing = config['GENERAL']['preprocessing'] == 'true'
        self.processing = config['GENERAL']['processing'] == 'true'

        self.pathToParameterFile = config['GENERAL']['pathtoparameterfile']
        self.pathToFactorFile = config['GENERAL']['pathtofactorfile']
        self.pathToSimulationFolder = config['GENERAL']['pathtosimulationfolder']
        self.pathToTemplateFolder = config['GENERAL']['pathtotemplatenfolder']


    def __parsePreProcessorConfig(self, pathToConfig:str):
        config = configparser.ConfigParser()
        config.read(pathToConfig)

        for key in config['PRE_PROCESSOR']:
            self.planSettings[key] = config['PRE_PROCESSOR'][key]

    def __parseProcessorConfig(self, pathToConfig: str):
        config = configparser.ConfigParser()
        config.read(pathToConfig)

        for key in config['PROCESSOR']:
            self.processorSettings[key] = config['PROCESSOR'][key]

    def __checkConfig(self):
        # TODO
        pass