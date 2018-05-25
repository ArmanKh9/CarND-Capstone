from styx_msgs.msg import TrafficLight
import cv2
import os
import matplotlib.image as mpimg
import numpy as np
from keras.layers import GlobalAveragePooling2D, Input, Flatten, Dense, Dropout
from keras.applications.resnet50 import ResNet50
from keras.optimizers import Adam
from keras.models import Model, Sequential

cwd = os.path.dirname(os.path.realpath(__file__))

#light_color = self.light_classifier.get_classification(cv_image)
class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.training_mode = False
        self.imgcount = 0
        self.img_path = '/home/student/CarND-Capstone/imgs/classifier/'
        self.model = self.load_model()
        pass

    def saveimage(self, image, type):
        if not self.training_mode:
            return
        print 'Saving image:', self.imgcount
        folder = ['red', 'green', 'yellow', 'unknown']
        fn = self.img_path + '/'+ folder[type] +'/' + str(self.imgcount) + '.jpg'
        cv2.imwrite(fn, image)
        self.imgcount += 1


    def load_model(self):
        os.chdir(cwd)
        base_model = ResNet50
        base_model = base_model(weights=None, include_top=False)
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        predictions = Dense(4, activation='softmax')(x)
        model = Model(inputs=base_model.input, outputs=predictions)
        model.load_weights('weights.h5')
        print('Traffic classifier model loaded.')
        return model



    def get_classification(self, image):

        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction



        lights = [TrafficLight.RED, TrafficLight.GREEN, TrafficLight.YELLOW, TrafficLight.UNKNOWN]
        rgb = cv2.resize(image[...,::-1], (224, 224))
        rgb = np.expand_dims(rgb, axis=0)
        #try:
        idx = self.model.predict(rgb)
        #except:
        idx = 3
        #print idx
        return lights[idx]
