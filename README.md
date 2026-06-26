# 🤖 ROS 2 & ESP32 Smart Obstacle Avoider

A real-time robotics perception and control system. This project establishes bidirectional communication between physical hardware (ESP32) and the ROS 2 ecosystem, creating a complete "Sense, Think, and Act" loop for autonomous obstacle avoidance.

## 👨‍💻 Author
**Jimmy Hadad**

## 🎯 Project Objective
To design and implement a zero-latency obstacle avoidance system controlling a single DC motor. By utilizing a customized serial bridge, the system translates physical distance measurements into ROS 2 topics, analyzes them in real-time to make movement decisions, and instantly sends hardware control commands back to the ESP32 based on a strict 15 cm safety threshold.

## ⚙️ Hardware & Software Stack
* **Microcontroller:** ESP32 Development Board
* **Sensor:** HC-SR04 Ultrasonic Sensor
* **Actuator:** Single DC Motor driven by an L298N Motor Driver
* **Operating System:** Ubuntu Linux
* **Framework:** ROS 2 (Humble)
* **Languages:** Python (ROS Nodes) & C++ (ESP32 Firmware)

## 🚀 Key Features
* **Zero-Latency Serial Bridge:** A highly optimized ROS 2 node that continuously clears the serial buffer to ensure only the most recent sensor data is published to `/sonar_distance`, while simultaneously listening for and routing motor commands to the ESP32.
* **Intelligent Brain (Subscriber/Publisher):** A processing node that evaluates distance data in real-time. It broadcasts an 'F' (Forward) command and prints "Safe Zone" if the path is clear, or instantly triggers an 'S' (Stop) command and a "WARNING!" message if an obstacle is <= 15 cm away.
* **Synchronized Physical Response:** Custom `pulseIn` timeouts on the ESP32 ensure the hardware never hangs, allowing the motor to react to obstacles in a fraction of a second.

## 🎬 Live Demonstration

**1. Practical Hardware Demonstration:**
Watch the physical system in action as the ultrasonic sensor detects obstacles and immediately halts the DC motor in real-time.


https://github.com/user-attachments/assets/f73e7139-7911-4b58-b6d5-89e3365205cd



**2. Software & ROS 2 Terminals:**
A screen recording showcasing the real-time data flow, node execution, and decision-making process within the ROS 2 environment.

[Screencast from 06-26-2026 09:22:45 PM.webm](https://github.com/user-attachments/assets/254fc9d5-86fb-4909-a369-74abde043318)



## 💻 ESP32 C++ Firmware Logic
The ESP32 acts as the physical interface, programmed via the Arduino IDE. Its execution loop performs two primary tasks simultaneously:
1. **Sensing:** Triggers the HC-SR04, calculates the physical distance in centimeters with a strict timeout, and streams the numerical data over the Serial port (baud rate 115200).
2. **Acting:** Listens to the Serial port for incoming character commands from the ROS 2 Brain node ('F' or 'S') and immediately toggles the L298N driver pins (IN1, IN2) to move or halt the motor.

## 📂 Repository Structure
* `my_first_package/` : The main ROS 2 Python package directory containing the source code.
* `my_first_node.py` : The Bridge node handling bidirectional serial communication.
* `my_sub_node.py` : The Brain node containing the decision-making logic.
* `setup.py` : Configuration file with correctly mapped entry points for the executables.
* `esp32_firmware/esp32_firmware.ino` : The C++ firmware for the ESP32 microcontroller.

## ⚠️ Setup & Deployment

**1. Hardware Setup (C++):**
Connect the HC-SR04 and L298N to the ESP32. Upload the C++ firmware using the Arduino IDE. Close the Arduino Serial Monitor completely.

**2. Serial Permissions:**
Plug the ESP32 into your Ubuntu machine and grant read/write access to the serial port:
```bash
sudo chmod a+rw /dev/ttyACM0
```

**3. Build the Workspace:**
Navigate to your `ros2_ws` and compile the package to register the executables:
```bash
cd ~/ros2_ws
colcon build --packages-select my_first_package
source install/setup.bash
```

**4. Run the System:**
Open two separate terminals and run the following commands:

* **Terminal 1 (The Bridge):**
  ```bash
  cd ~/ros2_ws
  source install/setup.bash
  ros2 run my_first_package my_first_node
  ```

* **Terminal 2 (The Brain):**
  ```bash
  cd ~/ros2_ws
  source install/setup.bash
  ros2 run my_first_package my_sub_node
  ```
