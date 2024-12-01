from naoqi import ALProxy
import numpy as np
import socket
import struct
from PIL import Image
import paramiko
import time

# Local path for saving images
local_path = r"C:\Python27\venv\NAO\naoCognitive\Nao"

def save_image(robot_ip, local_path, path):
    # nao_path = path[0]
    # print("Connecting to NAO robot at IP {} to retrieve image.".format(robot_ip))
    
    ssh_client = paramiko.SSHClient()
    ssh_client.tset_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=robot_ip, port=22, username='nao', password='nao')
    ftp_client = ssh_client.open_sftp()
    ftp_client.get(nao_path, local_path)
    ftp_client.close()
    ssh_client.close()
    print("Image saved locally at {}.".format(local_path))

# # NAO robot connection details
# robot_ip = "1.1.1.21"  # Replace with your NAO robot's IP address
# robot_port = 9559ip

# # Create proxies
# camera_proxy = ALProxy("ALPhotoCapture", robot_ip, robot_port)
# motion_proxy = ALProxy("ALMotion", robot_ip, robot_port)

# Set up socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('1.1.1.244', 65432))
server_socket.listen(1)
print("Waiting for connection...")

conn, client_address = server_socket.accept()
print("Connection from {} established.".format(client_address))

try:
    while True:
        # Capture the image
        folder_path = '/home/nao/'
        folder_name = 'captured_image'
        overwrite = True
        # nao_path = camera_proxy.takePicture(folder_path, folder_name, overwrite)
        
        # print("Image captured at {}".format(nao_path))
        
        # # Save the image locally
        # save_image(robot_ip, local_path, nao_path)
        
        flag = 1
        conn.sendall(struct.pack("!i", flag))  # Send flag as integer
        print("Flag sent to client.")

        # Receive predicted angles
        data = conn.recv(8)
        head_yaw, head_pitch = struct.unpack("!ff", data)
        print("Received angles: HeadYaw={}, HeadPitch={}".format(head_yaw, head_pitch))

        # # Set the robot's head angles
        # motion_proxy.setAngles(["HeadYaw", "HeadPitch"], [head_yaw, head_pitch], 0.1)
        # time.sleep(3)
        print("Head angles set on robot.")

finally:
    conn.close()
    server_socket.close()
    print("Server closed.")