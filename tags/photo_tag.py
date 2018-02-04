import datetime as dt
import json
import photo_json
import random


class PhotoTag(object):
    def __init__(self, input_json, num_result):
        self.input_json = input_json
        self.num_result = num_result
        self.result_tags = []

    def process(self):
        print(str(dt.datetime.now()) + " Start processing tagging json.")
        confirm_tags, photo_tags = self.load_result_tag()
        print(str(dt.datetime.now()) + " Completed processing image json")

        print(str(dt.datetime.now()) + " Start scrapping trending hashtags")
        trending_tags = self.load_instgram_trending_tags()
        print(str(dt.datetime.now()) + " Completed scrapping trending hashtags")

        print(str(dt.datetime.now()) + " Start tag comparison")
        self.result_tags = self.get_matching_tags(confirm_tags, photo_tags, trending_tags)
        print(str(dt.datetime.now()) + " Completed tag comparison")

        print(str(dt.datetime.now()) + " Returning comparison result")
        return json.dumps(self.result_tags)

    def get_matching_tags(self, confirm_tags, input_tags, trending_tags):
        top_result = self.process_confirmed_tags(confirm_tags)

        match_tags = self.compare_input_trending_tags(input_tags, trending_tags)
        top_result.extend(match_tags)
        print(str(dt.datetime.now()) + " Find " + str(len(top_result)) + " matching tags from the image description")

        if len(top_result) < self.num_result:
            top_result.extend(self.fill_tags(top_result, input_tags))

        return top_result

    def fill_tags(self, match_tags, input_tags):
        unmatched_tags = self.get_unused_tags(match_tags, input_tags)
        rand_set = set()
        unused_tag = []

        missing = len(unmatched_tags)

        while missing:
            index = random.randint(0, len(unmatched_tags) - 1)
            if index not in rand_set:
                selected_tag = unmatched_tags[index]
                temp = dict()
                temp['hashtag'] = selected_tag
                unused_tag.append(temp)
                rand_set.add(index)
                missing -= 1
            else:
                continue
        return unused_tag

    def get_unused_tags(self, match_tags, input_tags):
        unmatched = input_tags[:]

        for tag_pair in match_tags:
            tag = tag_pair['hashtag']
            if tag in unmatched:
                unmatched.remove(tag)
        return unmatched

    # region Construct tag_pairs
    def process_confirmed_tags(self, tags_list):
        confirmed = []
        for tag in tags_list:
            confirmed.append(self.__constructor_hashtag_pair(tag))
        return confirmed

    def compare_input_trending_tags(self, input_tags, trending_tags):
        matched = []
        for tag in input_tags:
            if tag in trending_tags:
                matched.append(self.__constructor_hashtag_pair(tag))
        return matched

    def __constructor_hashtag_pair(self, tag):
        tag_pair = dict()
        tag_pair['hashtag'] = tag
        return tag_pair
    # endregion

    # region Get Instagram trending tags
    def load_instagram_tags_dummy(self):
        popular_tags = dict()
        i = 1
        with open('example_tags.txt', 'r') as trending:
            for line in trending:
                tag = line.strip()[1:]
                popular_tags[tag] = i
                i += 1
        return popular_tags

    def load_instgram_trending_tags(self):
        return (self.load_instagram_tags_dummy())

    # endregion

    # region Get photo tags from result json
    def load_result_tag(self):
        data = self.input_json
        annotation = data['responses'][0]

        confirm_tags = []
        label_tags = []
        lookup_list = ['landmarkAnnotations', 'faceAnnotations', 'logoAnnotations', 'textAnnotations']

        for lookup in lookup_list:
            if lookup in annotation:
                labels = annotation[lookup]
                for label in labels:
                    description = self.__get_description(label, 'description', 0.5)
                    if description: confirm_tags.append(description)

        labels = annotation['labelAnnotations']
        for label in labels:
            description = self.__get_description(label, 'description', 0.80)
            if description: label_tags.append(description)
        return confirm_tags, label_tags

    def __get_description(self, label, loc='description', confidence_level=0.80):
        if loc not in label: return ""
        if ('score' not in label) or (label['score'] < confidence_level): return ""

        raw_description = label[loc]
        formatted_description = raw_description.replace(" ", "").lower()
        return formatted_description
    # endregion


def get_tags(filename):
    json_generator = photo_json.PhotoJson(filename)
    json_data = json_generator.generate()
    photo_tags = PhotoTag(json_data, 10)
    result = photo_tags.process()
    print(str(dt.datetime.now()) + " The result json is " + str(result))
    return result


get_tags('big_ben.jpg')
