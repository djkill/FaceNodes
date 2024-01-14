from deepface import DeepFace
import json 
import cv2
import numpy as np
from PIL import Image
import torch

# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


# Our any instance wants to be a wildcard string
any = AnyType("*")

class AnyToString:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "any": (any, {}),                                        },
        }

    RETURN_TYPES = ("STRING",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    #OUTPUT_NODE = False

    CATEGORY = "utils"

    def test(self, any):
        res = str(any)
        return {"ui": {"tags": res}, "result": (res,)}

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

    RETURN_TYPES = ("BOOLEAN", "FLOAT", "STRING")
    RETURN_NAMES = ("verified", "distance", "result")

    FUNCTION = "test"

    #OUTPUT_NODE = False

    CATEGORY = "Facial"

    def test(self, image1, image2, metric):
        tensor1 = image1*255
        tensor1 = np.array(tensor1, dtype=np.uint8)        
        tensor2 = image2*255
        tensor2 = np.array(tensor2, dtype=np.uint8)        
        objs = DeepFace.verify(tensor1[0], tensor2[0], distance_metric = metric)
        res = json.dumps(objs,)
        print(res)
        return objs["verified"], objs["distance"], res


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "FaceAnalyze": FaceAnalyze,
    "FaceCompare": FaceCompare,
    "AnyToString": AnyToString,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "FaceAnalyze": "Facial Attribute Analysis",
    "FaceCompare": "Face similarity",
    "AnyToString": "Any To String",
}