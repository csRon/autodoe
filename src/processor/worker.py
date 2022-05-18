import os
import pandas
import time
import numpy as np

from ..config.config import Config
from ..preProcessor.experimentalPlans.experimentalPlan import ExperimentalPlan

class Worker:

    def __init__(self, pathToWorkDir: str, testNr: int):
        print('\t\t\t Simulation started: %s'%pathToWorkDir)