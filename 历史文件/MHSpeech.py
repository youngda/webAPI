#coding:utf-8
"""
讯飞语音处理
"""
import requests
import json
import base64
import hashlib 
import time 
import wave 

def hashValue(x): 
    m2 = hashlib.md5()   
    m2.update(x)
    return m2.hexdigest()
	
def base64Value(x):
    return base64.b64encode(x)
	
def jsonString(x):
    
    return json.dumps(x)
	
def currentTime():
    return str(int(time.time()))
	
class MHSpeech(object):
    """this is a class"""
    def __init__(self,X_Appid,apiKey):
        self.X_Appid = X_Appid
        self.apiKey =apiKey
        self.__textUrl="http://api.xfyun.cn/v1/aiui/v1/text_semantic"
        self.__asrUrl="http://api.xfyun.cn/v1/aiui/v1/iat"
        self.__speechUrl="http://api.xfyun.cn/v1/aiui/v1/voice_semantic"
        self.__ttsUrl="http://api.xfyun.cn/v1/service/v1/tts"
	
    def rePost(self,cmdType,url,data,type="text",):
        dataType=type
        X_CurTime=currentTime()
        X_Param=base64Value(json.dumps(cmdType))
        data=dataType+"="+base64Value(data)
        X_CheckSum=self.apiKey+X_CurTime+X_Param+data
        X_CheckSum=hashValue(X_CheckSum)
        headers = {"Content-Type":"application/x-www-form-urlencoded;charset=utf-8",
                   "X-Appid":self.X_Appid,
		           "X-CurTime":X_CurTime,
		           "X-Param":X_Param,
		           "X-CheckSum":X_CheckSum
		           }
        r =requests.post(url, data=data, headers=headers)
        return r	
    def text(self,text):
        option={'scene':'main','userid':'user_0001'}
        r=self.rePost(option,self.__textUrl,text,"text")
        return r.json()
    def asr(self,waveFile):
        option={"auf":"16k","aue":"raw","scene":"main"}
        f=open(waveFile,"rb")
        strData = f.read()
        f.close()
        r=self.rePost(option,self.__asrUrl,strData,"data")
        return r.json()
    def speech(self,waveFile,userid):
        option={"auf":"16k","aue":"raw","scene":"main","userid":userid} 
        f=open(waveFile,"rb")
        strData = f.read()
        f.close()
        r=self.rePost(option,self.__speechUrl,strData,"data")
        return r.json()
  		
if __name__=="__main__"	:
    X_Appid="5a5f01d5"
    apiKey="a92baaf59a2d48debf27ad65c55fb364"
    sxy=MHSpeech(X_Appid,apiKey)
    b=sxy.text("中华人民共和国")
    c=sxy.asr("1.wav")
    d=sxy.speech("1.wav","sxy_1")
    print json.dumps(b).decode("unicode-escape")
    print 
    print json.dumps(c).decode("unicode-escape")
    print
    print json.dumps(d).decode("unicode-escape")
    