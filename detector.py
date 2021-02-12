import detector_utils

class Detector:
    detector_params = {}
    detector = None

    def __init__(self):
        pass

    def set_detector_params(self, params):
        self.detector_params = params

    def detect(self):
        pass

class TSDetector(Detector):
    def __init__(self):
        self.detection_graph, self.sess = detector_utils.load_inference_graph()

    def detect(self, rgb_image):
        # returns (top [0], left [1], bottom [2], right [3])
        boxes, confidences = detector_utils.detect_objects(rgb_image, self.detection_graph, self.sess)

        im_height, im_width = rgb_image.shape[:2]

        detection_th = self.detector_params.get('detection_th', 0.2)
        objects = [(box[0] * im_height, box[3] * im_width, box[2] * im_height, box[1] * im_width) for box, score in zip(boxes, confidences) if score >= detection_th]
        # change to an array of (x, y, w, h)
        return [(int(left), int(top), int(right - left), int(bottom - top)) for (top, right, bottom, left) in objects]