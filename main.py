from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import requests 
import base64
import os
from os import listdir
from PIL import Image as PImage
from base64 import decodestring
import json
import http.client, urllib.request, urllib.parse, urllib.error, base64
from flask import Flask
app = Flask(__name__)

@app.route('/')
class PanDetails(Resource):
   
    def post(self):
        
        imageRequest = request.json['image_request']
        storeval=bytes(imageRequest, 'utf-8')
        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.decodebytes(storeval))
        
        #print(image_file)

        #Reading the image file directly
        image_file = open("imageToSave.png", "rb").read()

        headers    = {'Ocp-Apim-Subscription-Key': '3b70f44a460f42a1b1c91e3541b042b5',
                      'Content-Type': 'application/octet-stream'}
        params     = {'language': 'unk', 'detectOrientation': 'true'}
        vision_base_url = "https://westus.api.cognitive.microsoft.com/vision/v2.0/"
        ocr_url = vision_base_url + "ocr"
        response = requests.post(
            ocr_url, headers=headers, params=params, data=image_file)
        response.raise_for_status()
        #print(response.text)

        #Till now, I have found two formats of Pan. The below code work for the older format.
        analysis = response.json()
        mainArray= analysis['regions'][0]['lines']
        nameArray = mainArray[1]['words']
        fnameArray = mainArray[2]['words']
        dob = mainArray[3]['words']
        docType = mainArray[4]['words']
        panNumber = mainArray[5]['words']

        #Till now, I have found two formats of Pan. The below code work for the newer format.
        #NameArray = analysis['regions'][1]['lines'][0]['words']

        Name = ""
        FName = ""
        DateOfBirth = ""
        PAN = ""
        DocType = ""

        for i in nameArray:
            #Name = i['text']
            Name += i['text'] + " "
            
        for i in fnameArray:
            #Name = i['text']
            FName += i['text'] + " "
            
        for i in dob:
            #Name = i['text']
            DateOfBirth += i['text'] + " "
            
        for i in panNumber:
            #Name = i['text']
            PAN += i['text'] + " "
            
        for i in docType:
            #Name = i['text']
            DocType += i['text'][0]    
            
        #result ={"Documet_Type":DocType,"Name":Name,"Father_Name":FName,"DOB":DateOfBirth,"ID":PAN};  

        if response.text is not None:
            os.remove("imageToSave.png")
            
        result ={"Documet_Type":DocType,"Name":Name[:-1],"Father_Name":FName[:-1],"DOB":DateOfBirth[:-1],"ID":PAN[:-1]};   
        return result
    
api.add_resource(PanDetails, '/pandetails') # Route_1


if __name__ == '__main__':
  app.run()

