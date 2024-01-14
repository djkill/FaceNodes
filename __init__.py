from deepface import DeepFace
import json 
import cv2
import numpy as np
from PIL import Image
import torch

class FaceAnalyze:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "image": ("IMAGE",),
                "backend": (['opencv', 
                              'ssd', 
                              'dlib', 
                              'mtcnn', 
                              'retinaface', 
                              'mediapipe',
                              'yolov8',
                              'yunet',
                              'fastmtcnn',], {}),
                                        },
        }

    RETURN_TYPES = ("STRING",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    #OUTPUT_NODE = False

    CATEGORY = "Facial"

    def test(self, image, backend):
        tensor = image*255
        tensor = np.array(tensor, dtype=np.uint8)        
        objs = DeepFace.analyze(tensor[0], actions=("age", "gender"), silent=False, enforce_detection=False, detector_backend = backend)
        res = json.dumps(objs,)
        print(res)
        return {"ui": {"tags": res}, "result": (res,)}

class FaceCompare:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "metric": (['euclidean_l2', 
                              'cosine', 
                              'euclidean',], {}),
            },
        }

    RETURN_TYPES = ("STRING",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    #OUTPUT_NODE = False

    CATEGORY = "Facial"

    def test(self, image1, image2):
        tensor1 = image1*255
        tensor1 = np.array(tensor1, dtype=np.uint8)        
        tensor2 = image2*255
        tensor2 = np.array(tensor2, dtype=np.uint8)        
        objs = DeepFace.verify(tensor1[0], tensor1[2], distance_metric = metric)
        res = json.dumps(objs,)
        print(res)
        return {"ui": {"tags": res}, "result": (res,)}


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "FaceAnalyze": FaceAnalyze,
    "FaceCompare": FaceCompare,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "FaceAnalyze": "Facial Attribute Analysis",
    "FaceCompare": "Face similarity"
}