from flask import Flask
from flask import request
import photo_tag, sys
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/foo": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def main():
    if request.method == "GET":
        filename = '/Applications/XAMPP/xamppfiles/htdocs/' + request.args.get('file')
        print(filename)
        if filename:
            tags = photo_tag.get_tags(filename)
            print("file path is: ", filename, file=sys.stdout)
            return tags
        return "no file name supplied"
    else:
        return "please use GET"
