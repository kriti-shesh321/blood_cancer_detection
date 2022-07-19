import cv2 #r
# import xgboost as xgb #r
from keras.applications.vgg19 import VGG19 #r
import numpy as np #r
# import streamlit as st 
from PIL import Image , ImageOps
from joblib import load #r
import matplotlib.pyplot as plt #r
from flask import Flask,jsonify,request
from flask_cors import CORS

model = load('vgg19_svm50.joblib')

map_dict = {0: 'leukemia',
            1: 'myeloma',
            2: 'normal'}

app = Flask(__name__)
CORS(app)

@app.route("/detect_cancer_type", methods=['POST'])
def detect_cancer_type():
    uploaded_file = request.files.getlist('file[]')[0]
    if uploaded_file.filename != '':
        file_extension = uploaded_file.filename.split('.')[-1]
        allowed_ext = ["jpg", "jpeg", "png", "bmp"]
        print("Ext",file_extension)
        if file_extension.lower() in allowed_ext:
            VGG_model = VGG19(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

            #Make loaded layers as non-trainable. This is important as we want to work with pre-trained weights
            for layer in VGG_model.layers:
                layer.trainable = False


            # Convert the file to an opencv image.
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, 1)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = cv2.resize(img,(128,128))

            fig = plt.figure()
            plt.imshow(img)
            plt.axis('off')
            img = img/255.0

            input_img = np.expand_dims(img, axis=0) #Expand dims so the input is (num images, x, y, c)
            input_img_feature=VGG_model.predict(input_img)
            input_img_features=input_img_feature.reshape(input_img_feature.shape[0], -1)
            prediction = model.predict(input_img_features)[0]
            # st.title("Predicted Label for the image is {}".format(map_dict[prediction]))
            # st.pyplot(fig)
            print(prediction)
            data = {
                "status":200,
                "data":"Predicted Label for the image is "+map_dict[prediction]
            }
        else:
            data = {
            "status":400,
            "data": "Invalid File extension. We only support "+', '.join(allowed_ext)
            }
    else:
        data = {
            "status":500,
            "data": "Error occured while uploading file. Please try again"
        }
    
  
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)







    