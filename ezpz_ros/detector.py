import rospy 
import cv2
from detecto.core import Model
from detecto.utils import filter_top_predictions

# Credits: detecto https://github.com/alankbi/detecto

class Detector(object):
    def __init__(self):
        self._model = Model()
    def predict(self, img):
        return self._model.predict(img)
    
class USBCamera(object):
    def __init__(self, usb_device):
        self._usb_device = usb_device
        self._device = cv2.VideoCapture(
            self._usb_device)   
    def __del__(self):
        self._device.release()
    def get_frame(self):
        _, frame = self._device.read()
        return frame

class DetectorNode(object):
    def __init__(self, node_name, camera, detector, threshold):
        rospy.init_node(node_name, anonymous = False)
        self._camera = camera
        self._detector = detector
        self._rate = rospy.Rate(5)
        self._score_threshold = threshold
        
    def run(self):
        while not rospy.is_shutdown():
            frame = self._camera.get_frame()
            predictions = self._detector.predict(frame)
            self.draw_bbox(frame, predictions)
            cv2.imshow("window", frame)
            cv2.waitKey(10)
            self._rate.sleep()
            
    def draw_bbox(self, img, p):
        for i in range(len(p[0])):
            label, bbox, probs = p[0][i], p[1][i], p[2][i]
            if (probs < self._score_threshold):
                return
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[2], bbox[3]), 
                          (255, 0, 0), 3)
            cv2.putText(img,
                    label, 
                    (bbox[0],bbox[1]), 
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255))

camera = USBCamera(0)
detector = Detector()

node = DetectorNode("detector_node", camera, detector, 0.85)

node.run()



