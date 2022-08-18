# cameracontrol.py
Visca Over IP control of PTZ camera using pygame and IP detection


#IP Detection
Utilizes the ARP command to search for the IPs of cameras based on their MAC address.

#Package Installation
Will check for the required packages and install them if needed.

#Joystick and Keyboard Control
Control the PTZ of cameras utilizing either keyboard or game controller. Joystick.py has been included to check which buttons and axis are mapped on the controller. Tested with Xbox 360 controller

#Needed Optimizations
-Delay between joystick and camera movement/zoom
-Program runs for a bit even if no actions have been done

#Possible features
-RSTP stream of camera in window.
