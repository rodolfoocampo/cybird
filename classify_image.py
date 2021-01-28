# Lint as: python3
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Example using TF Lite to classify a given image using an Edge TPU.

   To run this code, you must attach an Edge TPU attached to the host and
   install the Edge TPU runtime (`libedgetpu.so`) and `tflite_runtime`. For
   device setup instructions, see g.co/coral/setup.

   Example usage (use `install_requirements.sh` to get these files):
   ```
   python3 classify_image.py \
     --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite  \
     --labels models/inat_bird_labels.txt \
     --input images/parrot.jpg
   ```
"""
from __future__ import print_function
import argparse
import time

from PIL import Image

import classify
import tflite_runtime.interpreter as tflite
import platform
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import time

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime
import re


EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': 'edgetpu.dll'
}[platform.system()]


def call_weather():
    # importing requests and json
    import requests, json
    # base URL
    
    # City Name CITY = "Hyderabad"
    # API key API_KEY = "Your API Key"
    # upadting the URL
    URL = "https://api.openweathermap.org/data/2.5/weather?" + "lat=" + "-35.27" + "&lon=" + "149.11" + "&appid=" + 'bfc6a1fecf64956df53b31547c383929' + "&units=metric"
    print(URL)
    # HTTP request
    response = requests.get(URL)
    print(response)
    # checking the status code of the request
    if response.status_code == 200:
       # getting data in the json format
       data = response.json()
       # getting the main dict block
       main = data['main']
       # getting temperature
       temperature = main['temp']
       # getting the humidity
       humidity = main['humidity']
       # getting the pressure
       pressure = main['pressure']
       # weather report
       report = data['weather'][0]['description']
       
       wind = data['wind']['speed']
       
       print(temperature, humidity, pressure, report, wind)

    else:
       # showing the error message
       print("Error in the HTTP request")
    return(temperature. humidity, pressure, report, wind)

def load_labels(path, encoding='utf-8'):
  """Loads labels from file (with or without index numbers).

  Args:
    path: path to label file.
    encoding: label file encoding.
  Returns:
    Dictionary mapping indices to labels.
  """
  with open(path, 'r', encoding=encoding) as f:
    lines = f.readlines()
    if not lines:
      return {}

    if lines[0].split(' ', maxsplit=1)[0].isdigit():
      pairs = [line.split(' ', maxsplit=1) for line in lines]
      return {int(index): label.strip() for index, label in pairs}
    else:
      return {index: line.strip() for index, line in enumerate(lines)}


def make_interpreter(model_file):
  model_file, *device = model_file.split('@')
  return tflite.Interpreter(
      model_path=model_file,
      experimental_delegates=[
          tflite.load_delegate(EDGETPU_SHARED_LIB,
                               {'device': device[0]} if device else {})
      ])


def validate_google_api():
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.


    
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

            
  service = build('sheets', 'v4', credentials=creds)
  return service

## this function uses the Google Sheets Python API to upload values
def upload_observation(date, hour, dateandtime, bird, fed, imagelink, confidence, service):



  values = [
      [
        date, hour, dateandtime, bird, fed, confidence, imagelink
      ],
      # Additional rows ...
  ]
  body = {
      'values': values
  }
  result = service.spreadsheets().values().append(
      spreadsheetId='1F0qtrtRo28imVHNk1VMyq1dgCAik6sc5HpivjDEci4E', range='A1:AA100',
      valueInputOption='USER_ENTERED', body=body).execute()
  print('{0} cells appended.'.format(result \
                                         .get('updates') \
                                         .get('updatedCells')))

def read_selected_bird(service):


  result = service.spreadsheets().values().get(
    spreadsheetId='1F0qtrtRo28imVHNk1VMyq1dgCAik6sc5HpivjDEci4E', range='Sheet4!A2').execute()
  rows = result.get('values', [])
  name = rows[0][0]
  return name

def main():
  
  # establish connection with Google API
  
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.


    
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

            
  service = build('sheets', 'v4', credentials=creds)
  SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

  creds = None
  # The file token.pickle stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.


    
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
          
  service = build('sheets', 'v4', credentials=creds)




  # set up the servo
  
  time_since_lastfed = 1000
  camera = PiCamera()
  while True:
    # obtain what bird was selected by user
    selected_bird = read_selected_bird(service)
    
    #camera.start_preview()
    sleep(.5)
    camera.capture('images/current_photo.jpg')
    #camera.stop_preview()
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-m', '--model', required=True, help='File path of .tflite file.')
    parser.add_argument(
        '-i', '--input', required=False, help='Image to be classified.')
    parser.add_argument(
        '-l', '--labels', help='File path of labels file.')
    parser.add_argument(
        '-k', '--top_k', type=int, default=1,
        help='Max number of classification results')
    parser.add_argument(
        '-t', '--threshold', type=float, default=0.0,
        help='Classification score threshold')
    parser.add_argument(
        '-c', '--count', type=int, default=5,
        help='Number of times to run inference')
    args = parser.parse_args()

    labels = load_labels(args.labels) if args.labels else {}

    interpreter = make_interpreter(args.model)
    interpreter.allocate_tensors()

    size = classify.input_size(interpreter)
    image = Image.open('images/current_photo.jpg').convert('RGB').resize(size, Image.ANTIALIAS)
    classify.set_input(interpreter, image)

    print('----INFERENCE TIME----')
    print('Note: The first inference on Edge TPU is slow because it includes',
          'loading the model into Edge TPU memory.')
    for _ in range(args.count):
      start = time.perf_counter()
      interpreter.invoke()
      inference_time = time.perf_counter() - start
      classes = classify.get_output(interpreter, args.top_k, args.threshold)
      #print('%.1fms' % (inference_time * 1000))

    print('-------RESULTS--------')
    for klass in classes:
      label = labels.get(klass.id, klass.id)
      ## Only if a bird was identified
      print(label)
      
      print(selected_bird)
      if label != '' and label != 'background':
        name = label.split('(')[1].split(')')[0]
        print(name, ' , confidence: ', klass.score)
      #print('%s: %.5f' % (labels.get(klass.id, klass.id), klass.score))
        
        if name == selected_bird and klass.score>.60:
          if time_since_lastfed > 12:
            servoPIN = 17
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(servoPIN, GPIO.OUT)

            p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
            p.start(4.7) # Initialization
  
            p.ChangeDutyCycle(6)
            time.sleep(0.2)

            p.ChangeDutyCycle(4.7)
            time.sleep(0.5)

            p.stop()
            GPIO.cleanup()
            

            dateTimeObj = datetime.now()
            date = dateTimeObj.strftime("%b %d, %Y")
            hour = dateTimeObj.strftime("%I %p")
            dateandtime = dateTimeObj.strftime("%b %d, %Y, %I:%M %p")
            
            upload_observation(date, hour, dateandtime, name,'no', '', '', service)

            time_since_lastfed = 0
            
        elif klass.score>.60:
             
            dateTimeObj = datetime.now()
            date = dateTimeObj.strftime("%b %d, %Y")
            hour = dateTimeObj.strftime("%I %p")
            dateandtime = dateTimeObj.strftime("%b %d, %Y, %I:%M %p")
            
            upload_observation(date, hour, dateandtime, name,'yes', '', '', service)
             
    time_since_lastfed += 1
    print(time_since_lastfed)
    
if __name__ == '__main__':
  main()
