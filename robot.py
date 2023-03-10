#!/usr/bin/env python3

from wpilib.command import Command
Command.isFinished = lambda x: False

from commandbased import CommandBasedRobot
from wpilib._impl.main import run
from wpilib import RobotBase


#from custom import driverhud
import controller.layout
import subsystems
import shutil, sys

from wpilib.command import Subsystem

from subsystems.monitor import Monitor as monitor
from subsystems.potentiometer import PotentiometerInterface as potentiometer
from subsystems.motors import Motors as motors

class KryptonBot(CommandBasedRobot):
    '''Implements a Command Based robot design'''

    def robotInit(self):
        '''Set up everything we need for a working robot.'''

        if RobotBase.isSimulation():
            import mockdata

        self.subsystems()
        controller.layout.init()
        #driverhud.init()

        from commands.startupcommandgroup import StartUpCommandGroup
        StartUpCommandGroup().start()


    def autonomousInit(self):
        '''This function is called each time autonomous mode starts.'''
        pass
        # Send field data to the dashboard
        # Schedule the autonomous command


    def handleCrash(self, error):
        super().handleCrash()
        pass

    @classmethod
    def subsystems(cls):
        vars = globals()
        module = sys.modules['robot']
        for key, var in vars.items():
            try:
                if issubclass(var, Subsystem) and var is not Subsystem:
                    setattr(module, key, var())
            except TypeError:
                pass


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'deploy':
        shutil.rmtree('opkg_cache', ignore_errors=True)
        shutil.rmtree('pip_cache', ignore_errors=True)

    run(KryptonBot)
