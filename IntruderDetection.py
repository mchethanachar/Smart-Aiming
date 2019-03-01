'''
Written by:Chethan M
           BMS College of Engineering
           Bangalore
           mchethan.achar@gmail.com
Programming languge: Python 3.6.8
Last modified:20th Nov 2018
'''
#import the necessary packages
import argparse
import imutils
import cv2, time, pandas
from datetime import datetime
import serial
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders

#Replace with proper Email address
toaddr = "toEmailAddress"
fromaddr = "fromEmailAddress"

flag2=0
#To send the picture of the intruder
def mail():
    msg = MIMEMultipart()  
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Intruder detected"
    body = "Find attachment to know the intruder"
    msg.attach(MIMEText(body, 'plain'))
    filename ="C:\\Users\\india\\upload.jpg"
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p) 
    p.add_header('Content-Disposition',"attachment;filename= {}".format(filename))
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "FromEmailPassword")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit() 


#sending the coordinates(centroid of intruder) to the Arduino
#check the com port number of your arduino before copying
ser = serial.Serial('COM3', 9600)
def sendData(data):
	encoded = bytes(str(data), 'utf-8')
	ser.write(encoded)

static_back = None
 
# List when any moving object appear
motion_list = [ None, None ]

"""def captureBackground(gray):
    static_back = gray
    return static_back"""
    
# Time of movement
time2 = []

stor = 90
stor2=90
 
# Initializing DataFrame, one column is start 
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])
 
# Capturing video
video = cv2.VideoCapture(0)


# construct the argument parse and parse the arguments
while True:
    check, frame = video.read()
    cv2.imwrite("upload.jpg",frame)
    # Initializing motion = 0(no motion)
    motion = 0
    flag=0
 
    # Converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if static_back is None:
        static_back=gray
    diff_frame = cv2.absdiff(static_back, gray)
    thresh_frame = cv2.threshold(diff_frame, 80, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    cv2.imwrite("abc.jpg",thresh_frame)
    
    image = cv2.imread("abc.jpg")
    image=cv2.flip(image,1)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 30, 255, cv2.THRESH_BINARY)[1]


    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	    cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    l=len(cnts)
    max=0
    i=0;
    while i < l:
        area = cv2.contourArea(cnts[i])
        if max<area:
            max=area
            ind=i
        i=i+1
    if l>0:
        
        M = cv2.moments(cnts[ind])
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.drawContours(image, [cnts[ind]], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 7, (0, 0, 255), -1)
        cv2.putText(image, "center", (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        degX=int(0.140625*cX)
        degY=int(0.12631*cY)
        degY=degY+60
        degX=degX+45
        dif = stor-degX
        dif2=stor2-degY
        key=0

        if dif<-3 or dif>3:
                stor = degX
                sendData(str(degX))
                time.sleep(1.5)
                flag=1

        if dif2<-3 or dif2>3:
                stor2= degY
                degY=degY+180+5
                if(degY>360):
                        degY=360
                sendData(str(degY))
                #This delay is to prevent arduino buffer overflow
                time.sleep(1.5)
                flag=1

        print(cY)
    if flag==1:
        mail()
            
    flag2=flag2+1    
    cv2.imshow("Image", image)

    
    key = cv2.waitKey(1)
    if key == ord('b'):
        static_back=None;
    if key == ord('q'):
        if motion == 1:
            time.append(datetime.now())
        break
    
