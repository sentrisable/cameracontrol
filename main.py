
# Module Check and Install
import sys, subprocess, pkg_resources

required = {'visca_over_ip', 'pygame'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed
if missing:
    install_check = input("This program requires additional packages to be installed to run. Install additional packages? [y/n] \n{}".format(missing))
    if install_check == 'y':
            python = sys.executable
            subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)
    if install_check =='n':
        quit()
    else:
        install_check
# Imports
import pygame, json
from visca_over_ip import Camera


#Default Inits and setups
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((800,800))
pygame.display.set_caption("LH Camera Controller")

#Find Camera IPs
def FindCamIp(mac):
    if sys.platform == "win32":
        cmd = 'arp -a | findstr "{}" '.format(mac)
    elif sys.platform == "darwin":
        cmd = 'arp -a | grep "{}" '.format(mac)
    returned_output = subprocess.check_output((cmd), shell=True, stderr=subprocess.STDOUT)
    parse = str(returned_output).split(' ', 1)
    ip = parse[1].split(' ')
    print(ip[1])
    return(ip[1])
        
cam_one = #"INSERT CAM IP"
cam_two = #"INSERT CAM IP"

font = pygame.font.SysFont("Arial", 20)
#cam_one = FindCamIp("Insert Cam One MAC Address")
#cam_two = FindCamIp("Insert Cam Two MAC address")

#Joystick Inits
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
print(joysticks)

#Text Defaults
camera_controls_one = "Press ESC or B to return to camera selection."
camera_controls_two = "Press W or X to tilt up or down"
camera_controls_three = "Press A or D to pan left or right"
camera_controls_four = "Press R or F to zoom in or out"
camera_controls_five = "Press Q, E, Z, or C for diagonal movement"
camera_controls_six = "Press Shift + S or Start to reset camera to default position"
camera_controls_seven = "Left Joystick controls camera motion"
camera_controls_eight = "Left Trigger zooms out, Right Trigger Zooms in"
camera_controls_nine = "Select to change Focus Mode (Auto/Manual)"
camera_controls_ten = "DPad Left/Right to focus | Dpad Up/Down to change exposure"

#Camera movement defaults
pan_movement = 0
tilt_movement = 0
zoom_movement = 0
motion = [0,0]

#Color and pygame variables
update = pygame.display.update()
white = (255,255,255)
black = (0,0,0)

def ClearScreen():
    display.fill(black)

def DisplayText(camera_name):
    ClearScreen()
    display.blit(font.render(camera_name +" Selected. "+ camera_controls_one, True, white,black), (100,50))
    display.blit(font.render(camera_controls_two, True, white,black), (100,100))
    display.blit(font.render(camera_controls_three, True, white,black), (100,150))
    display.blit(font.render(camera_controls_four, True, white,black), (100,200))
    display.blit(font.render(camera_controls_five, True, white,black), (100,250))
    display.blit(font.render(camera_controls_six, True, white,black), (100,300))
    display.blit(font.render(camera_controls_seven, True, white,black), (100,350))
    display.blit(font.render(camera_controls_eight, True, white,black), (100,400))
    display.blit(font.render(camera_controls_nine, True, white,black), (100,450))
    display.blit(font.render(camera_controls_ten, True, white,black), (100,500))
    pygame.display.update()

def CameraControl(camera, camera_name):
    control = 1
    js = pygame.joystick.Joystick(0)

    while control:
        pygame.display.set_caption("Lighthouse Camera Controller: {}".format(camera_name))
        display.blit(font.render("Focus mode: {}".format(camera.get_focus_mode()), True, white,black), (100, 600))
        for event in pygame.event.get():

            if event.type == pygame.KEYUP or pygame.JOYAXISMOTION == 0:
                camera.pantilt(pan_speed=0, tilt_speed=0)
                camera.zoom(speed=zoom_movement)

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button==6:
                    if camera.get_focus_mode() == "auto":
                        camera.set_focus_mode("manual")
                    else:
                        camera.set_focus_mode("auto")                        
                if event.button==7:
                    camera.pantilt_home()
                if event.button == 0:
                    camera.close_connection()
                    control = 0
                    pygame.display.set_caption("Lighthouse Camera Controller")
                    break
                if event.button == 1:
                    js.rumble(0, 1, 3000)

            if event.type == pygame.JOYAXISMOTION:
                if event.axis <2:
                    motion[event.axis] = int(event.value)
                    camera.pantilt(pan_speed=motion[0]*-15, tilt_speed=motion[1]*-15)
                if event.axis == 5:
                    camera.zoom(speed=int((event.value+1)*3.5))
                if event.axis == 4:
                    camera.zoom(speed=int((event.value+1)*-3.5))
            
            if event.type == pygame.JOYHATMOTION:
                if js.get_hat(0) == (-1,0):
                    camera.manual_focus(speed=-5)
                if js.get_hat(0) == (1,0):
                    camera.manual_focus(speed=5)
                if js.get_hat(0) == (0,1):
                    camera.increase_exposure_compensation()
                if js.get_hat(0) == (0,-1):
                    camera.decrease_exposure_compensation()

            
            if event.type == pygame.KEYDOWN:
                if (event.key== pygame.K_UP and event.key==pygame.K_LEFT) or event.key==pygame.K_q:
                    camera.pantilt(pan_speed=15, tilt_speed=15)
                if (event.key== pygame.K_UP and event.key==pygame.K_RIGHT) or event.key==pygame.K_e:
                    camera.pantilt(pan_speed=-15, tilt_speed=15)
                if (event.key== pygame.K_DOWN and event.key==pygame.K_LEFT) or event.key==pygame.K_z:
                    camera.pantilt(pan_speed=15, tilt_speed=-15)
                if (event.key== pygame.K_DOWN and event.key==pygame.K_RIGHT) or event.key==pygame.K_c:
                    camera.pantilt(pan_speed=-15, tilt_speed=-15)
                if event.key == pygame.K_LEFT or event.key==pygame.K_a:
                    camera.pantilt(pan_speed=15, tilt_speed=0)
                if event.key == pygame.K_RIGHT or event.key==pygame.K_d:
                    camera.pantilt(pan_speed=-15, tilt_speed=0)
                if event.key == pygame.K_UP or event.key==pygame.K_w:
                    camera.pantilt(pan_speed=0, tilt_speed=15)
                if event.key== pygame.K_DOWN or event.key==pygame.K_x:
                    camera.pantilt(pan_speed=0, tilt_speed=-15)
                if event.key == pygame.K_f:
                    camera.zoom(speed=-5)
                if event.key == pygame.K_r:
                    camera.zoom(speed=5)
                if event.key == pygame.K_s and event.mod & pygame.KMOD_SHIFT:
                    camera.pantilt_home()
                if event.key == pygame.K_ESCAPE:
                    camera.close_connection()
                    ClearScreen()
                    pygame.display.set_caption("Lighthouse Camera Controller")
                    control = 0
                    break
                
        pygame.display.update()

def main():
    running = 1
    while running:

        display.blit(font.render("1 or Left Bumper for Camera One | 2 or Right Bumper for Camera Two, or ESC to quit",True,white,black),(100,100))
        display.blit(font.render("Camera one IP: {}| Camera two IP: {}".format(cam_one, cam_two), True, white,black), (100,300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = 0
                if event.key == pygame.K_1:
                    DisplayText("Camera One")
                    CameraControl(Camera(cam_one), "Camera One")
                if event.key == pygame.K_2:
                    DisplayText("Camera Two")
                    CameraControl(Camera(cam_two), "Camera Two")

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    running = 0
                if event.button == 4:
                    DisplayText("Camera One")
                    CameraControl(Camera(cam_one), "Camera One")
                if event.button == 5:
                    DisplayText("Camera Two")
                    CameraControl(Camera(cam_two), "Camera Two")
        
        
        clock.tick(120)  
        pygame.display.update()

if __name__ == "__main__":
    main()
