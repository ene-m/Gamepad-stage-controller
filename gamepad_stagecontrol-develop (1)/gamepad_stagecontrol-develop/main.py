import pygame
import time
from Stages.GamePadState import GamePadState


def initialize_gamepad():
#Initialize the gamepad, control if conncected, and return the joystick object
    pygame.init()
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("No gamepad connected")
        return None
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Gamepad connected: {joystick.get_name()}")
    return joystick

def poll_gamepad(joystick, com_port):
    # Updated button mappings to include phi controls
  
    gamepad = GamePadState()
    DeadZone = 0.12              # Deadzone for the joystick

#Cycle through the gamepad buttons and axis to check for input, stops when button exit is pressed   
    while gamepad.running:
        pygame.event.pump()
        # Set up the clock
        clock = pygame.time.Clock()

        for axis in gamepad.Axis:
            if gamepad.Axis[axis] != 100: # 100 is the default value for axis that are not used.
                if abs(joystick.get_axis(gamepad.Axis[axis])) >= DeadZone:
                    gamepad.axis_functions[axis](gamepad, value=joystick.get_axis(gamepad.Axis[axis]))   # Call the function associated with the axis

        for button in gamepad.buttons:
            if joystick.get_button(gamepad.buttons[button]) == 1:    # Check if buttons are pressed
                gamepad.button_functions[button](gamepad)
                time.sleep(0.3) # Sleep to prevent multiple inputs from a single button press

        for hat in gamepad.D_Pad:
            if gamepad.D_Pad[hat] != 100:   # 100 is the default value for hat that are not used.
                if joystick.get_hat(gamepad.D_Pad[hat])[0] != 0 or joystick.get_hat(gamepad.D_Pad[hat])[1] != 0:  # Check if the D-pad is pressed, the hat returns a tuple with the x and y values
                    gamepad.D_pad_functions[hat](com_port, value=joystick.get_hat(gamepad.D_Pad[hat]))


      
            

def main():
    com_port = 'COM3'                 
    joystick = initialize_gamepad()
    if joystick is not None:
        poll_gamepad(joystick, com_port)
    pygame.quit()

if __name__ == "__main__":
    main()
