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
path = "C:/Users/Sutrishna/Desktop/Pan_Ankit.jpg"

def post(self):
    image_file = open(path, "rb").read()

    headers    = {'Ocp-Apim-Subscription-Key': '065bddad0ed7496d9581b555db571d42',
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
#print(analysis)
    mainArray= analysis['regions'][0]['lines']

    NameArray = mainArray[1]['words']

    FNameArray = mainArray[2]['words']
    DOB = mainArray[3]['words']
    PANNumber = mainArray[5]['words']
    docType = mainArray[4]['words']
#Till now, I have found two formats of Pan. The below code work for the newer format.
#NameArray = analysis['regions'][1]['lines'][0]['words']

    Name = ""
    FName = ""
    DateOfBirth = ""
    PAN = ""
    DocType = ""

    for i in NameArray:
    #Name = i['text']
        Name += i['text'] + " "
    
    for i in FNameArray:
    #Name = i['text']
        FName += i['text'] + " "
    
    for i in DOB:
    #Name = i['text']
        DateOfBirth += i['text'] + " "
    
    for i in PANNumber:
    #Name = i['text']
        PAN += i['text'] + " "

    for i in docType:
    #Name = i['text']
        DocType += i['text'][0]
    
    result ={"Documet_Type":DocType,"Name":Name[:-1],"Father_Name":FName[:-1],"DOB":DateOfBirth[:-1],"ID":PAN[:-1]};   
    return result
print(result)
    
#api.add_resource(PanDetails, '/pandetails') # Route_1


if __name__ == '__main__':
  app.run()

