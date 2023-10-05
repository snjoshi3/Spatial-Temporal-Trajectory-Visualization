import uvicorn
import json

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
    allow_origins=origins,
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



def load_data_fn(file_path="/Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/simulated_trajectories.json"):
    # command = f'''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar {file_path}'''
    # process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)
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

def getSpatialRange_fn(file_path, latMin, lonMin, latMax, lonMax):
    command = f'''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar {file_path} /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/output get-spatial-range {latMin} {lonMin} {latMax} {lonMax}'''
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)

def getSpatioTemporalRange_fn(file_path, timeMin, timeMax, latMin, lonMin, latMax, lonMax):
    command = f'''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar {file_path} /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/output get-spatiotemporal-range {timeMin} {timeMax} {latMin} {lonMin} {latMax} {lonMax}'''
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)

def getKNNTrajectory_fn(file_path, trajectoryId, neighbors):
    command = f'''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar {file_path} /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/output get-knn {trajectoryId} {neighbors}'''
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)


# def func():
#     dict_option = {}
#     dict_option["load_data"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/simulated_trajectories.json'''
#     dict_option["getSpatialRange"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/simulated_trajectories.json /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/output get-spatial-range 33.41415667570768 -111.92518396810091 33.414291502635706 -111.92254858414022'''
#     dict_option["getSpatioTemporalRange"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/simulated_trajectories.json /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/output get-spatiotemporal-range 1664511371 1664512676 33.41415667570768 -111.92518396810091 33.414291502635706 -111.92254858414022'''
#     dict_option["getKNNTrajectory"] = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/simulated_trajectories.json /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/output get-knn 0 5'''




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

@app.post("/")
def spatial_range(payload):
    data = payload
    print(data)



# if __name__ == "__main__":
#     pass
#     uvicorn.run(app, host="0.0.0.0", port=8000)