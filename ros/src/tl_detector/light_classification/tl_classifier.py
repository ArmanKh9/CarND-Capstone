from styx_msgs.msg import TrafficLight
import cv2
import matplotlib.image as mpimg
import numpy as np

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.training_mode = False
        self.imgcount = 0
        self.img_path = '/home/student/CarND-Capstone/imgs/classifier/'
        pass

    def saveimage(self, image, type):
        if not self.training_mode:
            return
        print 'Saving image:', self.imgcount
        folder = ['red', 'green', 'yellow', 'unknown']
        fn = self.img_path + '/'+ folder[type] +'/' + str(self.imgcount) + '.jpg'
        cv2.imwrite(fn, image)
        self.imgcount += 1

    def get_classification(self, image):

        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction

        lights = [TrafficLight.RED, TrafficLight.GREEN, TrafficLight.YELLOW, TrafficLight.UNKNOWN]
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        #  HUE Table
        #   Red:     0-10, 160-180
        #   Yellow:  28-47    i.e., (40-67)/360*255
        #   Green:   63-99    i.e., (90-130)/360*255
        red_th1 = cv2.inRange(hsv, (0, 120, 120), (10, 255, 255))
        red_th2 = cv2.inRange(hsv, (160, 120, 120), (179, 255, 255))
        red_cnt = cv2.countNonZero(red_th1) + cv2.countNonZero(red_th2)

        yellow_th = cv2.inRange(hsv, (28, 120, 120), (47, 255, 255))
        yellow_cnt = cv2.countNonZero(yellow_th)

        green_th = cv2.inRange(hsv, (63, 100, 100), (92, 255, 255))
        green_cnt = cv2.countNonZero(green_th)

        idx = np.argmax(np.array([red_cnt, green_cnt, yellow_cnt, 50]))

        if self.training_mode:
            self.saveimage(image, idx)

        return lights[idx]
