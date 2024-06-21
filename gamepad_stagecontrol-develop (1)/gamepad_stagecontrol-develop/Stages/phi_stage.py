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
    return position

def move_phi(gamepad, value):

    print('Phi stage not operational.')

    return 

    gamepad.distance_phi += get_sign(value) * gamepad.step_size
    if gamepad.distance_phi < 0:
        gamepad.distance_phi = 360 + gamepad.distance_phi
    elif gamepad.distance_phi >= 360:
        gamepad.distance_phi = gamepad.distance_phi - 360

        

    speed_phi = gamepad.step_size
    acceleration_phi = gamepad.acceleration

    distance_hex_phi = format_hex(int(gamepad.distance_phi * 100), 8)
    speed_hex_phi = format_hex(int(speed_phi * 100), 8)
    acceleration_hex_phi = format_hex(int(acceleration_phi * 100), 4)

    command_phi = f'04109900000912{distance_hex_phi}00000001{speed_hex_phi[:4]}{speed_hex_phi[4:]}{acceleration_hex_phi}00000000'

    complete_command_phi = f':{command_phi}'
    checksum_phi = calculate_checksum(complete_command_phi)
    complete_command_with_checksum_phi = f'{complete_command_phi}{checksum_phi}'

    print(f"Constructed command for sending Phi: {complete_command_with_checksum_phi}")
    print(f"Virtual Phi position: {gamepad.distance_phi} degrees")

    # Send the constructed command to the device
    send_cmd(gameoad.com_port, complete_command_with_checksum_phi, True)