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
    return position

def move_X_analog(gamepad, value):
    
    gamepad.distance_x += -1 *value * gamepad.step_size   
    gamepad.distance_x = max(0, gamepad.distance_x)    
    # Calculate the speed in X and Y directions based on the joystick input, to have smooth movement when moving diagonally
    speed_x = gamepad.step_size   
    acceleration_x = gamepad.acceleration   
    distance_hex_x = format_hex(int(gamepad.distance_x * 100), 8)    
    speed_hex_x = format_hex(int(speed_x * 100), 8)   
    acceleration_hex_x = format_hex(int(acceleration_x * 100), 4)   
    command_x = f'03109900000912{distance_hex_x}00000001{speed_hex_x[:4]}{speed_hex_x[4:]}{acceleration_hex_x}00000000'   
    complete_command_x = f':{command_x}'    
    checksum_x = calculate_checksum(complete_command_x)   
    complete_command_with_checksum_x = f'{complete_command_x}{checksum_x}' 

    print(f"Constructed command for sending X: {complete_command_with_checksum_x}")

    send_cmd(gamepad.com_port, complete_command_with_checksum_x, True)

    time.sleep(gamepad.step_size/speed_x)

def move_X_Dpad(gamepad, value):

    gamepad.distance_x += -1* value * gamepad.step_size           
    gamepad.distance_x = max(0, gamepad.distance_x)            
    speed_x = gamepad.step_size
    acceleration_x = gamepad.acceleration            
    distance_hex_x = format_hex(int(gamepad.distance_x * 100), 8)            
    speed_hex_x = format_hex(int(speed_x * 100), 8)            
    acceleration_hex_x = format_hex(int(acceleration_x * 100), 4)           
    command_x = f'03109900000912{distance_hex_x}00000001{speed_hex_x[:4]}{speed_hex_x[4:]}{acceleration_hex_x}00000000'            
    complete_command_x = f':{command_x}'            
    checksum_x = calculate_checksum(complete_command_x)            
    complete_command_with_checksum_x = f'{complete_command_x}{checksum_x}'   
    print(f"Constructed command for sending X: {complete_command_with_checksum_x}")
    time_to_wait += gamepad.step_size/speed_x
    send_cmd(gamepad.com_port, complete_command_with_checksum_x, True)