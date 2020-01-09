import pickle
import socket
import struct
import numpy as np
import cv2

from pythonosc.udp_client import SimpleUDPClient

import cv2.aruco as aruco

HOST = ''
PORT = 8089

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST, PORT))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

cameraMatrix = np.load('cameraMatrix.npz')

data = b'' ### CHANGED
payload_size = struct.calcsize("L") ### CHANGED


ip = "127.0.0.1"
port = 1337
port_id = 8008

client = SimpleUDPClient(ip, port)  # Create client
clientID = SimpleUDPClient(ip, port_id)  # Create client



while True:
    conn, addr = s.accept()
    # Retrieve message size
    while len(data) < payload_size:
        data += conn.recv(4096)


    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

    # Retrieve all data based on message size
    while len(data) < msg_size:
        data += conn.recv(4096)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    # Extract frame
    frame = pickle.loads(frame_data)

    #print(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    gray = frame
       
    gray = cv2.flip(frame,0)

    aruco_dict = aruco.Dictionary_get(aruco.DICT_7X7_50)

   


    parameters =  aruco.DetectorParameters_create()
 
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if ids is not None:
        
        newGray = gray.copy()
        newGray = aruco.drawDetectedMarkers(newGray, corners)

        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(corners, 0.18, cameraMatrix['mtx'], cameraMatrix['dist'], np.float32(cameraMatrix['rvecs']), np.float32(cameraMatrix['tvecs']))
        
        positions = tvecs.tolist()
       
        blah = list()

        for i in range(len(rvecs)):

            rotM = np.zeros(shape=(3,3))
            cv2.Rodrigues(rvecs[i],rotM, jacobian = 0)
            ypr = cv2.RQDecomp3x3(rotM)
            
            ypr = list(ypr[0])
     
            positions[i][0].extend([ypr[0],ypr[1],ypr[2],ids[i].tolist()[0]]) 

            newGray = aruco.drawAxis(newGray, cameraMatrix['mtx'], cameraMatrix['dist'], rvecs[i], tvecs[i], 0.1)
            gray = newGray
            
            print(positions[i])
            blah.append([positions[i]])
            clientID.send_message("/", positions)

    else:
        positions, blah = None,None
        #client.send_message("/", positions)  # Send message with int, float and string 
        clientID.send_message("/", positions)

    gray = aruco.drawDetectedMarkers(gray, corners)

    # Display
    cv2.imshow('frame', gray)
    cv2.waitKey(1)

cv2.destroyAllWindows()