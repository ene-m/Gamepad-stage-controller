import time
import pygame
from Stages.commands_syntax import *

def home_phi(gamepad):
    # Switch Modbus 'x' on
    command = add_error_code(':04050427FF00')
    send_cmd(gamepad.com_port, command, True)

    # Switch SERVO on for X axis
    command = add_error_code(':04050403FF00')
    send_cmd(gamepad.com_port, command, True)

    # Home X axis
    command = add_error_code(':0405040BFF00')
    send_cmd(gamepad.com_port, command, True)

    # Homing off command for X axis
    command = add_error_code(':0405040B0000')
    send_cmd(gamepad.com_port, command, True)

    # Flag to indicate completion
    homing_completed = False

    while not homing_completed:
        command = add_error_code(':040390050001')
        response, _ = send_cmd(gamepad.com_port, command, True)
        
        if "98EF" in response:
            print("Homing process for Phi axis completed successfully.")
            homing_completed = True
            gamepad.distance_phi = 0
        else:
            print("Waiting for Phi axis homing to complete... Response: ", response)

        time.sleep(0.5)

    return 1

def get_position_phi(gamepad):
    # Send the command to get the X position
    command = add_error_code(':040390000002')
    response, _ = send_cmd(gamepad.com_port, command, True)
    
    # Extract the number of bytes encoding the position from the response
    n_bytes = int(response[5:7], 16)  # Adjusted index for Python string
    
    # Extract the position encoded in the response
    position_hex = response[7:7 + 2*n_bytes]
    position = int(position_hex, 16) / 100.0  # Convert from 1:100 mm to mm
    
    print(f"Current phi position: {position}mm")
    print(f"Virtual phi position: {gamepad.distance_phi}mm")
    gamepad.distance_phi = position
    return position

def move_phi(gamepad, value):
  
    # Update distance_phi based on input value and step size
    gamepad.distance_phi += get_sign(value) * gamepad.step_size
    gamepad.distance_phi = max(5, gamepad.distance_phi)  # Ensure distance is non-negative
    gamepad.distance_phi = min(355, gamepad.distance_phi)  # Ensure distance is within 0-360 degrees


    # Define speed and acceleration for Phi movement
    speed_phi = gamepad.step_size
    acceleration_phi = 0.3 # Default acceleration value, with other values nstage crashes

    # Format distance, speed, and acceleration as hexadecimal strings
    distance_hex_phi = format_hex(int(gamepad.distance_phi * 100), 8)
    speed_hex_phi = format_hex(int(speed_phi * 100), 8)
    acceleration_hex_phi = format_hex(int(acceleration_phi * 100), 4)

    # Construct the command string for moving the Phi stage
    command_phi = f'04109900000912{distance_hex_phi}00000001{speed_hex_phi[:4]}{speed_hex_phi[4:]}{acceleration_hex_phi}00000000'
    complete_command_phi = f':{command_phi}'  # Add colon at the beginning for command formatting

    # Calculate checksum for the command
    checksum_phi = calculate_checksum(complete_command_phi)

    # Append checksum to the command string
    complete_command_with_checksum_phi = f'{complete_command_phi}{checksum_phi}'

    # Print the constructed command for debugging purposes
    print(f"Constructed command for sending Phi: {complete_command_with_checksum_phi}")
    print(f"Virtual Phi position: {gamepad.distance_phi} degrees")

    # Send the command to move the Phi stage (not actually sent due to early return)
    send_cmd(gamepad.com_port, complete_command_with_checksum_phi, True)