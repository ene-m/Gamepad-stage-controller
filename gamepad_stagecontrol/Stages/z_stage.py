import time
import pygame
from Stages.commands_syntax import *

def home_z(gamepad):
    # Switch Modbus 'z' on
    command = add_error_code(':01050427FF00')
    send_cmd(gamepad, command, True)

    # Switch SERVO on
    command = add_error_code(':01050403FF00')
    send_cmd(gamepad, command, True)

    # Home Device
    command = add_error_code(':0105040BFF00')
    send_cmd(gamepad, command, True)

    # Homing off command
    command = add_error_code(':0105040B0000')
    send_cmd(gamepad, command, True)

    # Flag to indicate completion
    homing_completed = False

    while not homing_completed:
        command = add_error_code(':010390050001')
        response, _ = send_cmd(gamepad, command, True)
        
        if "98F2" in response:
            print("Homing process completed successfully.")
            homing_completed = True
            gamepad.distance_z = 0
        else:
            print("Waiting for homing to complete... Response: ", response)

        time.sleep(0.5)

    return 1

def get_position_z(gamepad):
    # Send the command to get the Z position
    command = add_error_code(':010390000002')
    response, _ = send_cmd(gamepad, command, True)
    
    # Extract the number of bytes encoding the position from the response
    n_bytes = int(response[5:7], 16)  # Adjusted index for Python string
    
    # Extract the position encoded in the response
    # Adjusted index for Python string and multiplied by 2 since each hex digit represents half a byte
    position_hex = response[7:7 + 2*n_bytes]
    position = int(position_hex, 16) / 100.0  # Convert from 1:100 mm to mm
    print(f"Current Z position: {position}mm")
    print(f"Virtual Z position: {gamepad.distance_z}mm")
    gamepad.distance_z = position
    
    return position

def move_z(gamepad, value):
    # Adjust the distance based on the input value and step size
    gamepad.distance_z += get_sign(value) * gamepad.step_size
    gamepad.distance_z = max(0, gamepad.distance_z)  # Ensure distance_z doesn't go below zero

    # Define speed and acceleration for Z movement
    speed_z = gamepad.step_size
    acceleration_z = gamepad.acceleration

    # Format distance, speed, and acceleration as hexadecimal strings
    distance_hex_z = format_hex(int(gamepad.distance_z * 100), 8)
    speed_hex_z = format_hex(int(speed_z * 100), 8)
    acceleration_hex_z = format_hex(int(acceleration_z * 100), 4)

    # Construct the command string for moving the Z stage
    command_z = f'01109900000912{distance_hex_z}00000001{speed_hex_z[:4]}{speed_hex_z[4:]}{acceleration_hex_z}00000000'
    complete_command_z = f':{command_z}'  # Add colon at the beginning for command formatting

    # Calculate checksum for the command
    checksum_z = calculate_checksum(complete_command_z)

    # Append checksum to the command string
    complete_command_with_checksum_z = f'{complete_command_z}{checksum_z}'

    # Print the constructed command for debugging purposes
    print(f"Constructed command for sending Z: {complete_command_with_checksum_z}")

    # Calculate time to wait for movement completion
    time_to_wait = gamepad.step_size / speed_z

    # Send the command to move the Z stage
    send_cmd(gamepad.com_port, complete_command_with_checksum_z, True)

    # Wait for the movement to complete
    time.sleep(time_to_wait)