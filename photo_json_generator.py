import base64
import json
import os
import time


class PhotoJson(object):

    def __init__(self, img_name):
        self.img = img_name

    def generate(self):
        # start = time.time()
        request_json = self.generate_request_json()

        with open('request.json', 'w') as request_file:
            request_file.write(json.dumps(request_json))
        API_key = "AIzaSyD_olILEcP-FsTGbsu669oLMxHt4wo4QyI"
        curl_command = "curl -v -s -H \"Content-Type: application/json\" https://vision.googleapis.com/v1/images:annotate?key="
        curl_command += API_key
        curl_command += " --data-binary @request.json"
        raw_res = os.popen(curl_command).read()
        res = json.loads(raw_res)
        # end = time.time()
        # print("The time taken to fetch labels is: ", end - start, file=sys.stdout)
        with open('data.json', 'a') as cache_file:
            for c in raw_res:
                if c not in " \n":
                    cache_file.write(c)
        return res

    def generate_request_json(self):
        request_object = {}
        request_object["requests"] = []
        requests = request_object["requests"]
        requests.append({})
        first_request = requests[0]
        byte_encoded_pic = self.encode_image_base64()
        first_request["image"] = {"content": byte_encoded_pic}
        first_request["features"] = []
        first_request["features"].append({"type": "LABEL_DETECTION"})
        first_request["features"].append({"type": "FACE_DETECTION"})
        first_request["features"].append({"type": "LANDMARK_DETECTION"})
        first_request["features"].append({"type": "TEXT_DETECTION"})
        first_request["features"].append({"type": "LOGO_DETECTION"})
        return request_object

    def encode_image_base64(self):
        with open(self.img, 'rb') as image_file:
            image_data = image_file.read()
            encoded_data = base64.b64encode(image_data)
        return encoded_data.decode('ascii')


#function that uses url to get tags
"""def generate_requestJSON(img_url):
    request_object = {}
    request_object["requests"] = []
    requests = request_object["requests"]
    requests.append({})
    first_request = requests[0]
    first_request["image"] = {"source": {"imageUri": img_url}}
    first_request["features"] = []
    first_request["features"].append({"type": "LABEL_DETECTION"})
    first_request["features"].append({"type": "FACE_DETECTION"})
    first_request["features"].append({"type": "LANDMARK_DETECTION"})
    first_request["features"].append({"type": "TEXT_DETECTION"})
    first_request["features"].append({"type": "LOGO_DETECTION"})
    return request_object

def getLabelsWithCurl(img_url):
    start = time.time()
    request_json = generate_requestJSON_localImg(img_url)
    with open('request.json', 'w') as request_file:
        request_file.write(json.dumps(request_json))
    API_key = "AIzaSyD_olILEcP-FsTGbsu669oLMxHt4wo4QyI"
    curl_command = "curl -v -s -H \"Content-Type: application/json\" https://vision.googleapis.com/v1/images:annotate?key="
    curl_command += API_key
    curl_command += " --data-binary @request.json" 
    raw_res = os.popen(curl_command).read()
    res = json.loads(raw_res)
    end = time.time()
    print("The time taken to fetch labels is: ", end - start)
    with open('data.json', 'a') as cache_file:
        for c in raw_res:
            if c not in " \n":
                cache_file.write(c)
    return res"""
