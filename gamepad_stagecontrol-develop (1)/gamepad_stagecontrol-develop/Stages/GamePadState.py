from Stages.commands_syntax import *
from Stages.x_stage import *
from Stages.y_stage import *
from Stages.z_stage import *
from Stages.phi_stage import *
import time
from Stages.commands import *

# This file contains the GamePadState class, which is used to store the state of the gamepad. 
class GamePadState:
    # Initialize the GamePadState object with the default values for the gamepad state.
    def __init__(self):
        self.all_profiles = {'Analog_sticks': 0, 'D_Pad': 1}
        self.profile = 'Analog_sticks'
        self.distance_x = 0
        self.distance_y = 0
        self.distance_z = 0
        self.distance_phi = 0
        self.step_size = 0.3
        self.acceleration = 0.5
        self.running = True
        self.com_port = 'COM3'

        # Define the buttons and their corresponding values
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
        
        # Define the axis and their corresponding values
        self.Axis = {
        'X': 0,
        'Y': 1,
        'Z':4,
        'phi': 100
        
        }

        # Define the D-Pad and their corresponding values
        self.D_Pad = {
        'phi' : 0,
        'XY' : 100
        
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
            'X': self.move_X_analog,
            'Y': self.move_Y_analog,
            'Z': self.move_z,
            'phi': self.move_phi
        }
        
        # Define the functions associated with the D-Pad
        self.D_pad_functions = {
            'phi': self.move_phi,
            'XY': self.move_XY_Dpad
        }
        
        print("GamePadState initialized with 'Analog_sticks' profile.")

    # This method is neccesary beacuse the D_pad gives a tuple with the x and y values, we need to separate the values to be consisten with the rest of the code

    def move_XY_Dpad(self, com_port, value):
        time_to_wait = 0
        if value[0] != 0:
            move_X_Dpad(com_port, value[0])

        if value[1] != 0:
            move_Y_Dpad(com_port, value[1])

        time.sleep(time_to_wait)
    