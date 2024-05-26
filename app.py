#import re
import numpy as np
import os
from flask import Flask, app,request,render_template, redirect, url_for,jsonify
from tensorflow.keras import models
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.python.ops.gen_array_ops import concat
from tensorflow.keras.applications.inception_v3 import preprocess_input
import requests
import tensorflow as tf
from PIL import Image
from tensorflow.keras.preprocessing.image import load_img,img_to_array

#Loading the model
modeln=load_model(r"vgg-16-Tea-leaves-disease-model.h5")


app=Flask(__name__)

#default home page or route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def inde1():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/teahome')
def teahome():
    return render_template('teahome.html')

@app.route('/teapred')
def teapred():
    return render_template('teapred.html')

@app.route('/tearesult',methods=["GET","POST"])
def nres():
    if request.method=="POST":
        f=request.files['image']
        path=f'static/uploads/{f.filename}'
        if not os.path.exists('static/uploads'):
            os.mkdir('static/uploads/')
        print("PATH",path)
        f.save(path)
        img=image.load_img(path,target_size=(224,224))
        x=image.img_to_array(img)#img to array
        x=np.expand_dims(x,axis=0)#used for adding one more dimension
        #print(x)
        img_data=preprocess_input(x)
        prediction=np.argmax(modeln.predict(img_data))
        
        index=['Anthracnose  ',
        'algal leaf ',
        'bird eye spot',
        'brown blight',
        'gray light',
        'healthy',
        'red leaf spot',
        'white spot']
        nresult = str(index[prediction])
        
        return render_template('teapred.html',prediction=nresult,path=path)
        



""" Running our application """
if __name__ == "__main__":
    app.run(debug =True, port = 8080)