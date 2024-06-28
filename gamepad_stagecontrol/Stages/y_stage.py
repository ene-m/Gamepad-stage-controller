import time
import pygame
from Stages.commands_syntax import *

def home_y(gamepad):
    # Switch Modbus 'x' on
    command = add_error_code(':02050427FF00')
    send_cmd(gamepad.com_port, command, True)

    # Switch SERVO on for X axis
    command = add_error_code(':02050403FF00')
    send_cmd(gamepad.com_port, command, True)

    # Home X axis
    command = add_error_code(':0205040BFF00')
    send_cmd(gamepad.com_port, command, True)

    # Homing off command for X axis
    command = add_error_code(':0205040B0000')
    send_cmd(gamepad.com_port, command, True)

    # Flag to indicate completion
    homing_completed = False


def get_position_y(gamepad):
    # Send the command to get the X position
    command = add_error_code(':020390000002')
    response, _ = send_cmd(gamepad.com_port, command, True)
    
    # Extract the number of bytes encoding the position from the response
    n_bytes = int(response[5:7], 16)  # Adjusted index for Python string
    
    # Extract the position encoded in the response
    position_hex = response[7:7 + 2*n_bytes]
    position = int(position_hex, 16) / 100.0  # Convert from 1:100 mm to mm
    
    print(f"Current Y position: {position}mm")
    print(f"Virtual Y position: {gamepad.distance_y}mm")
    gamepad.distance_y = position
    return position

def move_Y_analog(gamepad, value):
    # Adjust the distance based on the analog joystick input and step size
    gamepad.distance_y += value * gamepad.step_size
    gamepad.distance_y = max(0, gamepad.distance_y)  # Ensure distance_y doesn't go below zero

    # Define speed and acceleration for Y movement
    speed_y = gamepad.step_size
    acceleration_y = gamepad.acceleration

    # Format distance, speed, and acceleration as hexadecimal strings
    distance_hex_y = format_hex(int(gamepad.distance_y * 100), 8)
    speed_hex_y = format_hex(int(speed_y * 100), 8)
    acceleration_hex_y = format_hex(int(acceleration_y * 100), 4)

    # Construct the command string for moving the Y stage
    command_y = f'02109900000912{distance_hex_y}00000001{speed_hex_y[:4]}{speed_hex_y[4:]}{acceleration_hex_y}00000000'
    complete_command_y = f':{command_y}'  # Add colon at the beginning for command formatting

    # Calculate checksum for the command
    checksum_y = calculate_checksum(complete_command_y)

    # Append checksum to the command string
    complete_command_with_checksum_y = f'{complete_command_y}{checksum_y}'

    # Print the constructed command for debugging purposes
    print(f"Constructed command for sending Y: {complete_command_with_checksum_y}")

    # Send the command to move the Y stage
    send_cmd(gamepad.com_port, complete_command_with_checksum_y, True)

    # Calculate time to wait for movement completion
    time_to_wait = gamepad.step_size / speed_y

    # Wait for the movement to complete
    time.sleep(time_to_wait)



def move_Y_Dpad(gamepad, value):
    # Adjust the distance based on the D-pad input and step size
    gamepad.distance_y += -1 * value * gamepad.step_size
    gamepad.distance_y = max(0, gamepad.distance_y)  # Ensure distance_y doesn't go below zero

    # Define speed and acceleration for Y movement
    speed_y = gamepad.step_size
    acceleration_y = gamepad.acceleration

    # Format distance, speed, and acceleration as hexadecimal strings
    distance_hex_y = format_hex(int(gamepad.distance_y * 100), 8)
    speed_hex_y = format_hex(int(speed_y * 100), 8)
    acceleration_hex_y = format_hex(int(acceleration_y * 100), 4)

    # Construct the command string for moving the Y stage
    command_y = f'02109900000912{distance_hex_y}00000001{speed_hex_y[:4]}{speed_hex_y[4:]}{acceleration_hex_y}00000000'
    complete_command_y = f':{command_y}'  # Add colon at the beginning for command formatting

    # Calculate checksum for the command
    checksum_y = calculate_checksum(complete_command_y)

    # Append checksum to the command string
    complete_command_with_checksum_y = f'{complete_command_y}{checksum_y}'

    # Print the constructed command for debugging purposes
    print(f"Constructed command for sending Y: {complete_command_with_checksum_y}")

    # Calculate time to wait for movement completion
    time_to_wait = gamepad.step_size / speed_y

    # Send the command to move the Y stage
    send_cmd(gamepad.com_port, complete_command_with_checksum_y, True)

    # Wait for the movement to complete
    time.sleep(time_to_wait)
