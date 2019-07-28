#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)


# recognize speech using Google Cloud Speech
GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "jamong-186805",
  "private_key_id": "3cc9b91a3a123b71747ad7bfd39724aa0ecb04dd",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqNk7dNIwffw/A\nerrn4Fe3yrp/hKoUhsL1FI3jU862oIUSQ53lIdx016G25eusPwXGWygXrOGU/PM9\nixImaKR1NVIAowUoShSx7x5rMGzoibmoZ1+D3SX+fHN9GeCHzV+/LIv3Px8v2e3f\n4PlE0r1MUICglboaQWsfSNjTLETiL5x+lyTZmhGRpcyPcs6Hctfn43AZqNfTO22U\nvIwIiJ8k3r1IUxwXFgJ8r9r+L8kHlAVi45cVQcTidBWxUoYvsrVrmT/ft+ssbE0G\nbbp0xMQmKazPsLe7e05ibNIiwqXA2GzD61/pL9VmTeX61gSSet6adxxMMt0kEqym\nvKgXpbehAgMBAAECggEAAu2nQq/+PyZ492dFIusdpzhSKBJ4uJyu6vd9D22oL0Uo\ntO074K7J86qoChT/jnmRGF4GHQ4o3V7Ssnrbh5SiS6/spr0nQA+yNnN2MwLkxMVl\nz8tjfcnGtw+eDwdscPmsDYZvLARGfZTCvmjI8RGtFwyFgf3Bc2UvuhyPOmbXEosW\n8pj+alx9pGApBhqKVyGi9V1GywVg+7dIBRVutfFGkWo+ItPyA7MYf4b8A1T6poIA\nYf5fEHJHxvN80uLXxx3OqgFiBvtZIOC/gpwHZ9KD6+gAyZYV04WVazU8P7PWltwO\nZnhyWabRhJmOXFru+B7nULOzK5O+V8qiUjslAsw+oQKBgQDhOvhl7sjgJXb/mktV\nWjlAv65lg/exZklucew4r5qetcwE9rnoNrUuGxCTrFZQkgd8Us3Db2s+YO6KjwEj\n2INT1VzRsSYufd38DM4xb01lgEDV3SYoNl3QBDsudLB1tWe45VBvDJNn0ywu3u2i\n8ipttb1kSxKEtic4qZP5V08rWQKBgQDBdyyJQKnpl14M0ARLC9qMmVa5AYCPakYt\n01tT1HLS+vrBKF7F1lzswurgnu9ijT3GBvINllH9iqg4SgOU+2/p3Cg3JxrZznwQ\naVLJ4NDFvz4qtX5R2fBv/114U8xqsUSYgPtATqp3eFKnWV8rPDavbAtfZEDyBXtD\nqFz2gzQNiQKBgAglG8qD4hvI/w6rQ8Ioax2eUO424YQ20Lz/va0nHI5UwLYFPh/Z\nqp+qNuVAPDbZsQ+b5vkEVHqDAt1b4oyrTcSAWMT0hQ71Wku9Is/C2KetBas2PiUC\nIk5deM5rRd5b2w5irI/3gnUku9pOEYXs///LrLetx1OpSq3P5BwGPkSxAoGBAIjv\nREulxF49MGmbNt6zdi58PmDWilt4WlIHPqY4QknJMYFUhLg9QSqn0D3K4R99X1Ly\nCZPKaSAva1/kK2LhEVaS6LgY6q1ttGydT+bqRHsjIOpz6gQfYUq0kkEf9xkxfZ7/\n9FaRF6FWPhKLdIwSo5ZIwEf1mu5zKMs7uQkW1toZAoGAJT3/OFx4YnDvmjhs7xig\nAvaEWK9PGG9EmDlD0MhDlSWd5mll8f2Dn73Slrd2Qv7x9gYKcuKpNykqKvF8JqIv\naF82wWCz/YnFHs08ZIfhQfNEDw/oEod2CJtdrfCV/H34P8IV8FyRXC1dKEJhHVRY\nfntsagUo83jKYOAuUFC6TwA=\n-----END PRIVATE KEY-----\n",
  "client_email": "jamong@jamong-186805.iam.gserviceaccount.com",
  "client_id": "107732509745873817964",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/testspeech%40heroic-bonbon-186721.iam.gserviceaccount.com"
}"""
try:
    print("Google Cloud Speech thinks you said " + r.recognize_google_cloud(audio, language = "ko", credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
except sr.UnknownValueError:
    print("Google Cloud Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Cloud Speech service; {0}".format(e))
