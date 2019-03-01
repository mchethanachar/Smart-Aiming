# Smart-Aiming
Aiming at the intruder automatically using Image processing. 

The project is divided into 2 modules

1)Image processing
     This is where the intruder is detected and its centroid is computed. The program starts by taking the first frame of the video as the static frame.All the successive frames are subtracted from the static frame. The difference with some threshhold is then considered and the biggest contour in it is considered as the intruder.It's centroid is computed.Assuming the coverage of the camera as 80 degrees the agle of action for the servo motors is calculated. The angles are sent to the Arduino.


2)The Aiming
     The aiming mechanism uses 2 servo motors. One for horizontle and other for the vertical motions. The servo motors are set to the angle that is recieved from from python(through serial).If value recieved is between 0 to 179,the that value is for setting horizantle servo motor.If value recieved is between 180 to 360,the that value is for setting vertical servo motor after subtracting 180 from it. The video gives a better picture of the mechnical structure.
