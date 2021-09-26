import os

from flask import Flask, send_file
from flask_restful import Api, Resource, reqparse
import werkzeug
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)

# Image database
images = [None] * 100

# Set up image uploading
upload_folder = './images'
allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = upload_folder

# Helper functions
def get_unused_image_id():
    """
    Returns the first available image id in the database, else error
    """
    for i in range (0,100):
        if images[i] == None:
            return i
    raise Exception("Image repository full")

def valid_file_ext(filename):
    """
    Checks if the given file is in one of the allowed image formats
    """
    return '.' in filename \
           and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_filepath(index, filename):
    """
    Returns filepath of image in system
    """
    return os.path.join(app.config['UPLOAD_FOLDER'], str(index) + filename)

# Main class for most of our basic api calls
class Image(Resource):
    def get(self, id=-1):
        """
        Returns image file
        """
        if id == -1:
            return "please specify a picture name or id" 
        elif id < -1 or id > 100:
            return "id must be an integer between 0 and 99", 400 # Add proper format
        if images[id] != None:
            print(images[id]["filename"])
            return send_file(get_filepath(id, images[id]["filename"]), download_name=images[id]["filename"], as_attachment=True)
        return "this image id does not exist", 404

    def post(self):
        """
        Adds new image
        """
        parser = reqparse.RequestParser()
        parser.add_argument("image_file", type=werkzeug.datastructures.FileStorage, location='files')
        params = parser.parse_args()
        if not params["image_file"]:
            return "please pass image_file as argument", 400
        try:
            image_id = get_unused_image_id() 
        except Exception as e:
            return e.text, 403
        image_file = params["image_file"]
        if valid_file_ext(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_file.save(get_filepath(image_id, image_filename))
        image = {
            "id": image_id,
            "filename": image_filename
        }
        images[image_id] = image
        return image, 201

    def put(self, id):
        """
        Updates image entry, changing name
        """
        parser = reqparse.RequestParser()
        parser.add_argument("image_name")
        params = parser.parse_args()

        if images[id] == None:
            return "this image id does not exist", 404
        images[id]["name"] = params["image_name"]
        return images[id], 200

    def delete(self, id):
        """
        Deletes image
        """
        if images[id] == None:
            return "this image id does not exist", 404
 
        os.remove(get_filepath(id, images[id]["filename"]))
        images[id] = None

class Image_LS(Resource):
    def get(self):
        """
        Returns a list of all existing images
        """
        existing_images = list(filter(lambda x: x != None, images))
        return list(filter(lambda x:x != None, images)), 201

api.add_resource(Image, "/images", "/images/", "/images/<int:id>")
api.add_resource(Image_LS, "/images/ls", "/images/ls/")

if __name__ == '__main__':
    app.run(debug=True)
