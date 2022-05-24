import configparser

class Config():

    def __init__(self):
        self.__checkConfig()

        self.preProcessing = False
        self.processing = False
        self.postProcessing = False

        self.pathToParameterFile = ''
        self.pathToFactorFile = ''
        self.pathToSimulationFolder = ''

        config = configparser.ConfigParser()
        config.read('./config.conf')

        self.__parseGeneralConfig(config)

        if self.preProcessing:
            self.planSettings = {}
            self.__parsePreProcessorConfig(config)

        if self.processing:
            self.__parseProcessorConfig(config)

        if self.postProcessing:
            self.__parsePostProcessorConfig(config)

        print('\tConfig file read')

    def __parseGeneralConfig(self, config: configparser):
        self.preProcessing = (config['GENERAL']['preProcessing'] in ['true', 'True', 'TRUE'])
        self.processing = (config['GENERAL']['processing'] in ['true', 'True', 'TRUE'])
        self.postProcessing = (config['GENERAL']['postProcessing'] in ['true', 'True', 'TRUE'])

    def __parsePreProcessorConfig(self, config: configparser):
        self.planType = config['PRE_PROCESSOR']['planType']
        # settings for pydoe based plans
        if 'pydoe' in self.planType.lower():
            self.planCommand = config['PRE_PROCESSOR']['planCommand']
        # settings for custom plans
        if 'custom' in self.planType.lower():
            self.planPath = config['PRE_PROCESSOR']['planPath']

    def __parseProcessorConfig(self, config: configparser):
        self.startScript = config['PROCESSOR']['startScript']
        self.nWorker = int(config['PROCESSOR']['nWorker'])
        self.executeTests = config['PROCESSOR']['executeTests']

    def __parsePostProcessorConfig(self, config: configparser):
        self.extractScript = config['POST_PROCESSOR']['extractScript']

    def __checkConfig(self):
        # TODO
        pass