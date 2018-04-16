#!/usr/bin/python
#coding:utf-8
"""
讯飞语音处理
"""
import sys
import requests
import json
import base64
import hashlib 
import time
import pyaudio 
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

class MHStream():
    def __init__(self,channels=2,rate = 16000,record_seconds=5):
        self.chunk=1024
        self.format = pyaudio.paInt16
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
    def waveRecord(self,output_file_name="wo.wav"):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
				frames_per_buffer=self.chunk)
        frames = []
        for i in range(0, int(self.rate/ self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(output_file_name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
    
    def wavePlay(self,input_file_name="wo.wav"):
        wf = wave.open(input_file_name, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True)
        data = wf.readframes(self.chunk)
        while data != '':
            stream.write(data)
            data = wf.readframes(self.chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
		
	
         		
	
if __name__=="__main__"	:
    X_Appid="5a8852c9"
    apiKey="632c442c46d843ef9910a5235a4919af"
    sxy=MHSpeech(X_Appid,apiKey)
    #lj=MHStream()
    #print "start recording....."
   # lj.waveRecord()
   # print "stop recording....."
    b=sxy.text("李白静夜思")
    #c=sxy.asr("1.wav")
    #d=sxy.speech("wo.wav","sxy_1")
   # lj.wavePlay()
    print json.dumps(b).decode("unicode-escape")
    # print 
    #print json.dumps(c).decode("unicode-escape")
   # print
   # print json.dumps(d).decode("unicode-escape")
    