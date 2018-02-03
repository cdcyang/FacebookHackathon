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
        filename = request.args.get('file')
        windows_filename = "/mnt/c/xampp/htdocs" + filename
        #print("filename is: ", filename, file=sys.stdout)
        if filename:
            tags = photo_tag.get_tags(windows_filename)
            return tags
        return "no file name supplied"
    else:
        return "please use GET"