class Caption:
    def __init__(self, data):
        self.data = data

    def generate(self):
        caption = "I am "
        response = self.data["responses"][0]
        people = list()
        if "faceAnnotations" in response:
            emotions = {"joy": "happy", "sorrow": "sad", "anger": "angry", "surprise": "surprised"}
            for person in response["faceAnnotations"]:
                for emotion in emotions.keys():
                    if person[emotion + "Likelihood"] in ["LIKELY", "VERY_LIKELY"]:
                        people.append(emotion)
            tally = dict()
            common_emotion = ""
            max_count = 0
            for emotion in people:
                if emotion in tally:
                    tally[emotion] += 1
                else:
                    tally[emotion] = 1
                if tally[emotion] > max_count:
                    common_emotion = emotion
                    max_count = tally[emotion]
            if len(people) > 1:
                caption = "We are "
            common_emotion = emotions[common_emotion]
        else:
            common_emotion = "happy"
        if common_emotion == "happy":
            caption += "really enjoying "
            if len(people) > 1:
                caption += "ourselves"
            else:
                caption += "myself"
        else:
            caption += "really " + common_emotion
        if "landmarkAnnotations" in response:
            places = list()
            for place in response["landmarkAnnotations"]:
                places.append(place["description"])
            caption += " at " + places[0]
        caption += "!"
        return caption
