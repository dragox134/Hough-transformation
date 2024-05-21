from ximea import xiapi
import cv2
import numpy as np
### runn this command first echo 0|sudo tee /sys/module/usbcore/parameters/usbfs_memory_mb  ###
 
#create instance for first connected camera
cam = xiapi.Camera()
 
 
 
#start communication
#to open specific device, use:
#cam.open_device_by_SN('41305651')
#(open by serial number)
print('Opening first camera...')
cam.open_device()
 
#settings
cam.set_exposure(10000)
cam.set_param('imgdataformat','XI_RGB32')
cam.set_param('auto_wb', 1)
print('Exposure was set to %i us' %cam.get_exposure())
 
#create instance of Image to store image data and metadata
img = xiapi.Image()
 
#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()
 
 
while cv2.waitKey(1) != ord('q'):
    cam.get_image(img)
    image = img.get_image_data_numpy()
    image = cv2.resize(image,(1024,1024))

    #editing image for detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.blur(gray, (3, 3)) 

    # Apply Hough transform on the blurred image. 
    detected_circles = cv2.HoughCircles(gray_blurred,  
                    cv2.HOUGH_GRADIENT, 1, 60, param1 = 80, 
                param2 = 50, minRadius = 1, maxRadius = 80)
    

    # Draw circles that are detected. 
    if detected_circles is not None: 
    
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
    
        for pt in detected_circles[0, :]: 
            a, b, r = pt[0], pt[1], pt[2] 
    
            # Draw the circumference of the circle. 
            cv2.circle(image, (a, b), r, (0, 255, 0), 2) 
    
            # Draw a small circle (of radius 1) to show the center. 
            cv2.circle(image, (a, b), 1, (0, 0, 255), 3) 
    cv2.imshow("Detected Circle", image) 



 
 

 
 
#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()
 
#stop communication
cam.close_device()
cv2.destroyAllWindows()
print('Done.')