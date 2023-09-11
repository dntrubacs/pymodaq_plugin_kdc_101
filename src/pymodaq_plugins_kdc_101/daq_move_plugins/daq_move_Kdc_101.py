"""
Created by Daniel-Iosif Trubacs for the UoS QLM group on 4 August 2023. The
purpose of this module is to create a pymodaq plugin for the KDC101 brushed
motors.


Last update: 30 August 2023
"""

from pymodaq.control_modules.move_utility_classes import DAQ_Move_base
from pymodaq.control_modules.move_utility_classes import comon_parameters_fun
from pymodaq.control_modules.move_utility_classes import main
from pymodaq.utils.daq_utils import ThreadCommand
from pymodaq.utils.parameter import Parameter
from src.pymodaq_plugins_kdc_101.hardware.thorlabs_kdc_101 import KDC101Com
from src.pymodaq_plugins_kdc_101.hardware.coms import find_available_kdc_101

class DAQ_Move_Kdc_101(DAQ_Move_base):
    """Pymodaq plugin for the KDC101 Brushed Motor Controller. """
    # inner attributes for pymodaq
    _controller_units = 'mm'
    _epsilon = 0.05
    is_multiaxes = False

    # check if there are any KDC101 motors available
    try:
        find_available_kdc_101()
    except Exception as ex:
        print(Exception)
        print('No KDC101 connected to this computer could have been found. '
              'Check whether the motor is properly connected or whether the '
              'correct Thorlabs software has been installed.')

    stage_names = []
    params = comon_parameters_fun(is_multiaxes, epsilon=_epsilon)

    def ini_attributes(self):
        print('No attributes to be initiated')

    def get_actuator_value(self):
        return self.controller.get_current_position()

    def close(self):
        # Terminate the communication protocol. Not needed now.
        raise Exception('The termination of the communication protocol is'
                        'not implemented')

    def commit_settings(self):
        print('No settings to be committed for now.')

    def ini_stage(self):
        # connect to the KDC101 brushed motor
        self.controller = KDC101Com()

    def move_abs(self, value):
        # move to an absolute position
        self.controller.move_to_position(position=value)

    def move_rel(self, value):
        # move a relative value with regard to the current position
        current_position = self.get_actuator_value()
        self.controller.move_to_position(position=current_position+value)

    def move_home(self):
        # move to position 0
        self.controller.move_to_position(position=0)

    def stop_motion(self):
        print('The motors automatically stops when it reaches the given '
              'position')
        self.emit_status(
            ThreadCommand('Update_Status',
                          [f'Motor stopped at position '
                           f'{self.get_actuator_value()}.']))


if __name__ == '__main__':
    main(__file__)