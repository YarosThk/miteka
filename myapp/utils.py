import os
import secrets
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

#saves book cover in a foulder with a random hexed name
def save_cover(form_cover):
    #for hexing image file in def save_picture
    hex_code = secrets.token_hex(8)
    #tuple of file name and extensions
    _, f_ext = os.path.splitext(secure_filename(form_cover.filename))
    file_name = hex_code + f_ext #this is the hexed picture name
    #app.root_path is the root path of our app, i think up until the __init__ file
    file_path = os.path.join(current_app.root_path, "static/book_covers", file_name)

    output_size = (230, 390)
    i = Image.open(form_cover)
    i.thumbnail(output_size)

    i.save(file_path) #saving the new resized picture
    return file_name

def delete_cover(current_cover):
    file_path = os.path.join(current_app.root_path, "static/book_covers", current_cover)

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        pass
