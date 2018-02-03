import json


def load_tag_from_vision_json(input_json):
    photo_tags = []

    with open(input_json, 'r') as json_data:
        data = json.load(json_data)
        labels = data['responses'][0]['labelAnnotations']
        for label in labels:
            description = get_description(label, 'description')
            if description: photo_tags.append(description)
    return photo_tags


def get_description(label, loc='description'):

    if loc not in label: return ""

    raw_description = label[loc]
    formatted_description = raw_description.replace(" ", "")
    return formatted_description


def load_image_json_dummy(file):

    photo_tags = []

    with open(file, 'r') as tags_file:
        for line in tags_file:
            photo_tags.append(line.strip())
        
    return photo_tags

def load_instagram_tags():
    pass


def load_instagram_tags_dummy():

    popular_tags = dict()
    i =1
    with open('dummy_tags', 'r') as insta_tag:
        for line in insta_tag:
            tag = line.strip()[1:]
            popular_tags[tag] = i
            i += 1
    return popular_tags
            
def compare_trending(input_tags):
    show_on_website =[]

    instgram_tags = load_instagram_tags_dummy()
    for tag in input_tags:
        if tag in instgram_tags:
            show_on_website.append((tag, instgram_tags[tag]))

    # if show_on_website:
    #     return input_tags

    return show_on_website

def main():
    example = load_image_json_dummy('example_tags')
    a = compare_trending(example)
    return a


if __name__ == '__main__':
    print(load_tag_from_vision_json('sample-data.json'))
    


