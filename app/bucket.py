import os
from datetime import datetime
from io import BytesIO
from os import path
from PIL import Image
from tqdm import tqdm

import boto3
from werkzeug.utils import secure_filename

from app import app

def l_int(*l):
    return list(map(int, l))

def scale(img, n_size, return_type='i', format='JPEG'):
    im = img.copy()
    w, h = im.size
    if type(n_size) == tuple:
        n_w, n_h = n_size
        if n_w == 0:
            im = im.resize(l_int(n_h * w/h, n_h))
        elif n_h == 0:
            im = im.resize(l_int(n_w, n_w * h/w))
        else:
            if w >= h:
                im = im.resize(l_int(n_h * w/h, n_h))
                w, h = im.size
                im = im.crop(l_int((w - n_w)/2, 0, (w + n_w)/2, n_h))
            else:
                im = im.resize(l_int(n_w, n_w * h/w))
                w, h = im.size
                im = im.crop(l_int(0, (h - n_h)/2, n_w, (h + n_h)/2))
        
    elif type(n_size) in [float, int]:
        im = im.resize(l_int(w*n_size, h*n_size), Image.ANTIALIAS)
    
    else:
        raise TypeError(f'Invalid argument type. n_size is a {type(n_size)}.')
    
    if return_type == 'i':
        return im
    elif return_type == 'b':
        temp_file = BytesIO()
        im.save(temp_file, format=format)
        return temp_file
    else:
        raise ValueError(f'Only i and b are allowed as arguments for return_type. Set argument value is {return_type}')
        

def compress(img, quality=85, format='JPEG'):
    byte_img = BytesIO()
    img.save(byte_img, optimize=True, quality=quality, subsampling=0, format=format)
    byte_img.flush()
    byte_img.seek(0)

    return Image.open(byte_img)

def compress_and_scale(img, sizes, quality=85, format='JPEG', return_type='i'):
    return [scale(compress(img, quality, format), size, return_type, format) for size in sizes]
    
def save_images(img_list, sizes, filename="picture", filetype="jpg"):
    for img, size in zip(img_list, sizes):
        if type(size) == tuple:
            img.save(f"{size[0]},{size[1]}-{filename}.{filetype}")
        else:
            img.save(f"{size}-{filename}.{filetype}")
            
def upload_s3(key, obj, name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(app.config['S3_BUCKET'])
    obj.seek(0)
    bucket.upload_fileobj(obj, f"{key}/{name}", ExtraArgs={
                          'ACL': 'public-read'})
    
    return f"https://{app.config['S3_BUCKET']}.s3.amazonaws.com/{key}/{name}"       

def preprocess_img_and_upload(img, key, sizes=app.config["IMAGE_SIZES"], format='JPEG'):
    filename, filetype = os.path.splitext(secure_filename(img.filename))
    temp_file = BytesIO()
    img.save(temp_file)
    temp_file.flush()
    temp_file.seek(0)
    im = Image.open(temp_file)
    img_list = compress_and_scale(im, 
                                  sizes, 
                                  quality=app.config["IMAGE_QUALITY"], 
                                  format=format,
                                  return_type='b')
    
    img_urls = []
    
    for img, size in zip(img_list, sizes):
        if type(size) == tuple:
            w, h = size
            img_urls.append(upload_s3(key, img, f"{w},{h}-{filename}{filetype}"))
        else:
            img_urls.append(upload_s3(key, img, f"{size}-{filename}{filetype}"))
                
        img_urls_dict = dict(zip(app.config["IMAGE_SIZE_FORMAT"], img_urls))
    
    return img_urls_dict