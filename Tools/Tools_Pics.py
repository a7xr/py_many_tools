import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
# this should deal with Image, Pics, ...
# Planning to use OpenCV with this file

pic_face_jpg = 'E:\\DEV\\python\\py_many_tools\\Tools\\image.jpg'
pic_face_png = 'E:\\DEV\\python\\py_many_tools\\Tools\\image002.png'

face_cascade = cv2.CascadeClassifier('C:\\Python364_rc1\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('C:\\Python364_rc1\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml')

smile_cascade = cv2.CascadeClassifier('C:\\Python364_rc1\\Lib\\site-packages\\cv2\\data\\haarcascade_smile.xml')


class Tools_Pics:

    @staticmethod
    def play_video_from_file():
        cap = cv2.VideoCapture('Tools\\Web.avi')
        print(cap)
        while(cap.isOpened()):
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        pass

    @staticmethod
    def face_detect_from_pic():
        # face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        face_cascade = cv2.CascadeClassifier('C:\\Python364_rc1\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('C:\\Python364_rc1\\Lib\\site-packages\\cv2\\data\\haarcascade_eye.xml')

        
        img = cv2.imread(pic_face_png)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            # print ('x: ', x, ' y: ', y, ' w: ', w, ' h: ', h)
            # # x:  64  y:  179  w:  234  h:  234
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        cv2.imshow('img',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        pass

    @staticmethod
    def face_detect_from_webcam():
        # import cv2

        cap = cv2.VideoCapture(0)
        # cap = cv2.VideoCapture('Tools\\Web.avi')

        
        # print('cap: ', cap)
        # # cap:  <VideoCapture 0000025FFADCBBD0>
        cap.set(3, 640) # WIDTH
        cap.set(4, 480) # HEIGHT

        ret, frame = cap.read()
        # print ('ret: ', ret)
        # print ('frame: ', frame)
        # sys.exit(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # print ('ret: ', ret)
            # # ret:  False
            # print ('frame: ', frame)    
            # # frame:  None

            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            print(len(faces))
            # Display the resulting frame
            for (x,y,w,h) in faces:
                print ('x: ', x, ' y: ', y, ' w: ', w, ' h: ', h)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        pass

    @staticmethod
    def face_detect002():   # doesn_t work
        cascPath = sys.argv[1]
        faceCascade = cv2.CascadeClassifier(cascPath)

        video_capture = cv2.VideoCapture(0)

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.cv2.CV_HAAR_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
        pass

    @staticmethod
    def camshift001():

        # cap = cv2.VideoCapture('slow.flv')
        # take first frame of the video
        cap = cv2.VideoCapture(0)

        ret,frame = cap.read()
        # setup initial location of window
        r,h,c,w = 250,90,400,125 # simply hardcoded the values
        track_window = (c,r,w,h)
        # set up the ROI for tracking
        roi = frame[r:r+h, c:c+w]
        hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        while(1):
            ret ,frame = cap.read()
            if ret == True:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
                # apply meanshift to get the new location
                ret, track_window = cv2.CamShift(dst, track_window, term_crit)
                # Draw it on image
                pts = cv2.boxPoints(ret)
                pts = np.int0(pts)
                img2 = cv2.polylines(frame,[pts],True, 255,2)
                cv2.imshow('img2',img2)
                k = cv2.waitKey(60) & 0xff
                if k == 27:
                    break
                else:
                    cv2.imwrite(chr(k)+".jpg",img2)
            else:
                break
        cv2.destroyAllWindows()
        cap.release()
        pass

    @staticmethod
    def meanshift001():
        # cap = cv2.VideoCapture('relay.flv')
        cap = cv2.VideoCapture(0)

        # take first frame of the video
        ret,frame = cap.read()
        # setup initial location of window
        r,h,c,w = 250,90,400,125 # simply hardcoded the values
        track_window = (c,r,w,h)
        # set up the ROI for tracking
        roi = frame[r:r+h, c:c+w]
        hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        while(1):
            ret ,frame = cap.read()
            if ret == True:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
                # apply meanshift to get the new location
                ret, track_window = cv2.meanShift(dst, track_window, term_crit)
                # Draw it on image
                x,y,w,h = track_window
                img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
                cv2.imshow('img2',img2)
                k = cv2.waitKey(60) & 0xff
                if k == 27:
                    break
                else:
                    cv2.imwrite(chr(k)+".jpg",img2)
            else:
                break
        cv2.destroyAllWindows()
        cap.release()
        pass

    @staticmethod
    def capture_camera002():
        cap = cv2.VideoCapture(0)
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                frame = cv2.flip(frame,0)
                # write the flipped frame
                out.write(frame)
                cv2.imshow('frame',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        # Release everything if job is finished
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    @staticmethod
    def capture_camera001():
        cap = cv2.VideoCapture(0)
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow('frame',gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def show_image002():
        img = cv2.imread('Tools\\image.jpg',0)
        plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
        plt.xticks([]), plt.yticks([]) # to hide tick values on X and Y axis
        plt.show()

    @staticmethod
    def show_image001(
        path_image = pic_face_png
    ):

        img = cv2.imread(path_image,0)
        # cv2.namedWindow('potatoe', cv2.WINDOW_NORMAL)
        cv2.imshow('image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

