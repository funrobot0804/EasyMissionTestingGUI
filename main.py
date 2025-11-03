from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import glob
import re
from datetime import datetime
from typing import List

import requests
import json
import sys

import zlib
import numpy as np
from base64 import b64encode

import time
import threading
import random

import csv
import copy

import math
import traceback


FMS_server_web="http://127.0.0.1:6600"
#FMS_server_web="http://172.16.57.35:6600"
printlogfile="log/Print"+str(time.time())+".log"
printlogfiletime=time.time()

session = requests.Session()

def Print(*d):
    global printlogfile
    global printlogfiletime
    if time.time()-printlogfiletime>60*60*24:
        printlogfile="log/Print"+str(time.time())+".log"
        printlogfiletime=time.time()
    #print(*d)
    #f=open(printlogfile, "a",encoding="utf-8")
    #Print(time.time(),file=f)
    #Print(*d,file=f)
    #f.flush()
    #f.close()

def Split(L,f=lambda x,y:x==y):
    if len(L)==0:
        return L
    l=[[L[0]]]
    for x in L[1:]:
        if f(l[-1][-1],x):
            l[-1].extend([x])
        else:
            l.extend([[x]])
    return l

def Flatten(L,d=9999):
    if type(L)!=list:
        return L
    if d<=0:
        return L
    l=[]
    for x in L:
        if type(x)==list:
            l.extend(Flatten(x,d-1))
        else:
            l.extend([x])
    return l

def Select(L,f):
    if type(L)==np.ndarray:
        return L[[x for x in range(len(L)) if f(L[x])]]
    return [x for x in L if f(x)]


def GetTarget():
    url = FMS_server_web+"/get_target"
    payload = {
                "option":"all",   # "name" - 回傳 '給定名稱' 的充電站狀態
                                  # "all"  - 回傳 '全部' 的充電站狀態                       
                }
    for _ in range(100000000000000000000):
        try:
            r = session.post(url, data=json.dumps(payload), timeout=5)  
            break
        except:
            time.sleep(0.1)
  

    # 回傳的字串
    #Print(r.text)

    # 如果POST的JSON格式沒有錯誤，其指令回傳為JSON資料格式
    # 若不是，則上面的輸入格式有誤 
    try:
        json_data = r.json()  
        
        result = json_data['result']
        Print("result=", result)
        Print("----------")
        
        value = json_data['value']
        Print("value=", value)
        Print("----------")
        return result,value
        '''
        回傳資料格式
        {
            'result':'success',          # 會有'success'和'fail'兩字串，'success'代表console端沒錯誤，'fail'代表console端可能有錯誤
            
            'value':{'target':         
                     [
                        [["N435-2",-4.82,23.44,1.58,"1F"],
                         ["N435-1",2.68,23.66,1.6,"1F"],
                         ["N100",-19.08,28.7,-3.14,"1F"],
                         ["N610",-22.24,20.48,0.0,"1F"],
                         ["N300",-10.12,16.84,1.53,"1F"]
                         ] 
                     ] 
                    }
            }        
        '''
        '''   
        result = json_data['result']
        Print("result=", result)
        Print("----------")
        
        Print("dock ==> ")
        Print("----------")
     
        dock_list = json_data['value']['dock']
        for dock in dock_list:
            Print("dock name="   , dock[0]) # 格式為字串(str)
            Print("dock x="      , dock[1]) # 格式為float，地圖座標，單位為m
            Print("dock y="      , dock[2]) # 格式為float，地圖座標，單位為m
            Print("dock a="      , dock[3]) # 格式為float，地圖座標，單位為rad (deg*PI/180)
            Print("dock floor="  , dock[4]) # 格式為str
            Print("==========")

        '''        
    except:                      
        Print("The POST JSON format has error!")             
        return "fail","except error"



def GetDock():
    url = FMS_server_web+"/get_dock"
    payload = {
                "option":"all",   # "name" - 回傳 '給定名稱' 的充電站狀態
                                  # "all"  - 回傳 '全部' 的充電站狀態                       
                }
    for _ in range(100000000000000000000):
        try:
            r = session.post(url, data=json.dumps(payload), timeout=5)  
            break
        except:
            time.sleep(0.1)
  

    # 回傳的字串
    #Print(r.text)

    # 如果POST的JSON格式沒有錯誤，其指令回傳為JSON資料格式
    # 若不是，則上面的輸入格式有誤 
    try:
        json_data = r.json()  
        
        result = json_data['result']
        Print("result=", result)
        Print("----------")
        
        value = json_data['value']
        Print("value=", value)
        Print("----------")
        return result,value
        '''
        回傳資料格式
        {
            'result':'success',          # 會有'success'和'fail'兩字串，'success'代表console端沒錯誤，'fail'代表console端可能有錯誤
            
            'value':{'dock':         
                     [
                        [
                         ["dock_0",-6.16,6.8,-0.0,"1F"]
                         ] 
                     ] 
                    }
            }        
        '''
        '''   
        result = json_data['result']
        Print("result=", result)
        Print("----------")
        
        Print("dock ==> ")
        Print("----------")
     
        dock_list = json_data['value']['dock']
        for dock in dock_list:
            Print("dock name="   , dock[0]) # 格式為字串(str)
            Print("dock x="      , dock[1]) # 格式為float，地圖座標，單位為m
            Print("dock y="      , dock[2]) # 格式為float，地圖座標，單位為m
            Print("dock a="      , dock[3]) # 格式為float，地圖座標，單位為rad (deg*PI/180)
            Print("dock floor="  , dock[4]) # 格式為str
            Print("==========")

        '''        
    except:                      
        Print("The POST JSON format has error!")             
        return "fail","except error"


def GetAMR(_amr=""):
    amr=_amr
    if amr=="":
        amr="all"
    url = FMS_server_web+"/get_agv"
    payload = {
            "option": ("all" if amr=="" else "name"),   # "name" - 回傳 '給定名稱' 的AGV狀態
                              # "all"  - 回傳 '全部' 的AGV狀態 
                                    
            "agv_name": amr  # 如果option是"all"，則忽略此項目；是"name"，則選擇給定的AGV name            
            
            }
    for _ in range(100000000000000000000):
        try:
            r = session.post(url, data=json.dumps(payload), timeout=5)  
            break
        except:
            time.sleep(0.1)

    # 回傳的字串
    #Print(r.text)

    # 如果POST的JSON格式沒有錯誤，其指令回傳為JSON資料格式
    # 若不是，則上面的輸入格式有誤 
    try:
        json_data = r.json()  
    
        '''
        回傳資料格式
        {
            'result':'success',          # 會有'success'和'fail'兩字串，'success'代表console端沒錯誤，'fail'代表console端可能有錯誤
        
            'value':{'agv':         
                     [
                        ["Simulator_104",-19.082,28.441,-1.134,"1F",80,"running", 26, 3, 0, 3, "end,standby", 1, "172.16.114.141", 935488, 5, 0] 
                     ] 
                    }
            }        
        '''
    
        #result = json_data['result']
        #Print("result=", result)
        #Print("----------")
        #
        #Print("agv ==> ")
        #Print("----------")
        return json_data['result'],json_data['value']
 
        '''
        agv_list = json_data['value']['agv']
        for agv in agv_list:
            Print("agv name="           , agv[0])  # 格式為字串(str)
            Print("agv x(unit:m)="      , agv[1])  # 格式為float    
            Print("agv y(unit:m)="      , agv[2])  # 格式為float
            Print("agv a(unit:rad)="    , agv[3])  # 格式為float
            Print("agv floor="          , agv[4])  # 格式為字串(str)
            Print("agv power="          , agv[5])  # 格式為int
            Print("agv task status="    , agv[6])  # 格式為字串(str), 有"standby", "running", "error"三種狀態
            Print("agv volts="          , agv[7])  # 格式為int
            Print("agv ai_status="      , agv[8])  # 格式為int, 詳見AI狀態代碼表
            Print("agv ai_error="       , agv[9])  # 格式為int, 詳見AI狀態代碼表
            Print("agv ai_info="        , agv[10]) # 格式為int, 詳見AI狀態代碼表
            Print("agv ai_name="        , agv[11]) # 格式為字串(str)
            Print("agv charging="       , agv[12]) # 格式為int, 0跟1, 表示是否有在充電
            Print("agv ip addr="        , agv[13]) # 格式為字串(str)
            Print("agv work time="      , agv[14]) # 格式為int，單位: 秒(seconds)
            Print("agv work distance="  , agv[15]) # 格式為int，單位: 公尺(m)
            Print("agv is UV work="     , agv[16]) # 格式為int，0跟1, 表示UVC是否有在工作
            Print("==========")
        '''
            
    except:                      
        Print("The POST JSON format has error!")             
        return "fail","except error"


def GetMission(category="unfinish"):
    url = FMS_server_web+"/get_mission"
    payload = {
                "category":category,      # "unfinish" - 回傳 '進行中' 或 '預備中' 的 task
                                            # "finish"   - 回傳 '已完成' 或 '未完成但被推到紀錄區' 的 task
                                            # "all"      - 回傳 '全部' 的 task
                                        
                "task_id": -1               # -1         - 回傳全部
                                            # 0,1,2,3... - 回傳指定id的task           
                
                }
    for _ in range(100000000000000000000):
        try:
            r = session.post(url, data=json.dumps(payload), timeout=5)  
            break
        except:
            time.sleep(0.1)
  

    # 回傳的字串
    #Print(r.text)

    # 如果POST的JSON格式沒有錯誤，其指令回傳為JSON資料格式
    # 若不是，則上面的輸入格式有誤 
    try:
        json_data = r.json()  
        
        '''
        回傳資料格式
        {
            'result':'success',          # 會有'success'和'fail'兩字串，'success'代表console端沒錯誤，'fail'代表console端可能有錯誤
            
            'value':{'unfinish':         # 有'unfinish'和'finish'兩種字串，端看當時POST的'category' 
                     [
                        ['3',  '2/2', 'Simulator_104', '1592209639', '60 sec', '[15938,1592209639]', '[-1,-1.0]', '0', '[0 0 0]', "[[-19.1, 28.48, -3.14, '1F'], [-5.04, 3.66, -0.0, '1F']]", 'none', "1F","50","3"], 
                        ['5', '-1/2', 'Simulator_104', '1592209639', '60 sec', '[15938,1592209639]', '[-1,-1.0]', '0', '[0 0 0]', "[[-19.1, 28.48, -3.14, '1F'], [-5.04, 3.66, -0.0, '1F']]", 'none', "2F","40","4"]
                     ] 
                    }
            }
            
            
        task error會回傳以下可能字串:
            "none" => '等待執行'或'執行中'，並未有錯誤發生
            "script error" => 傳到AGV上的task python腳本發生錯誤，發生的原因: 1. AGV上的python安裝有問題、
                                                                              2. AI報錯導致腳本出錯
            "ai error" => 發生的原因: 1.可能有人透過另一個console來操作機器人
                                      2.AGV被插上Joystick，搶走控制權

            "no error" => '正常結束'，過程中沒有出任何錯誤   
            "busy error" => 機器正在忙，無法執行此任務
            "already error" => 之前的錯誤尚未解除，不能執行此任務 (除非POST至'http://127.0.0.1:6601/recover_error'以解除錯誤)   
            "lowbattery error" => 電量不足，不能執行此任務           

        unfinish_mission_list = json_data['value']['unfinish']
        for mission in unfinish_mission_list:
            Print("mission index="     , mission[0]) # 格式為字串(str)
            Print("task step="         , mission[1]) # 格式為字串(str)
            Print("AGV name="          , mission[2]) # 格式為字串(str)
            Print("start time="        , mission[3]) # 格式為字串(str)
            Print("using time="        , mission[4]) # 格式為字串(str)
            Print("booking id & time=" , mission[5]) # 格式為字串(str)
            Print("cancel id & time="  , mission[6]) # 格式為字串(str)
            Print("AGV type="          , mission[7]) # 格式為字串(str)
            Print("AGV mode="          , mission[8]) # 格式為字串(str)
            Print("task array="        , mission[9]) # 格式為字串(str)
            Print("mission error="     , mission[10])# 格式為字串(str)
            Print("start floor="       , mission[11])# 格式為字串(str)
            Print("work time="         , mission[12])# 格式為字串(str)
            Print("work distance="     , mission[13])# 格式為字串(str)
            #Print("mission name="     , mission[14])# 格式為字串(str)
            #Print("mission from="     , mission[15])# 格式為字串(str)
            Print("==========")


        '''
        result = json_data['result']
        Print("result=", result)
        Print("----------")
        
        value = json_data['value']
        Print("value=", value)
        Print("----------")
        return result,value
    except:                      
        Print("The POST JSON format has error!")       
        return "fail","except error"

def SetMission(amr_name,task_arr,userid=0,startTime=None):
    if startTime==None:
        startTime=time.time()
    url = FMS_server_web+"/set_mission"
    payload = { "start_time":float( startTime ),    # 格式為float，西元1970年後所經過的浮點秒數(UTC)         
                "using_time":float(300),              # 格式為float，任務欲使用的浮點秒數
                "userid":int(userid),                  # 格式為int，下命令者的userid
                "robot_type":int(0),                  # 格式為int，欲使用的robot type (垃圾車、送餐車、送衣服車...)
                "robot_mode":[0,0,0],                 # 格式為list，0 => off
                                                      #             1 => on
                                                      # [上UV燈、下UV燈、吸塵器]

                "robot_name": amr_name,            # 格式為str，指定機器的名字，如果有指定就只會挑選特定名稱的機器
                                                      
                # MoveTo_TrafficNetwork指令格式
                #
                # AMR會優先使用指定的眾多鐵軌來當作移動的依據，並指定前往目的地，使用'目的地名稱'
                # 
                # ["MoveTo_TrafficNetwork", [<目的地名稱>,<目的地所在樓層>],<行走方式>]
                # ["MoveTo_TrafficNetwork", [<目的地名稱>,<目的地所在樓層>]]
                #
                # <行走方式> : 可填可不填，
                #              "Path": 使用FollowPath的行走方式 (主動繞開障礙物)
                #              "Rail": 使用FollowRail的行走方式 (等待障礙物消失)
                #

                "task_arr": task_arr
                                                                                
                }
    Print("*****************************************************************")
    Print(payload)
    #return 'success',777
    for _ in range(100000000000000000000):
        try:
            r = session.post(url, data=json.dumps(payload), timeout=5)  
            break
        except:
            time.sleep(0.1)
   
    #time.sleep(2.0) 

    # 回傳的字串
    Print(r.text)

    # 如果POST的JSON格式沒有錯誤，其指令回傳為JSON資料格式
    # 若不是，則上面的輸入格式有誤 
    try:
        json_data = r.json()  
        
        '''
        回傳資料格式
        {
            'result':'success',          # 會有'success'和'fail'兩字串，'success' 代表任務新增成功
                                         #                              'fail'    代表任務新增失敗
                                         # 
                                         #
                                         
            'value': 3                   # 有可能是'數字'或'字串'
                                         # 數字 0,1,2,3... => 指派成功的task id
                                         # 字串 "xxxxx" => 無法指派的原因                                     
                                         #      "task array type error" => task_arr的格式有誤   
                                         #      "task array empty" => task_arr是空的
                                         #      "task start time in past" => 指派任務的時間是在"過去"
                                         #      "taskManager loop dead lock" => console的task manager當了
                                         #      "robot error" => AGV有錯誤，無法指派
                                         #      "reserver overlap" => 指派的任務時間與其他任務重疊，無法指派
                                         #      "no robot" => 無空閒的AGV在指定的時間可以指派       
                
            }                            
            
                     
        '''
        
        result = json_data['result']
        Print("result=", result)
        Print("----------")
        
        value = json_data['value']
        Print("value=", value)
        Print("----------")
        return result,value
        
                
    except:                      
        Print("The POST JSON format has error!")  
        return "fail","except error"

def GetRail():
	url = FMS_server_web+"/get_rail"

	payload = {
				"option":"all",   # "name" - 回傳 '給定名稱' 的軌跡(鐵軌)狀態
								  # "all"  - 回傳 '全部' 的軌跡(鐵軌)狀態                       
				}
	for _ in range(100000000000000000000):
		try:
			r = session.post(url, data=json.dumps(payload), timeout=5)  
			break
		except:
			time.sleep(0.1)

	# 回傳的字串
	#Print(r.text)

	# 如果POST的JSON格式沒有錯誤，其指令回傳為JSON資料格式
	# 若不是，則上面的輸入格式有誤 
	try:
		json_data = r.json()  
		
		'''
		回傳資料格式
		{
			'result':'success',          # 會有'success'和'fail'兩字串，'success'代表console端沒錯誤，'fail'代表console端可能有錯誤
			
			'value':{'rail':         
					 [
						[
						 ["T1",[-4.74,6.48],[-10.66,21.06],507,"1F",[[-4.72,6.48],[-4.71,6.48]...]],
						 ["T2",[-22.22,20.42],[-19.58,28.58],666,"1F",[[-22.22,20.42],[-22.20,20.42]...]]
						] 
					 ] 
					}
			}        
		'''
		
		result = json_data['result']
		#Print("result=", result)
		Print("----------")
		
		Print("rail ==> ")
		Print("----------")
	 
		rail_list = json_data['value']['rail']
		for rail in rail_list:
			Print("rail name="   , rail[0]) # 格式為字串(str)
			Print("rail start="  , rail[1][0], ",", rail[1][1]) # 格式為float，地圖座標，單位為m
			Print("rail end="    , rail[2][0], ",", rail[2][1]) # 格式為float，地圖座標，單位為m
			Print("rail length=" , rail[3]) # 格式為int
			Print("rail floor="  , rail[4]) # 格式為str
			#Print("rail path="   , rail[5]) # 格式為list, [[x0, y0],[x1, y1]...[x99,y99]...]
			Print("==========")

		result = json_data['result']
		Print("result=", result)
		Print("----------")

		value = json_data['value']
		Print("value=", value)
		Print("----------")
		return result,value

				
	except:                      
		Print("The POST JSON format has error!")             
		return "fail","except error"


def GetPath(amr):
	# 取得規劃路線
	url = FMS_server_web+"/get_pathplan"

	payload = { "robot_name": amr        # 必須指定機器人的名稱
				}
	for _ in range(100000000000000000000):
		try:
			r = session.post(url, data=json.dumps(payload), timeout=5)  
			break
		except:
			time.sleep(0.1)

	#Print(r.text)
	try:
		'''
		回傳資料格式
		{
			'result':'success',          # 會有'success'和'fail'兩字串，'success' 代表任務新增成功
										 #                              'fail'    代表任務新增失敗
										 # 
										 #
										 
			'value': [  [-1.33, 3.55], [-1.31, 3.55], [-1.30, 3.55]...]
					 
					 # 一般會回傳 [[x0,y0],[x1,y1],[x2,y2],[x3,y3],[x4,y4]...] (list, 單位:公尺)
					 # 機器沒在動時，回傳 [] (list)
					 #
					 #
					 # 發生錯誤，回傳字串(str)                 
					 # 錯誤字串: "TaskManager not support (version<=1.0)" (派車版本不支援)
					 #           "Found no robot" (找不到機器人)
			}                            
			
					 
		'''

		json_data = r.json()
		#Print("json_data['value']=")
		#Print(json_data['value'])

		result = json_data['result']
		#Print("result=", result)
		#Print("----------")

		value = json_data['value']
		#Print("value=", value)
		#Print("----------")
		return result,value


	except:                      
		Print("The POST JSON format has error!")  
		return "fail","except error"


######################################################
def FindPointTargetName(xy,mapname=""):
    for t in alltarget:
        if mapname!="":
            if t[4]!=mapname:
                continue
        if (t[1]-xy[0])**2+(t[2]-xy[1])**2<0.2**2:
            return t[0]
    return ""

def FindTargetPoint(targetname,mapname=""):
    for t in alltarget:
        if mapname!="":
            if t[4]!=mapname:
                continue
        if t[0]==targetname:
            return [t[1],t[2],t[3]]
    return [0.,0.,0.]

def FindRailPath(railname,mapname):
    for r in allrail:
        if (r[0]==railname)&(r[4]==mapname):
            return r[5]
    return []

for i in range(999999):
    try:
        alltarget=GetTarget()[1]['target']
        allrail=GetRail()[1]['rail']
        break
    except: 
        time.sleep(1)
        Print("GetTarget or GetRail failure")



app = FastAPI()
templates = Jinja2Templates(directory="templates")
MISSION_DIR = "./missions"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_missions(station):
    missions = []
    for filepath in sorted(glob.glob(os.path.join(MISSION_DIR+(("/"+station) if station!="" else ""), "*.txt"))):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            mission_name=""
            name_match = re.search(r"name:\s*(.+)", content)
            if name_match:
                mission_name = name_match.group(1).strip().split("#")[0].replace(" ","")
            amr_name=""
            name_match = re.search(r"robot:\s*(.+)", content)
            if name_match:
                amr_name = name_match.group(1).strip().split("#")[0].replace(" ","")

            missions.append({
                "name": mission_name,
                "file": filepath, #os.path.basename(filepath)
                "amr": amr_name
            })
    return missions

@app.get("/", response_class=HTMLResponse)
async def index(request: Request, station: str = Query(default="")):
    missions = load_missions(station)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "missions": missions,
        "station": station
    })

class StatusInput(BaseModel):
    strlist: List[str]
    amrlist: List[str]

@app.post("/status")
async def status(input: StatusInput):
    return {"text_list": showtexttest(input.strlist,input.amrlist)}

@app.get("/run")
async def run(file: str):
    filepath = file #os.path.join(MISSION_DIR, file)
    if not os.path.isfile(filepath):
        raise HTTPException(status_code=404, detail="任務檔案不存在")

    #try:
    if 0==0:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        mission_name=""
        name_match = re.search(r"name:\s*(.+)", content)
        if name_match:
            mission_name = name_match.group(1).strip().split("#")[0].replace(" ","")
        amr_name=""
        name_match = re.search(r"robot:\s*(.+)", content)
        if name_match:
            amr_name = name_match.group(1).strip().split("#")[0].replace(" ","")
        tasks_raw = content.split("========", 1)[1].strip().splitlines()
        tasks = [eval(line.strip()) for line in tasks_raw if line.strip()]

        station_name=filepath.replace("\\","/").split("/")[-2]
        station_hash=hash(station_name)%(2**31)
        Print(f"\n✅ station_name: {station_name}    hash={station_hash}")
        Print(f"\n✅ Mission: {mission_name}")
        for task in tasks:
            Print("🔸", task)


        #ret=SetMission(amr_name,tasks,station_hash,time.time())
        ret=SetMission(amr_name,tasks,station_hash,time.time())
        if ret[0]=="success":
            return {"status": "ok", "mission_id": ret[1], "task": str(tasks)}
        else:
            raise HTTPException(status_code=500, detail=str(ret[1]))


        #return {"status": "ok", "mission": mission_name, "task_count": len(tasks)}

    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))

stupidAMRAverageVelocity_data=dict()
def stupidAMRAverageVelocity(amr,v=[]):
    global stupidAMRAverageVelocity_data
    #Print("??????????????????????????????????????????????????????????")
    #Print(stupidAMRAverageVelocity_data)
    if v==[]:
        if amr not in stupidAMRAverageVelocity_data:
            return 1.0
        else:
            if len(stupidAMRAverageVelocity_data[amr][1])>0:
                return np.array(stupidAMRAverageVelocity_data[amr][1]).mean()
            return 1.0
    if type(v)==list:
        if amr not in stupidAMRAverageVelocity_data:
            stupidAMRAverageVelocity_data[amr]=[[time.time(),v],[]]
        else:
            if stupidAMRAverageVelocity_data[amr][0]==[]:
                stupidAMRAverageVelocity_data[amr][0]=[time.time(),v]
            else:
                if time.time()-stupidAMRAverageVelocity_data[amr][0][0]>=10.0:
                    vv=(((v[0]-stupidAMRAverageVelocity_data[amr][0][1][0])**2+(v[1]-stupidAMRAverageVelocity_data[amr][0][1][1])**2)**0.5)/(abs(time.time()-stupidAMRAverageVelocity_data[amr][0][0])+0.00000000001)
                    if (vv>=0.1)&(time.time()-stupidAMRAverageVelocity_data[amr][0][0]<15.0):
                        stupidAMRAverageVelocity_data[amr][1]=(stupidAMRAverageVelocity_data[amr][1]+[vv])[-100:]
                    stupidAMRAverageVelocity_data[amr][0]=[time.time(),v]
                    return vv
        return v
    if v>=0.1:
        if amr not in stupidAMRAverageVelocity_data:
            stupidAMRAverageVelocity_data[amr]=[[],[v]]
        else:
            stupidAMRAverageVelocity_data[amr][1]=(stupidAMRAverageVelocity_data[amr][1]+[v])[-100:]
    return v


def showtexttest(strlist: List[str],amrlist: List[str]) -> (List[str],List[str]):
  try:
    now = datetime.now().strftime('%H:%M:%S')
    #print("GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG",now)
    station_name = strlist[0]# if len(strlist) > 0 else "Unknown"
    buttons = strlist[1:]
    #buttons = amrlist
    #result = [f"[{now}] Station: {station_name}, 任務數: {len(buttons)}"]
    #result=[str(GetMission("unfinish"))]
    #result=[str(GetTarget())]

    getmission=GetMission("unfinish")
    if getmission[0]!="success":
        result=copy.deepcopy(strlist)
        result[0]="ERROR from FMS:"+str(getmission[1])
        return result

    mlist=getmission[1]["unfinish"]
    mlistsort=[[float(m[3]),int(m[0]),i,m] for i,m in enumerate(mlist)]
    mlistsort.sort()
    mlist=[mm for t,index,i,mm in mlistsort]
    Print(mlist)
    #analze show mission
    station_hash=hash(station_name)%(2**31)
    result=[""]
    amrq=dict()
    for i,m in enumerate(mlist):
        #result=[""]
        #if eval(m[5])[0]==station_hash:
        #    result[0]=result[0]+str(m)+"\n\n"

        sm=Split(eval(m[9]),lambda x1,x2:x1[0]!="ButtonWait")
        mi=-1
        fromto=[]
        #analyze each submission before "ButtonWait"
        for ssm in sm:
            start="Unknown"
            end=""
            startmi=mi+1
            for task in ssm:
                mi+=1
                if task[0]=="MoveTo_TrafficNetwork":
                    if start=="Unknown":
                        start=""
                    end=task[1][0]
                if task[0]=='DockTo':
                    if start=="Unknown":
                        start=""
                    Print(task)
                    end=task[1][0][:-5]
                if task[0]=='MoveTo':
                    if start=="Unknown":
                        start=""
                    end=task[1][0]
                if (task[0]=='FollowRail')|(task[0]=='FollowPath'):
                    path=FindRailPath(task[1][0],task[1][3])
                    #print("AAAAAAAAAAAAAAAAAAAAAAA",task,len(path))
                    if start=="Unknown":
                        start=FindPointTargetName(path[max((task[1][1] if task[1][1]<len(path) else len(path)-1),0)],task[1][3])
                    Print("task=",task)
                    end=FindPointTargetName(path[(task[1][2] if task[1][2]<len(path) else len(path)-1)],task[1][3])
            fromto+=[[[start,startmi],[end,mi]]]
        #missionname=str([s[0] for s in Split(Select(Flatten(fromto,1),lambda x:(x!="")&(x!="Unknown")))]).replace(","," ==> ").replace("'","")
        #result[0]+="  fromto="+str(fromto)+"   "+"   sm="+str(sm)


        #check this mission should be showed
        missionstep=int(m[1].split("/")[0])
        if missionstep>=1:

            getamr=GetAMR(m[2])
            if getamr[0]!="success":
                result=copy.deepcopy(strlist)
                result[0]="ERROR from FMS:"+str(getamr[1])
                return result

            getamr=getamr[1]['agv']
            stupidAMRAverageVelocity(m[2],[getamr[0][1],getamr[0][2],getamr[0][3]])
            laststeprobotpose=[getamr[0][1],getamr[0][2],getamr[0][3]]

            buttonwaitcount=0
            eta=0.
            edistance=0.

            getpath=GetPath(m[2])
            if getpath[0]!="success":
                result=copy.deepcopy(strlist)
                result[0]="ERROR from FMS:"+str(getpath[1])
                return result

            path=getpath[1]
            if type(path)!=list:
                path=[]
            total_length =0.
            if len(path)>=2:
                points = np.array(path)
                diffs = np.diff(points, axis=0)  # shape: (n-1, 2)
                segment_lengths = np.linalg.norm(diffs, axis=1)
                total_length = np.sum(segment_lengths)
                edistance+=total_length
                eta+=total_length/stupidAMRAverageVelocity(m[2])
                #result[0]+="\nPath  dis:"+str(total_length)+"\n"

            #result[0]+="\n\n step="+m[1]+" path_len="+str(total_length)+" , "+str(len(path))+"\n\n"

            sm=Split(eval(m[9])[missionstep-1:],lambda x1,x2:x1[0]!="ButtonWait")

            #analyze each submission before "ButtonWait"
            mi=missionstep-2
            for ssm in sm:
                start="Unknown"
                end=""
                for task in ssm:
                    mi+=1
                    #result[0]+="\nmi="+str(mi)+str(task)+"\n\n"


                    if task[0]=="ButtonWait":
                        buttonwaitcount+=1
                        #result[0]+="\nbuttonwait mi="+str(mi)+"\n"

                    if task[0]=="MoveTo_TrafficNetwork":
                        if start=="Unknown":
                            start=""
                        end=task[1][0]
                        total_length=((np.array(FindTargetPoint(end,task[1][1])[:2])-np.array(laststeprobotpose[:2]))**2).sum()
                        edistance+=total_length
                        eta+=total_length/stupidAMRAverageVelocity(m[2])+10.0
                        laststeprobotpose=FindTargetPoint(end,task[1][1])
                        #result[0]+="\MoveTo_TrafficNetwork mi="+str(mi)+"   dis:"+str(total_length)+"\n"

                    if task[0]=='DockTo':
                        if start=="Unknown":
                            start=""
                        end=task[1][0][:-5]
                        total_length=1.0
                        edistance+=total_length
                        eta+=total_length/stupidAMRAverageVelocity(m[2])+10.0
                        laststeprobotpose=FindTargetPoint(end,task[1][1])
                        #result[0]+="\nDockTo mi="+str(mi)+"   dis:"+str(total_length)+"\n"
                    if task[0]=='MoveTo':
                        if start=="Unknown":
                            start=""
                        end=task[1][0]
                        total_length=((np.array(FindTargetPoint(end,task[1][1])[:2])-np.array(laststeprobotpose[:2]))**2).sum()
                        edistance+=total_length
                        eta+=total_length/stupidAMRAverageVelocity(m[2])+10.0
                        laststeprobotpose=FindTargetPoint(end,task[1][1])
                        #result[0]+="\nMoveTo mi="+str(mi)+"   dis:"+str(total_length)+"\n"

                    if (task[0]=='FollowRail')|(task[0]=='FollowPath'):
                        path=FindRailPath(task[1][0],task[1][3])
                        if start=="Unknown":
                            start=FindPointTargetName(path[task[1][1]],task[1][3])
                        end=FindPointTargetName(path[(task[1][2] if task[1][2]<len(path) else len(path)-1)],task[1][3])
                        laststeprobotpose=FindTargetPoint(end,task[1][3])
                        #if (mi>missionstep-2+1)|((mi==missionstep-2+1)&(edistance==0.)):
                        if mi>missionstep-2+1:
                            points = np.array(path[task[1][1]:task[1][2]])
                            diffs = np.diff(points, axis=0)  # shape: (n-1, 2)
                            segment_lengths = np.linalg.norm(diffs, axis=1)
                            total_length = np.sum(segment_lengths)
                            edistance+=total_length
                            eta+=total_length/stupidAMRAverageVelocity(m[2])+10.0
                            #result[0]+="task_len="+str(total_length)+"\n"
                            #result[0]+="\nFollow mi="+str(mi)+"   dis:"+str(total_length)+"\n"
                    if (end==station_name)&(station_name!=""):
                    #if end==station_name:
                        break

                if (end==station_name)|(station_name==""):				
                    targetmi=mi
                    #result[0]+="\n\ntargetmi="+str(targetmi)+"\n\n"

                    #missionname=str([s[0] for s in Split(Select(Flatten(fromto,1),lambda x:(x!="")&(x!="Unknown")))]).replace(","," ==> ").replace("'","")
                    showmission=[]
                    for ft in fromto:
                        if ((ft[0][0]=="")|(ft[0][0]=="Unknown"))&(showmission==[]):
                            showmission+=[[">",[ft[0][1],ft[1][1]-1]],[ft[1][0],[ft[1][1],ft[1][1]]]]
                        else:                        					
                            if (showmission[-1][0] if len(showmission)>0 else "")==ft[0][0]:
                                #showmission[-1]=[showmission[-1][0],[showmission[-1][1][0],ft[0][1]]]
                                #showmission[-1]=[showmission[-1][0],[showmission[-1][1][0],ft[0][1]]]
                                pass
                            else:					
                                showmission+=[[">",[(showmission[-1][1][1]+1 if len(showmission)>0 else -1),ft[0][1]-1]]]
                                showmission+=[[ft[0][0],[ft[0][1],ft[0][1]]]]

                            if ft[0][0]!=ft[1][0]:
                                #showmission+=[[">",[ft[0][1],ft[1][1]-1]]]
                                showmission+=[[">",[(showmission[-1][1][1]+1 if len(showmission)>0 else -1),ft[1][1]-1]]]
                                showmission+=[[ft[1][0],[ft[1][1],ft[1][1]]]]
                            else:
                                showmission[-1]=[showmission[-1][0],[showmission[-1][1][0],ft[1][1]]]





                        '''					
                        if ((ft[0][0]=="")|(ft[0][0]=="Unknown"))&(showmission==[]):
                            showmission+=[[">",[ft[0][1],ft[1][1]-1]]]
                        else:
                            if (showmission[-1][0] if len(showmission)>0 else "")==ft[1][0]:
                                showmission[-1]=[showmission[-1][0],[showmission[-1][1][0],ft[1][1]]]
                            elif len(showmission)>0:
                                #if showmission[-1][0]!=ft[1][0]:
                                #    showmission+=[[ft[1][0],[ft[1][1],ft[1][1]]]]
                                pass
                            else:
                                showmission+=[[ft[0][0],[-1,-1]]]
                            if ft[0][0]!=ft[1][0]:
                                showmission+=[[">",[ft[0][1],ft[1][1]-1]]]
                                showmission+=[[ft[1][0],[ft[1][1],ft[1][1]]]]
                        '''

                    #result[0]+="\n\n"+str(fromto)+"\n\n"

                    #result[0]+="\n\n"+str(showmission)+"\n\n"

                    #result[0]+="\n\n"+str(m)+"\n\n"



                    missionname=""
                    
                    for sm in showmission:
                        if sm[0]==">":
                            if (sm[1][0]<=missionstep-1)&(missionstep-1<=sm[1][1]):
                                #flush
                                missionname+=(">>>"[:int(time.time())%3+1]+"---")[:3]+" "
                            elif missionstep-1<sm[1][0]:
                                missionname+="==>"+" "
                            else:
                                missionname+="---"+" "
                            if (sm[1][0]<=targetmi)&(targetmi<=sm[1][1]):
                                targetmi=sm[1][1]+1
                        else:
                            if (sm[1][0]<=targetmi)&(targetmi<=sm[1][1]):
                                #target[
                                missionname+="["
                            if (sm[1][0]<=missionstep-1)&(missionstep-1<=sm[1][1]):
                                #flush
                                missionname+=(sm[0] if int(time.time())%2==0 else "_"*len(sm[0]))
                            else:
                                missionname+=sm[0]
                            if (sm[1][0]<=targetmi)&(targetmi<=sm[1][1]):
                                #target]
                                missionname+="]"
                            missionname+=" "			
                    

					#result[0]+=m[1]+missionname+"dis:"+str(int(edistance*10)/10.)+"m　　eta:"+str(int(eta))+"s"+(" + buttonwait:"+str(buttonwaitcount) if buttonwaitcount>0 else "")+"\n\n"
                    result[0]+=missionname+"\n("+m[2]+")　dis:"+str(int(edistance*10)/10.)+"m"+"　　　ETA:"+str(int(eta))+"s"+(" +buttonwait:"+str(buttonwaitcount) if buttonwaitcount>0 else "")+("　　ERROR:"+str(m[10]) if m[10]!="none" else "")+"\n\n"

                    break

        else:
            if m[2] not in amrq:
                amrq[m[2]]=[]
            if (station_name in [ft[1][0] for ft in fromto])|(station_name==""):
                missionname=str([s[0] for s in Split(Select(Flatten([[ft[0][0],ft[1][0]] for ft in fromto],1),lambda x:(x!="")&(x!="Unknown")))]).replace(","," ==> ").replace("'","").replace("[","{").replace("]","}")
                result[0]+=missionname+"\n("+m[2]+")　　　queue:"+str(len(amrq[m[2]]))+"\n\n"



        if m[2] in amrq:
            amrq[m[2]]+=[i]
        else:
            amrq[m[2]]=[i]

    #analyze each button queueN
    for i, name in enumerate(buttons):
        qn=0
        amr=amrlist[i]
        for i,m in enumerate(mlist):
            if amr=="":
                if int(m[1].split("/")[0])<0:
                    qn+=1
            else:
                if m[2]==amr:
                    qn+=1

        #result.append(f"[{now}] 按鈕{i+1}: {name}")
        #result.append(f"{name} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  queue:{qn}")
        result.append(f"{name} 　　　　 queue:{qn}")

    return result
  except Exception as e:
    result=copy.deepcopy(strlist)
    result[0]="ERROR: "+str(e)+"  "+traceback.format_exc()
    return result
