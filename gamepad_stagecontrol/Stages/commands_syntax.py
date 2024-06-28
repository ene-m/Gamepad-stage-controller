import pygame 
import serial
import time

# Define the command syntax for the stages, used for building the command strings in the movemets functions

def send_cmd(com_port, string1, display):
    ser = serial.Serial(port=com_port, baudrate=115200, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.1)
    to_send = string1.encode() + b'\r\n'
    ser.write(to_send)
    time.sleep(0.5)  # Delay for response
    response = ser.read(ser.in_waiting or 1).decode('utf-8')
    num = len(response)
    if num == 0:
        print('Timeout was reached.')
    elif display:
        print(f'String sent to Device: "{string1}"')
        print(f'Response from Device (in HEX): "{response.strip()}"')
        print(f'Number of Chars received: {num - 2} (+2 terminator chars)')
    ser.close()
    return response, num

def add_error_code(string):
    if len(string) % 2 == 0:
        print('Error: Input string length must be odd.')
        return -1
    temp = 0x100000000  # Equivalent to hex2dec('ffffffff') + 1
    string = string[1:]  # Remove the first character
    for i in range(0, len(string) - 1, 2):
        temp -= int(string[i:i+2], 16)
    temp_hex = '{:X}'.format(temp)
    complete_string = ':' + string + temp_hex[-2:]
    return complete_string

def format_hex(value, length):
    """Format the given value as a hexadecimal string of the specified length."""
    return f'{value:0{length}X}'

def calculate_checksum(command):
    """Calculate the two's complement checksum for the given command."""
    sum_bytes = sum(int(command[i:i+2], 16) for i in range(1, len(command), 2))  # Start from 1 to skip ':'
    checksum = (0x10000 - sum_bytes) & 0xFFFF
    return format_hex(checksum, 4)[-2:]

def get_sign(num):
    if num > 0:
        return 1
    elif num < 0:
        return -1
    else:
        return 0