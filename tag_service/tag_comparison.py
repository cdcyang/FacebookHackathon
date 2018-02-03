import json


class PhotoTags(object):

    def __init__(self, input_json, num_result):
        self.input_json = input_json
        self.num_result = num_result
        self.result_tags = []

    def process(self):
        photo_tags = self.load_result_tag()
        trending_tags = self.load_instgram_trending_tags()
        self.result_tags = self.rank_top_tags(photo_tags, trending_tags)
        return self.result_tags

    def compare_input_trending_tags(self, input_tags, trending_tags):
        show_on_website =[]
        for tag in input_tags:
            if tag in trending_tags:
                show_on_website.append((tag, trending_tags[tag]))
        return show_on_website

    def rank_top_tags(self, input_tags, trending_tags):
        match_tags = self.compare_input_trending_tags(input_tags, trending_tags)

        top_result = []
        for i in range(len(match_tags)):
            top_result.append(match_tags[i])

        if len(top_result) < self.num_result:
            missing_num = self.num_result - len(top_result)
            additional_tags = self.fill_top_result(match_tags, input_tags, missing_num)
            top_result.extend([(tag, 9999)for tag in additional_tags])
        return top_result[:self.num_result]


    def fill_top_result(self, match_tags, input_tags, missing_num):
        for tags in match_tags:
            if tags in input_tags:
                input_tags.remove(tags)
        return input_tags[:missing_num]

    #region Get Instagram trending tags
    def load_instagram_tags_dummy(self):
        popular_tags = dict()
        i =1
        with open('dummy_tags', 'r') as insta_tag:
            for line in insta_tag:
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

        with open(self.input_json, 'r') as json_data:
            data = json.load(json_data)
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


def main():
    photo_tags = PhotoTags("sample-data.json", 5)
    result = photo_tags.process()
    print(result)


if __name__ == '__main__':
    main()
    



