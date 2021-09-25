import string

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

images = [None] * 100
images[0] = {"name": "tooster1"}

def get_unused_image_id():
    for i in range (0,100):
        if images[i] == None:
            return i
    raise Exception("Image repository full")

class Image(Resource):
    def get(self, id=-1):
        if id == -1:
            return "please specify a picture name or id" 
        elif id < -1 or id > 100:
            return "id must be an integer between 0 and 99", 400 # Add proper format
        if images[id] != None:
            return images[id]["name"]
        else:
            return "this image id does not exist", 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image_name")
        params = parser.parse_args()
        if not params["image_name"]:
            return "please pass image_name as an argument", 400
        try:
            image_id = get_unused_image_id() 
        except Exception as e:
            return e.text, 403
        image = {
            "name": params["image_name"]
        }
        images[image_id] = image
        return image, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("image_name")
        params = parser.parse_args()

        if images[id] == None:
            return "this image id does not exist", 404
        images[id]["name"] = params["image_name"]
        return images[id], 200

    def delete(self, id):
        if images[id] == None:
            return "this image id does not exist", 404
 
        images[id] = None

api.add_resource(Image, "/images", "/images/", "/images/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
