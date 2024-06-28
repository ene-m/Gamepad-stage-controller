# Gamepad_StageControl

This repository is an open-loop gamepad controller used to control four motorized stages via Modbus ASCII with a gamepad. The repository consists of a main file, which contains the main loop for controlling the stages, and a `Stages` folder that includes all the Python files necessary to process commands from the controller.

## Main.py

The main file (`main.py`) serves as the entry point for controlling motorized stages via a gamepad using Python and Pygame. It initializes the gamepad, polls for input from its buttons and axes, and executes corresponding functions to control the stages via Modbus ASCII communication.

### Functions

- **Initialize Gamepad (`initialize_gamepad()`)**:
  - Initializes Pygame and the connected gamepad.
  - Checks if a gamepad is connected; if not, prints a message and returns `None`.
  - Returns the initialized joystick object for further use.

- **Poll Gamepad (`poll_gamepad(joystick, com_port)`)**:
  - Initializes a `GamePadState` object to manage gamepad states and stage controls.
  - Defines a deadzone (`DeadZone`) to filter out minor joystick movements.
  - Continuously polls the gamepad for button presses and joystick movements until the `gamepad.running` flag is set to `False`.
  - Iterates through defined axes (`gamepad.Axis`), calling associated functions based on joystick axis movements.
  - Processes button presses (`gamepad.buttons`), executing corresponding functions defined in `GamePadState`.
  - Handles directional pad (D-pad) inputs (`gamepad.D_Pad`), triggering functions based on hat (D-pad) movements.
  - Uses `pygame.event.pump()` to update the event queue and `pygame.time.Clock()` to control the loop's execution rate.

- **Main Function (`main()`)**:
  - Entry point of the script.
  - Calls `initialize_gamepad()` to obtain the gamepad joystick object.
  - If a gamepad is connected (`joystick` is not `None`), calls `poll_gamepad(joystick, com_port)` to start processing gamepad inputs and controlling the stages via `com_port`.
  - Quits Pygame (`pygame.quit()`) after exiting the main loop.

## Stages Folder

This folder contains all the functions and settings for the stages and the gamepad. It is subdivided into:
- **Command_syntax**: Contains function syntax to build the commands to send to the stages.
- **Commands**: Contains functions not inherent to the movement of the stages, which are performed by commands on the gamepad (e.g., Change_profile, Change_step_size, Stop, Get_all_positions).
- **GamePadState**: Defines a class that holds all the information and states of the gamepad and the stages.
- **Stage-specific files**: Four files, one for each stage, where all the specific functions for the stages are defined (movement, homing, get_position).

### Command_syntax.py

The `commands_syntax` module provides essential functions for constructing and formatting command strings used to control motorized stages via Modbus ASCII.

#### Functions

- **Send Command (`send_cmd(com_port, string1, display)`)**:
  - Establishes a serial connection (`com_port`) with specified settings (baudrate, parity, etc.).
  - Sends the provided command string (`string1`) to the connected device, appending carriage return and newline characters.
  - Waits for a response from the device with a timeout of 0.1 seconds.
  - Displays the sent command and received response (in hexadecimal) if `display` is `True`.
  - Closes the serial connection after communication.
  - Returns the response string and the number of characters received.

- **Add Error Code (`add_error_code(string)`)**:
  - Calculates and appends a two-byte checksum to the provided command string (`string`).
  - Ensures the length of the input string is odd before processing.
  - Returns the complete command string with the appended checksum.

- **Format Hexadecimal (`format_hex(value, length)`)**:
  - Converts a given `value` into a hexadecimal string of specified `length`.
  - Prepends zeros as needed to achieve the desired length.

- **Calculate Checksum (`calculate_checksum(command)`)**:
  - Computes the two's complement checksum for the given command string (`command`).
  - Sums the hexadecimal byte values and calculates the checksum to ensure data integrity.
  - Returns the calculated checksum as a two-byte hexadecimal string.

### Commands.py

The `commands` module includes functions that manage various gamepad actions, facilitating interaction with the motorized stages controlled via Modbus ASCII.

#### Functionality

- **Change Profile (`change_profile(gamepad)`)**:
  - Switches between 'Analog_sticks' and 'D_Pad' profiles.
  - Adjusts axis and D-Pad mappings accordingly:
    - In 'D_Pad' mode, axes X and Y are disabled (set to 100), and step sizes are adjusted for finer control.
    - In 'Analog_sticks' mode, all axes are enabled, and default step sizes are restored.
  - Prints confirmation of profile change to the console.

- **Change Step Size (`change_step_size(gamepad)`)**:
  - Allows the user to input a new step size for stage movements.
  - Updates `gamepad.step_size` and `gamepad.step_size_phi` with the user-defined value.
  - Prints confirmation of the new step size to the console.

- **Stop Program (`stop(gamepad)`)**:
  - Halts the execution of stage movements by setting `gamepad.running` to `False`.
  - Signals the program to exit gracefully.
  - Prints an exit message to the console.

- **Get Positions (`get_position(gamepad)`)**:
  - Retrieves and prints the current positions of all stages (X, Y, Z, and phi).
  - Utilizes functions `get_position_x`, `get_position_y`, `get_position_z`, and `get_position_phi` to obtain and display each stage's position.
  - Outputs each position in millimeters to the console.

### GamePadState.py

#### Overview

The `GamePadState` class manages the state and functionality of a gamepad used to control motorized stages. It encapsulates various attributes and methods essential for interacting with the gamepad and coordinating stage movements.

#### Attributes

Upon initialization, the `GamePadState` object sets default values for its attributes:
- `all_profiles`: A dictionary defining different control profiles ('Analog_sticks' and 'D_Pad').
- `profile`: Initialized to 'Analog_sticks', determines the current control mode.
- `distance_x`, `distance_y`, `distance_z`, `distance_phi`: Variables storing the distances moved along each axis, initialized to 0.
- `step_size`: Sets the default step size for incremental movements to 0.3.
- `acceleration`: Defines the acceleration factor for stage movements, set to 0.5.
- `running`: Boolean flag indicating the operational status of the gamepad, initialized as True.
- `com_port`: Communication port identifier, set to 'COM3'.
- `buttons`: A dictionary mapping button names to their respective identifiers and associated functions.
- `Axis`: A dictionary defining axis names and numerical identifiers for stages.
- `D_Pad`: A dictionary mapping D-Pad actions to identifiers for stage control.

#### Function Mapping

##### Button Functions
- `button_functions`: Maps button names to their associated functions for execution.
  - `home_x`, `home_y`, `home_z`, `home_phi`: Initiate homing procedures for respective stages.
  - `change_profile`: Switches between control profiles ('Analog_sticks' and 'D_Pad').
  - `exit`: Stops stage movement and terminates the program.
  - `change_step_size`: Adjusts the step size used for stage movements.
  - `get_position`: Retrieves and displays current stage positions.

##### Axis Functions
- `axis_functions`: Associates axis names with methods for continuous analog control.
  - `move_X_analog`, `move_Y_analog`: Control movements along X and Y axes.
  - `move_z`, `move_phi`: Manage movements along Z-axis and rotation (phi) respectively.

##### D-Pad Functions
- `D_pad_functions`: Maps D-Pad actions to their corresponding movement functions.
  - `move_phi`: Controls rotation based on D-Pad inputs.
  - `move_XY_Dpad`: Coordinates movements in the XY plane using D-Pad inputs.

### Stage-specific.py

The `x_stage`, `y_stage`, `z_stage`, and `phi_stage` modules each define functions for their respective motorized stages. These modules utilize commands and syntax from `commands_syntax` to control the stages via Modbus ASCII communication.

#### Functionality

Each stage module provides the following functions:

- **Homing Function (`home_<stage>`)**:
  - Initiates the homing process for the respective stage.
  - Turns on Modbus and SERVO as necessary.
  - Executes specific homing commands until completion is confirmed.

- **Get Position Function (`get_position_<stage>`)**:
  - Retrieves the current position of the respective stage.
  - Converts the position from the Modbus response (1:100 mm format) to millimeters.
  - Prints the current position to the console.

- **Analog Movement Function (`move_<stage>_analog`)**:
  - Moves the respective stage based on analog input values.
  - Calculates movement parameters such as distance, speed, and acceleration.
  - Constructs and sends formatted commands to the stage using Modbus ASCII.
  - Ensures smooth movement based on the specified step size and joystick input.

- **D-Pad Movement Function (`move_<stage>_Dpad`)**:
  - Controls movement of the respective stage using D-Pad inputs.
  - Adjusts distance and direction based on D-Pad values.
  - Constructs and sends formatted commands to the stage.
  - Manages movement timing to ensure proper stage control and synchronization.
