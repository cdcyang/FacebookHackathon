#sample JSON for label detection
"""{
  "requests": [
    {
      "image": {
        "source": {
          "imageUri": "https://cloud.google.com/vision/docs/images/ferris-wheel.jpg"
        }
      },
      "features": [
        {
          "type": "LABEL_DETECTION"
        }
      ]
    }
  ]
}"""

import requests
import json
from google.cloud import vision
from google.cloud.vision import types

def generate_requestJSON(img_url):
    """a = {
        "requests": [
            {
            "image": {
                "source": {
                "imageUri": "https://cloud.google.com/vision/docs/images/ferris-wheel.jpg"
                }
            },
            "features": [
                {
                "type": "LABEL_DETECTION"
                }
            ]
            }
        ]
        }"""
    request_object = {}
    request_object["requests"] = []
    requests = request_object["requests"]
    requests.append({})
    first_request = requests[0]
    first_request["image"] = {"source": {"imageUri": img_url}}
    first_request["features"] = []
    first_request["features"].append({"type": "LABEL_DETECTION", "maxResults": 5})
    return json.dumps(request_object)

def main():
    API_key = "AIzaSyD_olILEcP-FsTGbsu669oLMxHt4wo4QyI"
    uri = "https://vision.googleapis.com/v1/images:annotate?key=" + API_key
    img_Uri = "https://cloud.google.com/vision/docs/images/ferris-wheel.jpg"
    params = generate_requestJSON(img_Uri)
    res = requests.post(uri, data=params).json()
    print(res)
    with open('sample_data', 'a') as cache_file:
        cache_file.write(res)
    #print(res.json())
    #detect_labels_uri(uri)

def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

if __name__ == "__main__":
    main()