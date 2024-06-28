from Stages.commands_syntax import *
from Stages.x_stage import *
from Stages.y_stage import *
from Stages.z_stage import *
from Stages.phi_stage import *
import time
from Stages.commands import *

# This file contains the GamePadState class, which is used to store the state of the gamepad. 
class GamePadState:
    """
    Represents the state and behavior of a gamepad controller.
    """

    def __init__(self):
        """
        Initialize the GamePadState object with default values for gamepad state.
        """
        # Profiles for gamepad
        self.all_profiles = {'Analog_sticks': 0, 'D_Pad': 1}
        self.profile = 'Analog_sticks'  # Default profile set to 'Analog_sticks'

        # Initial distances of stages
        self.distance_x = 0
        self.distance_y = 0
        self.distance_z = 0
        self.distance_phi = 0

        # Default step size and acceleration
        self.step_size = 0.3
        self.acceleration = 0.5

        # Running state of the gamepad
        self.running = True

        # Communication port for external devices
        self.com_port = 'COM3'

        # Define the buttons and their corresponding indices
        self.buttons = {
            'home_x': 0,
            'home_y': 1,
            'home_z': 4,
            'home_phi': 3,
            'get_position': 11,
            'change_profile': 7,
            'change_step_size': 10,
            'exit': 12
        }

        # Define the axis and their corresponding indices
        self.Axis = {
            'X': 0,
            'Y': 1,
            'Z': 4,
            'phi': 100  # Default value indicating 'not used' for phi axis
        }

        # Define the D-Pad and their corresponding indices
        self.D_Pad = {
            'phi': 0,   # Phi control on D-Pad
            'XY': 100   # Default value indicating 'not used' for XY control on D-Pad
        }

        # Define the functions associated with the buttons
        self.button_functions = {
            'home_x': home_x,
            'home_y': home_y,
            'home_z': home_z,
            'home_phi': home_phi,
            'change_profile': change_profile,
            'exit': stop,
            'change_step_size': change_step_size,
            'get_position': get_position,
        }

        # Define the functions associated with the axis
        self.axis_functions = {
            'X': move_X_analog,
            'Y': move_Y_analog,
            'Z': move_z,
            'phi': move_phi
        }

        # Define the functions associated with the D-Pad
        self.D_pad_functions = {
            'phi': self.move_phi_Dpad,
            'XY': self.move_XY_Dpad
        }

        print("GamePadState initialized with 'Analog_sticks' profile.")

    def move_XY_Dpad(self, com_port, value):
        """
        Handle movement commands for XY D-Pad control.

        Args:
            com_port (str): The COM port for communication with external devices.
            value (tuple): Tuple containing X and Y values from the D-Pad.

        Notes:
            This method is necessary to separate X and Y values from the D-Pad input.
        """
        time_to_wait = 0

        # Move X stage if X value is non-zero
        if value[0] != 0:
            move_X_Dpad(self, value[0])

        # Move Y stage if Y value is non-zero
        if value[1] != 0:
            move_Y_Dpad(self, value[1])

    def move_phi_Dpad(self, value):
        """
        Handle movement commands for phi D-Pad control.

        Args:
            value (tuple): Tuple containing X and Y values from the D-Pad.

        Notes:
            This method is necessary to separate X and Y values from the D-Pad input.
        """
        

        # Move phi stage if X value is non-zero
        if value[0] != 0:
            move_phi(self, value[0])
