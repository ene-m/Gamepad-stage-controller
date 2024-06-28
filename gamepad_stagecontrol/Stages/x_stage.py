import time
import pygame
from Stages.commands_syntax import *


def home_x(gamepad):
    # Switch Modbus 'x' on
    command = add_error_code(':03050427FF00')
    send_cmd(gamepad.com_port, command, True)

    # Switch SERVO on for X axis
    command = add_error_code(':03050403FF00')
    send_cmd(gamepad.com_port, command, True)

    # Home X axis
    command = add_error_code(':0305040BFF00')
    send_cmd(gamepad.com_port, command, True)

    # Homing off command for X axis
    command = add_error_code(':0305040B0000')
    send_cmd(gamepad.com_port, command, True)

    # Flag to indicate completion
    homing_completed = False

    while not homing_completed:
        command = add_error_code(':030390050001')
        response, _ = send_cmd(gamepad.com_port, command, True)
        
        if "98F0" in response:
            print("Homing process for X axis completed successfully.")
            homing_completed = True
            gamepad.distance_x = 0
        else:
            print("Waiting for X axis homing to complete... Response: ", response)

        time.sleep(0.5)

    return 1

def get_position_x(gamepad):
    # Send the command to get the X position
    command = add_error_code(':030390000002')
    response, _ = send_cmd(gamepad.com_port, command, True)
    
    # Extract the number of bytes encoding the position from the response
    n_bytes = int(response[5:7], 16)  # Adjusted index for Python string
    
    # Extract the position encoded in the response
    position_hex = response[7:7 + 2*n_bytes]
    position = int(position_hex, 16) / 100.0  # Convert from 1:100 mm to mm
    
    print(f"Current X position: {position}mm")
    print(f"Virtual X position: {gamepad.distance_x}mm")
    gamepad.distance_x = position
    return position

def move_X_analog(gamepad, value):
    # Move the X stage by the given value
    gamepad.distance_x += -1 *value * gamepad.step_size   
    gamepad.distance_x = max(0, gamepad.distance_x)    
    # Define the speed and acceleration for the movement
    speed_x = gamepad.step_size   
    acceleration_x = gamepad.acceleration   
    #Format the distance, speed and acceleration as hexadecimal strings
    distance_hex_x = format_hex(int(gamepad.distance_x * 100), 8)   
    speed_hex_x = format_hex(int(speed_x * 100), 8)   
    acceleration_hex_x = format_hex(int(acceleration_x * 100), 4)   
    # Construct the command string for moving the X stage
    command_x = f'03109900000912{distance_hex_x}00000001{speed_hex_x[:4]}{speed_hex_x[4:]}{acceleration_hex_x}00000000'   
    # Add the checksum to the command string
    complete_command_x = f':{command_x}'    
    # Calculate the checksum for the command
    checksum_x = calculate_checksum(complete_command_x)   
    # Add the checksum to the command string
    complete_command_with_checksum_x = f'{complete_command_x}{checksum_x}' 

    print(f"Constructed command for sending X: {complete_command_with_checksum_x}")
    # Send the command to the X stage
    send_cmd(gamepad.com_port, complete_command_with_checksum_x, True)
    # Wait for the movement to complete
    time.sleep(gamepad.step_size/speed_x)

def move_X_Dpad(gamepad, value):
    # Adjust the distance based on the D-pad input and step size
    gamepad.distance_x += -1 * value * gamepad.step_size
    gamepad.distance_x = max(0, gamepad.distance_x)

    # Define speed and acceleration for X movement
    speed_x = gamepad.step_size
    acceleration_x = gamepad.acceleration

    # Format distance, speed, and acceleration as hexadecimal strings
    distance_hex_x = format_hex(int(gamepad.distance_x * 100), 8)
    speed_hex_x = format_hex(int(speed_x * 100), 8)
    acceleration_hex_x = format_hex(int(acceleration_x * 100), 4)

    # Construct the command string for moving the X stage
    command_x = f'03109900000912{distance_hex_x}00000001{speed_hex_x[:4]}{speed_hex_x[4:]}{acceleration_hex_x}00000000'
    complete_command_x = f':{command_x}'  # Add colon at the beginning for command formatting

    # Calculate checksum for the command
    checksum_x = calculate_checksum(complete_command_x)

    # Append checksum to the command string
    complete_command_with_checksum_x = f'{complete_command_x}{checksum_x}'

    # Print the constructed command for debugging purposes
    print(f"Constructed command for sending X: {complete_command_with_checksum_x}")

    # Calculate time to wait for movement completion
    time_to_wait = gamepad.step_size / speed_x

    # Send the command to move the X stage
    send_cmd(gamepad.com_port, complete_command_with_checksum_x, True)

    # Wait for the movement to complete
    time.sleep(time_to_wait)
