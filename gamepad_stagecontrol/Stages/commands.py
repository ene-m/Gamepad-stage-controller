from Stages.commands_syntax import *
from Stages.x_stage import *
from Stages.y_stage import *
from Stages.z_stage import *
from Stages.phi_stage import *
import time

# Functions for the gamepad buttons

def change_profile(gamepad):
    """
    Change the profile of the gamepad between Analog_sticks and D_Pad.

    Args:
        gamepad (GamePadState): The GamePadState object representing the gamepad state.

    Notes:
        - Changes the axis and D-Pad values accordingly.
        - Adjusts step sizes for both linear and phi movements.
    """
    if gamepad.profile == 'Analog_sticks':
        # Switch to D_Pad profile
        gamepad.profile = 'D_Pad'
        gamepad.Axis = {
            'Z': 4,
            'phi': 0,
            'X': 100,
            'Y': 100
        }
        gamepad.D_Pad = {
            'XY': 0,
            'phi': 100
        }
        gamepad.step_size = 0.03
        gamepad.step_size_phi = 0.03
        
        print(f"Profile changed to {gamepad.profile} mode.")
        
    elif gamepad.profile == 'D_Pad':
        # Switch to Analog_sticks profile
        gamepad.profile = 'Analog_sticks'
        gamepad.Axis = {
            'X': 0,
            'Y': 1,
            'Z': 4,
            'phi': 100
        }
        gamepad.D_Pad = {
            'phi': 0,
            'XY': 100
        }
        gamepad.step_size = 0.3
        gamepad.step_size_phi = 0.3
        
        print(f"Profile changed to {gamepad.profile} mode.")


def change_step_size(gamepad):
    """
    Change the step size of the stages.

    Args:
        gamepad (GamePadState): The GamePadState object representing the gamepad state.

    Notes:
        - Input step size is set for both linear and phi movements.
    """
    step_size = float(input("Enter desired stepsize: "))
    gamepad.step_size = step_size
    gamepad.step_size_phi = step_size
    print(f"Step size changed to {step_size}mm.")


def stop(gamepad):
    """
    Stop the movement of the stages.

    Args:
        gamepad (GamePadState): The GamePadState object representing the gamepad state.
    """
    gamepad.running = False
    print("Exiting program.")


def get_position(gamepad):
    """
    Get the position of the stages and print them.

    Args:
        gamepad (GamePadState): The GamePadState object representing the gamepad state.
    """
    get_position_x(gamepad)
    get_position_y(gamepad)
    get_position_z(gamepad)
    get_position_phi(gamepad)
