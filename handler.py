import math
import blowfish as bf
# def send(data):
def init():
    bf.init()

def handler_decrypt(arr):
    org=[]
    for ans in arr:
        if ans != '':
            s=str(bf.decrypt(int(ans)))
            for i in range(0,len(s),2):
                s1=s[i]+s[i+1]
                # print(s1)
                org.append(chr(int(s1)))
    return ''.join(org)
# print('final',final_org)

# data=input("Enter the Data ")
def handler_encrypt(data):
    data=data.upper()
    ans=""#data on encrypted
    arr=[]
    for i in range(math.ceil(len(data)/5)):
        num=""
        # print(i)
        for c in range(i*5,min((i+1)*5,len(data))):
            # print(c)
            num+=str(ord(data[c]))
        # print(num)
        if num != '':
            arr.append(str(bf.encrypt(int(num))))
    return arr
# init()
# ans=handler_encrypt(str("hi"))
# print(ans)
# org=handler_decrypt(ans)
# print(org)

