import cv2
import numpy as np

cap = cv2.VideoCapture(0)

background = cv2.imread('./img1.jpg')

if background is None:
    print("Error: 'img1.jpg' not found or cannot be read.")
    exit()
    
while cap.isOpened():
    ret, current_frame = cap.read()

    if ret: 

        hsv_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)

        #range for lower red
        l_red =  np.array([0,0,0])
        u_red = np.array([179,255,50])
        mask1 = cv2.inRange(hsv_frame,l_red,u_red)

        # range for upper red
        # l_red =  np.array([170,120,70])
        # u_red = np.array([180,255,255])
        # mask2 = cv2.inRange(hsv_frame,l_red,u_red)

        red_mask = mask1
        

        red_mask = cv2.morphologyEx(red_mask,cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations=10)
        red_mask = cv2.morphologyEx(red_mask,cv2.MORPH_DILATE,np.ones((3,3),np.uint8), iterations=1)

        red_mask = cv2.resize(red_mask, (background.shape[1], background.shape[0]))

        # Convert background to the same data type (CV_8U) as red_mask
        background = background.astype(np.uint8)

        part1 = cv2.bitwise_and(background,background,mask = red_mask)

        red_free = cv2.bitwise_not(red_mask)

        part2 = cv2.bitwise_and(current_frame,current_frame,mask = red_free)
        
        cv2.imshow("cloak", part1+part2)
        if cv2.waitKey(5) ==ord('q'):
            break
cap.release()
cv2.destroyAllWindows