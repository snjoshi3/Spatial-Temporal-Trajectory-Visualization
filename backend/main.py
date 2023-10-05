import json
import numpy as np
from flask import Flask, redirect, url_for, request, send_from_directory
import os
import glob
import shutil
import os.path
import time
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()

origins = [
    "*",
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(common.router)
# app.include_router(video.router)
# # app.include_router(rois.router)
# # app.include_router(machines.router)
# app.include_router(sensors.router)
# app.include_router(signals.router)
# app.include_router(sensor_mappings.router)
# app.include_router(help.router)

requiredFilePath = ""

def load_data_fn(file_path="simulated_trajectories.json"):
    # command = f'''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar {file_path}'''
    # process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    if len(requiredFilePath) > 0 :
        file_path = requiredFilePath

    with open(file_path,"r") as file:
        data = json.load(file)
    data_2 = []

    global_data = {}

    lat_lon_array = []
    timestamp_list = []


    for ele in data:
        temp_dict = {}
        temp_dict['location']=[]
        temp_dict['timestamp']=[]
        for k,v in ele.items():
            # print(k)
            if(k in ['trajectory_id']):
                temp_dict[k] = v
            if(k in ['vehicle_id']):
                temp_dict[k] = v
            if(k in ['trajectory']):
                for list_val in v:
                        temp_dict['location'].append([list_val['location'][1], list_val['location'][0]])
                        lat_lon_array.append([list_val['location'][1], list_val['location'][0]])
                        temp_dict['timestamp'].append(list_val['timestamp'])
                        timestamp_list.append(list_val['timestamp'])
        data_2.append(temp_dict)

    global_data['data'] = data_2  

    lat_lon_array = np.array(lat_lon_array)   
    global_data['center'] = np.mean(lat_lon_array, axis=0).tolist()

    global_data['min_ts'] = min(timestamp_list)
    
    return global_data

def getSpatialRange_fn(latMin, lonMin, latMax, lonMax, file_path="simulated_trajectories.json"):
    command = f'''spark-submit SDSE-Phase-1-assembly-0.1.jar {file_path} D:/sem1/cse594/Project/Final get-spatial-range {latMin} {lonMin} {latMax} {lonMax}'''
    # process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    os.system(command)
    temp_fldr_name = 'D:/sem1/cse594/Project/Final/get-spatial-range/'
    shutil.rmtree(temp_fldr_name, ignore_errors=True)
    print(command)
    # print(process)

    temp_file_path = 'D:/sem1/cse594/Project/Final/get-spatial-range/_SUCCESS'
        # while True:
            # if(os.exists(temp_file_path)):
            #     break
    while not os.path.exists(temp_file_path):
        time.sleep(1)

        # if os.path.isfile(temp_file_path):
        #     print(os.listdir('/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/'))
        # else:
        #     print("No file")

        print(temp_fldr_name, temp_file_path)
        
    req_file_name = ''
    for file_name in glob.glob(temp_fldr_name+'*.json'):
        req_file_name = file_name
            
    result_data = {}
    res_lat_lon_array = []
    li = []
    res_timestamp_list = []
    print(req_file_name)

    with open(req_file_name,"r") as f:
        for line in f:
            temp = json.loads(line)
            temp['location'] = [[x[1],x[0]] for x in temp['location']]
                # print(len(temp['location']))
            res_timestamp_list.extend(temp['timestamp'])
            res_lat_lon_array.extend([[x[0],x[1]] for x in temp['location']])
            li.append(temp)
    print("Hey B")
    result_data['data'] = li
    res_lat_lon_array = np.array(res_lat_lon_array)

    result_data['center'] = np.mean(res_lat_lon_array, axis=0).tolist()

    result_data['min_ts'] = min(res_timestamp_list)
    print("Hey C")
    print(result_data)
    return result_data
    # try:
        # temp_fldr_name = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/'
        # shutil.rmtree(temp_fldr_name, ignore_errors=True)

        # temp_file_path = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/_SUCCESS'
        # # while True:
        #     # if(os.exists(temp_file_path)):
        #     #     break
        # while not os.path.exists(temp_file_path):
        #     time.sleep(1)

        # # if os.path.isfile(temp_file_path):
        # #     print(os.listdir('/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/'))
        # # else:
        # #     print("No file")

        # print(temp_fldr_name, temp_file_path)
        
        # req_file_name = ''
        # for file_name in glob.glob(temp_fldr_name+'*.json'):
        #     req_file_name = file_name
            
        # result_data = {}
        # res_lat_lon_array = []
        # li = []
        # res_timestamp_list = []
        # print(req_file_name)

        # with open(req_file_name,"r") as f:
        #     for line in f:
        #         temp = json.loads(line)
        #         temp['location'] = [[x[1],x[0]] for x in temp['location']]
        #         # print(len(temp['location']))
        #         res_timestamp_list.extend(temp['timestamp'])
        #         res_lat_lon_array.extend([[x[0],x[1]] for x in temp['location']])
        #         li.append(temp)
        # print("Hey B")
        # result_data['data'] = li
        # res_lat_lon_array = np.array(res_lat_lon_array)

        # result_data['center'] = np.mean(res_lat_lon_array, axis=0).tolist()

        # result_data['min_ts'] = min(res_timestamp_list)
        # print("Hey C")
        # return result_data
    # except:
    #     print("pass")
    #     pass





def getSpatioTemporalRange_fn(timeMin, timeMax, latMin, lonMin, latMax, lonMax, file_path="simulated_trajectories.json"):
    command = f'''spark-submit SDSE-Phase-1-assembly-0.1.jar {file_path} D:/sem1/cse594/Project/Final get-spatiotemporal-range {timeMin} {timeMax} {latMin} {lonMin} {latMax} {lonMax}'''
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)

def getKNNTrajectory_fn(trajectoryId, neighbors, file_path="simulated_trajectories.json"):
    command = f'''spark-submit SDSE-Phase-1-assembly-0.1.jar {file_path} D:/sem1/cse594/Project/Final get-knn {trajectoryId} {neighbors}'''
    print(command)
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)


# def func():
#     dict_option = {}
#     dict_option["load_data"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/simulated_trajectories.json'''
#     dict_option["getSpatialRange"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/simulated_trajectories.json /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output get-spatial-range 33.41415667570768 -111.92518396810091 33.414291502635706 -111.92254858414022'''
#     dict_option["getSpatioTemporalRange"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/simulated_trajectories.json /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output get-spatiotemporal-range 1664511371 1664512676 33.41415667570768 -111.92518396810091 33.414291502635706 -111.92254858414022'''
#     dict_option["getKNNTrajectory"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/simulated_trajectories.json /Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output get-knn 0 5'''

class SpatialPayload(BaseModel):
    lat_min:float
    lat_max:float
    lon_min:float
    lon_max:float

class TemporalSpatialPayload(BaseModel):
    min_Time:str
    max_Time:str
    lat_min:float
    lat_max:float
    lon_min:float
    lon_max:float

class KnnPayload(BaseModel):
    trajectory_id:str
    neighbor:str
    
class filePathPayload(BaseModel):
    filePath:str

@app.get("/")
def index():
    print("jello")
    return "Hello"

@app.get("/load_data")
def load_data():
    data = load_data_fn()
    if(data):
        response = {"data":data}
    else:
        response={"message":"Error fetching data!"}
    return response

@app.post("/loadFile")
def loadFile(payload:filePathPayload):
    filesPath = payload.filePath
    print(filesPath)
    global requiredFilePath  
    requiredFilePath = filesPath
    data = load_data_fn(filesPath)
    if(data):
        response = {"data":data}
    else:
        response={"message":"Error fetching data!"}
    return response

@app.post("/spatial_data_query")
async def spatial_range(payload:SpatialPayload):
    # return payload
    print("spatial_data_query")
    # temp_fldr_name = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/'
    # shutil.rmtree(temp_fldr_name, ignore_errors=True)

    data = getSpatialRange_fn(payload.lat_min, payload.lon_min, payload.lat_max, payload.lon_max)

    # if data:
    print("returned")
    return data
    # else:
    #     return data

    # temp_file_path = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/_SUCCESS'
    # while not os.path.exists(temp_file_path):
    #     time.sleep(1)

    # if os.path.isfile(temp_file_path):
    #     print(os.listdir('/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/'))
    # else:
    #     print("No file")

    
    # req_file_name = ''
    # for file_name in glob.glob(temp_fldr_name+'*.json'):
    #     req_file_name = file_name
        
    # result_data = {}
    # res_lat_lon_array = []
    # li = []
    # res_timestamp_list = []
    # # print(req_file_name)

    # with open(req_file_name,"r") as f:
    #     for line in f:
    #         temp = json.loads(line)
    #         temp['location'] = [[x[1],x[0]] for x in temp['location']]
    #         # print(len(temp['location']))
    #         res_timestamp_list.extend(temp['timestamp'])
    #         res_lat_lon_array.extend([[x[0],x[1]] for x in temp['location']])
    #         li.append(temp)
            
    # result_data['data'] = li
    # res_lat_lon_array = np.array(res_lat_lon_array)

    # result_data['center'] = np.mean(res_lat_lon_array, axis=0).tolist()

    # result_data['min_ts'] = min(res_timestamp_list)
    # # print(result_data)

    # return result_data




@app.post("/spatial_data_Temporal_query")
def temporal_spatial_range(payload:TemporalSpatialPayload):
    # return payload
    print(payload)
    data = payload
    print(data)

    temp_fldr_name = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatiotemporal-range/'
    shutil.rmtree(temp_fldr_name, ignore_errors=True)

    getSpatioTemporalRange_fn(payload.min_Time, payload.max_Time, payload.lat_min, payload.lon_min, payload.lat_max, payload.lon_max)

    temp_file_path = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatiotemporal-range/_SUCCESS'
    while not os.path.exists(temp_file_path):
        time.sleep(1)

    # if os.path.isfile(temp_file_path):
    #     print(os.listdir('/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/'))
    # else:
    #     print("No file")

    
    req_file_name = ''
    for file_name in glob.glob(temp_fldr_name+'*.json'):
        req_file_name = file_name
        
    result_data = {}
    res_lat_lon_array = []
    li = []
    res_timestamp_list = []
    print(req_file_name)

    with open(req_file_name,"r") as f:
        for line in f:
            temp = json.loads(line)
            temp['location'] = [[x[1],x[0]] for x in temp['location']]
            # print(len(temp['location']))
            res_timestamp_list.extend(temp['timestamp'])
            res_lat_lon_array.extend([[x[0],x[1]] for x in temp['location']])
            li.append(temp)
            
    result_data['data'] = li
    res_lat_lon_array = np.array(res_lat_lon_array)

    result_data['center'] = np.mean(res_lat_lon_array, axis=0).tolist()

    result_data['min_ts'] = min(res_timestamp_list)
    print(result_data)

    return result_data


@app.route('/index', methods=['GET'])
def getIndex():
    return send_from_directory('templates', 'index.html') 

@app.post("/spatial_knn_query")
def knn_range(payload:KnnPayload):
    # return payload
    print(payload)
    data = payload
    print(data)

    temp_fldr_name = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-knn/'
    shutil.rmtree(temp_fldr_name, ignore_errors=True)

    getKNNTrajectory_fn(payload.trajectory_id, payload.neighbor)

    temp_file_path = '/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-knn/_SUCCESS'
    while not os.path.exists(temp_file_path):
        time.sleep(1)

    # if os.path.isfile(temp_file_path):
    #     print(os.listdir('/Users/trickster/Downloads/courses/CSE594/debugging/SDSE-Phase-1/data/output/get-spatial-range/'))
    # else:
    #     print("No file")

    
    req_file_name = ''
    for file_name in glob.glob(temp_fldr_name+'*.json'):
        req_file_name = file_name
        
    result_data = {}
    res_lat_lon_array = []
    li = []
    res_timestamp_list = []
    print(req_file_name)

    with open(req_file_name,"r") as f:
        for line in f:
            temp = json.loads(line)
            temp['location'] = [[x[1],x[0]] for x in temp['location']]
            # print(len(temp['location']))
            res_timestamp_list.extend(temp['timestamp'])
            res_lat_lon_array.extend([[x[0],x[1]] for x in temp['location']])
            li.append(temp)
            
    result_data['data'] = li
    res_lat_lon_array = np.array(res_lat_lon_array)

    result_data['center'] = np.mean(res_lat_lon_array, axis=0).tolist()

    result_data['min_ts'] = min(res_timestamp_list)
    print(result_data)

    return result_data

app.mount('/', StaticFiles(directory='frontend',html=True))
# if __name__ == "__main__":
#     pass
#     uvicorn.run(app, host="0.0.0.0", port=8000)