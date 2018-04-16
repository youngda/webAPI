#!/usr/bin/env python
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

class MH_ASR(object):
    """this is a class"""
    def __init__(self,X_Appid,apiKey):
        self.X_Appid = X_Appid
        self.apiKey =apiKey
		#文本语义
        self.__textUrl="http://api.xfyun.cn/v1/aiui/v1/text_semantic"
		#语音识别
        self.__asrUrl="http://api.xfyun.cn/v1/aiui/v1/iat"
		#语音语义
        self.__speechUrl="http://api.xfyun.cn/v1/aiui/v1/voice_semantic"

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

class MH_TTS(object):
    """this is a class"""
    def __init__(self,X_Appid,apiKey,aue="lame"):
        self.X_Appid = X_Appid
        self.apiKey =apiKey
        self.__ttsUrl="http://api.xfyun.cn/v1/service/v1/tts"
        self.aue=aue
    def getHeader(self,):
        curTime = str(int(time.time()))
        param = "{\"aue\":\""+self.aue+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
        paramBase64 = base64.b64encode(param)
        m2 = hashlib.md5()
        m2.update(self.apiKey + curTime + paramBase64)
        checkSum = m2.hexdigest()
        header ={
                'X-CurTime':curTime,
                'X-Param':paramBase64,
                'X-Appid':self.X_Appid,
                'X-CheckSum':checkSum,
                'X-Real-Ip':'127.0.0.1',
                'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header
    def getBody(self,text):
        data = {'text':text}
        return data
    def writeFile(self,file, content):
        with open(file, 'wb') as f:
            f.write(content)
        f.close()    
    def tts(self,text):
        r = requests.post(self.__ttsUrl,headers=self.getHeader(),data=self.getBody(text))
        contentType = r.headers['Content-Type']
        if contentType == "audio/mpeg":
            sid = r.headers['sid']
            if self.aue == "raw":
                self.writeFile("audio/MHZZ.wav", r.content)
            else :
                self.writeFile("audio/MHZZ.mp3", r.content)
        else :
            print r.text  
			
class MHStream():
    def __init__(self,channels=1,rate = 16000,record_seconds=5):
        self.chunk=1024
        self.format = pyaudio.paInt16
        self.channels = channels
        self.rate = rate
        self.record_seconds = record_seconds
		
    def waveRecord(self,output_file_name="record/MHZZ.wav"):
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

    def wavePlay(self,input_file_name="audio/MHZZ.wav"):
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
		
def speechParser(b):
    c=""
    if b["code"]=="00000":
        if b["data"]: 
            if b["data"]["rc"] ==0:
                c=b["data"]["answer"]["text"]
                return c
            else:
                c="这个问题太难了，请换一个简单一点的！"
                return c
        else:
            c="请求信息为空，再试一遍"
            return c 
    else:
        c="请求错误"
        return c
if __name__=="__main__":
    myAppid="5ab0c49c"
    myasrKey="95eb9dcf1f1943eb8ea8dd1a829bee49"
    myttsKey="65d40c89696e67f0547d7f7e4c3f7c87"
	
    sxy=MH_TTS(myAppid,myttsKey)
    lj=MH_ASR(myAppid,myasrKey)

    #qiu=MHStream()
    #qiu.waveRecord()
    #b=lj.speech("record/MHZZ.wav","2")      #语音语义识别
    #te=speechParser(b)
    sxy.tts("一百")
    #qiu.wavePlay()
	
    
                                  #合成
                              #播放
	
  
	
	
