import cv2
import numpy as np

import pigpio
import time


pi = pigpio.pi()
pi.set_mode(17, pigpio.OUTPUT)

pi.set_mode(27, pigpio.OUTPUT)


#90° pour commencer
value_x = 1500
value_y = 1500

print("set to: ",pi.get_servo_pulsewidth(17))
pi.set_servo_pulsewidth(17, value_x)


print("set to: ",pi.get_servo_pulsewidth(27))
pi.set_servo_pulsewidth(27, value_y)


cap = cv2.VideoCapture(0)

# Set camera resolution
cap.set(3, 480)
cap.set(4, 320)

_, frame = cap.read()
frame = cv2.flip(frame, -1 ) ##pour voir a l'envers
rows, cols, _ = frame.shape


x_medium = int (cols / 2)

y_medium = int (rows / 2)


center_x = 240

center_y = 160


K_x = 0.2 #Constante de mouvement par pixel à régler
K_y = 0.3


while True:
    
    _, frame = cap.read()
    frame = cv2.flip(frame, -1 ) ##pour voir a l'envers
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    
    # red color
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)
    
    

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium = int((x + x + w) / 2)
        
        cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
        
        
        y_medium = int((y + y + h) / 2)
        
        cv2.line(frame,(0, y_medium), (480, y_medium), (0, 255, 0), 2)
        
        break
        
    
    cv2.imshow("Frame", frame)
    #cv2.imshow("", red_mask)
    
    
    key = cv2.waitKey(1)
    
    if(key == 27):
        break
    
    
    print(x_medium)
    
    
    if x_medium < center_x -30:
            
            value_x2=value_x+(K_x*abs(x_medium - center_x -10))
            
            if(value_x2<2495):
                value_x=value_x2
               
    if x_medium > center_x +30:
            
            value_x2=value_x-(K_x*abs(x_medium - center_x -10))
            
            if(value_x2>505):
                value_x=value_x2
                
    else:
        value_x=value_x

    
    pi.set_servo_pulsewidth(17, value_x)
    
    


    if y_medium < center_y -30:
            
            value_y2=value_y-(K_y*abs(y_medium - center_y -10))
            
            if(value_y2<2495):
                value_y=value_y2  
           
    if y_medium > center_y +30:
            
            value_y2=value_y+(K_y*abs(y_medium - center_y -10))
            
            if(value_y2>505):
                value_y=value_y2
                
    else:
        value_y=value_y
     
    print(value_y)
    pi.set_servo_pulsewidth(27, value_y)
    

cap.release()
cv2.destroyAllWindows()
