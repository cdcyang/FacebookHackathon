import photo_json
import random
import json
import logging


class PhotoTag(object):
    def __init__(self, input_json, num_result):
        self.input_json = input_json
        self.num_result = num_result
        self.result_tags = []

    def process(self):
        print("Start processing tagging json.")
        photo_tags = self.load_result_tag()
        print("Completed loading image json")

        print("Start scrapping trending hashtags")
        trending_tags = self.load_instgram_trending_tags()
        print("Completed scrapping trending hashtags")

        print("Start tag comparison")
        self.result_tags = self.rank_top_tags(photo_tags, trending_tags)
        print("Completed tag comparison")

        print("Returning comparison result")
        return json.dumps(self.result_tags)

    def compare_input_trending_tags(self, input_tags, trending_tags):
        matches =[]
        for tag in input_tags:
            if tag in trending_tags:
                tag_pair = dict()
                tag_pair['hashtag'] = tag
                tag_pair['rank'] = trending_tags[tag]
                matches.append(tag_pair)
        return matches

    def rank_top_tags(self, input_tags, trending_tags):
        match_tags = self.compare_input_trending_tags(input_tags, trending_tags)
        top_result = match_tags[:]
        print("Find " + str(len(top_result)) + " matching tags from the image description")

        if len(top_result) < self.num_result:
            top_result.extend(self.fill_tags(top_result, input_tags))

        return top_result

    def fill_tags(self, match_tags, input_tags):
        unmatched_tags = self.get_unused_tags(match_tags, input_tags)
        rand_set = set()
        unused_tag = []

        missing = len(unmatched_tags)

        while missing:
            index = random.randint(0, len(unmatched_tags) -1)
            if index not in rand_set:
                selected_tag = unmatched_tags[index]
                temp = dict()
                temp['hashtag'] = selected_tag
                temp['rank'] = 9999
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

    #region Get Instagram trending tags
    def load_instagram_tags_dummy(self):
        popular_tags = dict()
        i =1
        with open('dummy_tags', 'r') as trending:
            for line in trending:
                tag = line.strip()[1:]
                popular_tags[tag] = i
                i += 1
        return popular_tags

    def load_instgram_trending_tags(self):
        return(self.load_instagram_tags_dummy())

    # endregion

    #region  Generate photo tags from result json
    def load_result_tag(self):
        photo_tags = []
        data = self.input_json
        labels = data['responses'][0]['labelAnnotations']
        for label in labels:
            description = self.__get_description(label, 'description')
            if description: photo_tags.append(description)
        return photo_tags

    @staticmethod
    def __get_description(label, loc='description'):
        if loc not in label: return ""

        raw_description = label[loc]
        formatted_description = raw_description.replace(" ", "").lower()
        return formatted_description
    # endregion


def get_tags(filename):
    json_generator = photo_json.PhotoJson(filename)
    json_data = json_generator.generate()
    photo_tags = PhotoTag(json_data, 10)
    result = photo_tags.process()
    print("The result json is " + str(result))
    return result

