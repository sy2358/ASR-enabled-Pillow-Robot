#-*- coding: utf-8 -*-

import time
import argparse
import re

parser = argparse.ArgumentParser(description='Speech Recognition Arduino Driver')
parser.add_argument('--noarduino', dest='arduino', action='store_false', default=True, help='activate if no arduino')
parser.add_argument('--noasr', dest='asr', action='store_false', default=True, help='activate if no asr')
parser.add_argument('--lang', dest='lang', default="en-US", help='select language')

args = parser.parse_args()
print 'start',args.arduino
if args.arduino:
  import serial

def connect():
    if not args.arduino:
        print('fake arduino: connected')
        return
    global arduino
    #Initiate a connection
    arduino = serial.Serial('COM3', 9600)
    #Read confirmation from Arduino
    while True:
        try:
            time.sleep(0.01)
            #read the message from the Arduino
            raw_message = str(arduino.readline())
            print(raw_message)
            #remove EOL characters from string
            message = raw_message.rstrip()
            if message == "Serial Connected":
                return message
        except:
            pass
            KeyboardInterrupt

def arduinoWrite(s):
    if not args.arduino:
        print('fake arduino sent: ['+s+']')
        return
    arduino.write(s)

def action(sentence, confidence):
    sentence = sentence.replace(" ","")
    if confidence>0.6 and re.search(r"똑바로누워", sentence):
        arduinoWrite('a')
    elif confidence>0.6 and re.search(r"엎드려", sentence):
        arduinoWrite('b')
    elif confidence>0.6 and re.search(r"책읽어", sentence):
        arduinoWrite('c')
    elif confidence>0.6 and re.search(r"자면안되", sentence):
        arduinoWrite('d')	
    elif confidence>0.6 and re.search(r"마사지", sentence):
        arduinoWrite('e')		
    elif confidence>0.6 and re.search(r"옆으로누워", sentence):
        arduinoWrite('f')

# connect to the arduino and wait for connection acknowledgement
connect()

if not args.asr:
  # test mode - type keywords
  print('TEST MODE - type sentences:')
  while True:
    line = raw_input("Type>> ")
    action(line,1)

else:
  import speech_recognition as sr
  # obtain audio from the microphone
  r = sr.Recognizer()
  with sr.Microphone() as source:
      print("Speak>>")
      audio = r.listen(source)

  # recognize speech using Google Cloud Speech
  GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
    "type": "service_account",
    "project_id": "heroic-bonbon-186721",
    "private_key_id": "e3be268e8231a40d7952f9088ca2c17ae8bb9890",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDWY/4VsihHMVf9\nodFEW4qSA95PIs+GJ1h1nrfRa6cQZcNGG1fiXTVgKlZxE/2ahL05s94Eji4q9k6x\ngrkYOHPyN74FZG+cqY9MYxp3W7Gp4244GgTM05ligWONy2w3rHFrNpm8hIKK5isj\n28vSnRT4Tru0cAktUgStJLj8bDUwQ0Y6zaA6PVjjWhsgH0NomUMVviLvWf79P5Y3\nNEPfVPc+GxaA+SpqexrDWSyYUFhMoq/BjuNxote8iaB5iQHoOxbEsxLISKDpfMAM\nVluYyOmOgH2b/jrlM22s0214M+M6gVkFbAb6FfpY+RHnH/mRw1MaxsEGChxyBiEm\nllPSB/OFAgMBAAECggEAMZk3BFpv3o6QGn2n/g5Gh+LMuNanF5R9LtLuGE01PIIq\nc8rqIVSqf0m0L1tuWaPZaiLOW5PwIuDSUldZjnyq+E/EjpdOifohTI0F57SnLNRQ\noLqGP0O50dP4zepQqi2jHKhoVzh5wfwfYV+dbyeHnS2L1+HugZVevxbGlCFNidEu\nIfY8yp8W6omF8W/jqUzEOfKoYVaR2b4iTxxks035m4IEegDrdwgj3Fkma5qvoQCz\nJUOQNtOyAutO2hMXUKgGuWbgGQYDEPDAWQW1OHa5L7xtT6NSMmx+5GFMToUTCtke\n0D3JMu3x6PZOsIMpAY3gw2Dx6YtTxv4Gy/6ar3pcAQKBgQDuDV3prCn5x56iQXDK\niUtV1d//OJct20xpCcBvY6J6vV8vWFq3jGUp1N+roGwHvo4r8Ut/QNViijrrBzM0\nISgLHJat7C5/ssVTUGkcomERcPPO5V/fx/TlaYwOHJUKKotDj3XnYnU7Kp200COS\nPILXPVkEL+S7RRiFlcSl1HrEAQKBgQDmje8cjZANCveJAx8OlbSm9aL2P3wfRgHZ\nKxf4+dSjDPmvF8/kPFit53RlWFW5fD+pNZR3o6pwCmH2CVF0JD8Lab74tiBzlgZR\nPt2nNIIUkB4367KBmTl+zijp65BM/1xn7W9kz6/Cidi7wIj/Q/J3qjBYNW80zksW\nrNYkgIQfhQKBgHEKtertz20GZwUj0DzNX5HeIyVeKSQkfC9w6wm6JYDlhlrEOSfq\nKmvn42LrpgEzcu3ZAoHmNq45d+r9m0oI6KwGImNqwVXwfZWnnJJ1ZWTT32MDNzjc\nCiYareBRoFCYjVNCv7ll3sd+4C7pm8qoo3U0c53yZEqtcAyXZy9cLAQBAoGBAIEY\nCEMcoQQsl94H+WPZP4YdFFp9waphMLfBAXNPsFh783KvCqDpiV4Ws33rsFRj1eGR\nNsimw9Bof+Gb5hf6E7L4Sw5ILHOMFY14ffQZ2pxY9hKpzxHyEdeG6DHSzMHQWpV2\nxWDVSbzMIqc+b3c/PIz0po09nj8bI8BWlrFppJFhAoGBANSCuuZPxwiBKvG0x2Bk\nBE65SGeovDPhkd74Oy+TJSY5SRB+pFXZXysLvJYWIENnOMMddeZb6QbkGZwvUMT5\nPSaprK518mRMGfysdfbdq1LMTU5FcRVhk90GdcQm1LQtoxu8vfNtuCmtnCpMkZCf\nV1WLByWqPgtGxZaPsgNPqxtt\n-----END PRIVATE KEY-----\n",
    "client_email": "testspeech@heroic-bonbon-186721.iam.gserviceaccount.com",
    "client_id": "103078585269405881654",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/testspeech%40heroic-bonbon-186721.iam.gserviceaccount.com"
  }"""

  try:
      results = r.recognize_google_cloud(audio, language = args.lang, 
                                        credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS,
                                        preferred_phrases=["똑바로누워","옆으로누워","엎드려","책읽어","자면","안","돼","마사지"], show_all=True)
      result = {}
      if 'results' in results:
        result = results['results'][0]['alternatives'][0]
        print "Recognized: '" + result['transcript'].encode("utf-8")+"'", "confidence:", result['confidence']
        action(result['transcript'].encode("utf-8"), result['confidence'])
      else:
        print("nothing recognized")
  except sr.UnknownValueError:
      print("Google Cloud Speech could not understand audio")
  except sr.RequestError as e:
      print("Could not request results from Google Cloud Speech service; {0}".format(e))

