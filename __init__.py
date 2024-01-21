import json 
import os
import cv2
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import torch
import yadisk
import folder_paths as comfy_paths
from datetime import datetime

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


class SaveYDrive:

    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {
                "images": ("IMAGE", ),
                "token": ("STRING", {"default": ""}),
            },
            "hidden": {
                "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    RETURN_NAMES = ()

    FUNCTION = "save_image"

    OUTPUT_NODE = True

    CATEGORY = "image"

    def save_image(self, images, token="", prompt=None, extra_pnginfo=None):
        subfolder = datetime.today().strftime('%Y-%m-%d')
        timef = datetime.today().strftime('%H:%M:%S.%f')[:-3]
        client = yadisk.Client(token=token)
        # Проверяет, валиден ли токен
        print(client.check_token())    
        # Получает общую информацию о диске
        print(client.get_disk_info())
        try:
            client.mkdir("Comfy/"+subfolder)
        except yadisk.exceptions.PathExistsError:
            pass     
        tmpdir = comfy_paths.get_temp_directory()
        results = list()
        counter = 0
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            metadata = PngInfo()
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))            
            
            file = f"{timef}_{counter}.png"
            output = os.path.join(tmpdir, subfolder)
            if not os.path.exists(output):
                os.makedirs(output)
            res = os.path.join(output, file)    
            img.save(res, pnginfo=metadata, compress_level=4)
            client.upload(res, os.path.join("Comfy/"+subfolder, file)) 
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": "temp"
            })
            counter += 1
        print(results)
        return { "ui": { "images": results } }      



# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "AnyToString": AnyToString,
    "SaveYDrive": SaveYDrive,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "AnyToString": "Any To String",
    "SaveYDrive": "Save to Yandex drive",
}