# coding: utf-8
from  PIL import Image
import requests as req
import binascii
import pytesseract
import sys
import os
import time

chall_url = "http://challenge01.root-me.org/programmation/ch8/"   # image encoded with base64

def getImageFromUrl(filename):    
    result = req.get(chall_url)
    if result.status_code != 200:
        print('Requests failed')
        sys.exit(1)    
    result = result.text
    tagStartIdx = result.find("<img src=")
    tagEndIdx = result.find("/>", tagStartIdx)
    imgEncoded = result[tagStartIdx:tagEndIdx].split(',')[1]
    img = binascii.a2b_base64(imgEncoded)
    with open('captcha.png', 'wb')  as f:
        f.write(img)  

def image2str(fullpath, lang='eng'):
    img = Image.open(fullpath)
    captcha = pytesseract.image_to_string(img, lang=lang, config="--psm 1 -c preserve_interword_spaces=1")

    return captcha

def sendCaptcha(captcha):
    data = {"cametu":captcha}
    result = req.post(chall_url, data=data)
    return result.text

def main():
    cnt = 0
    while True:
        filename = 'captcha.png'
        fullpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
        getImageFromUrl(fullpath)
        captcha = image2str(fullpath)
        print('Try [%d] ' % cnt, end='')
        cnt += 1
        if captcha.isascii():
            captcha = "".join(ch for ch in captcha if ch.isalnum())
            print("captcha is ", captcha)

            # below code is for root-me challenge.
            result = sendCaptcha(captcha)   
            if "Trop tard..." in result:
                print("to late..")
            elif "retente ta chance." in result:
                print("wrong captcha")
            else:
                print(result)
                break
        time.sleep(0.2) # too fast, skip extract processing

if __name__ == "__main__":
    main()
