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

        print('\tConfig file read')


    def __parseGeneralConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.conf')

        self.preProcessing = (config['GENERAL']['preProcessing'] in ['true', 'True', 'TRUE'])
        self.processing = (config['GENERAL']['processing'] in ['true', 'True', 'TRUE'])

        self.pathToParameterFile = config['GENERAL']['pathToParameterFile']
        self.pathToFactorFile = config['GENERAL']['pathToFactorFile']
        self.pathToSimulationFolder = config['GENERAL']['pathToSimulationFolder']
        self.pathToTemplateFolder = config['GENERAL']['pathToTemplateFolder']


    def __parsePreProcessorConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.conf')

        self.planType = config['PRE_PROCESSOR']['planType']
        self.planCommand = config['PRE_PROCESSOR']['planCommand']

    def __parseProcessorConfig(self):
        config = configparser.ConfigParser()
        config.read('./config.conf')

        for key in config['PROCESSOR']:
            self.processorSettings[key] = config['PROCESSOR'][key]

    def __checkConfig(self):
        # TODO
        pass