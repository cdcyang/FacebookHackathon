from flask import Flask
from flask import request
import photo_tag, sys

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == "GET":
        filename = request.args.get('file')
        #print("filename is: ", filename, file=sys.stdout)
        if filename:
            tags = photo_tag.get_tags(filename)
            return tags
        return "no file name supplied"
    else:
        return "please use GET"