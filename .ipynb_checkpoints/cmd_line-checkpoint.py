import subprocess

command = '''/Users/amritbhaskar/Documents/spatial_data_science/spark-3.0.3-bin-hadoop2.7/bin/spark-submit /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/target/scala-2.12/SDSE-Phase-1-assembly-0.1.jar /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/simulated_trajectories.json /Users/amritbhaskar/Documents/spatial_data_science/project/SDSE-Phase-1/data/output get-spatial-range 33.41415667570768 -111.92518396810091 33.414291502635706 -111.92254858414022'''

process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, universal_newlines=True, shell=True)
stdout,stderr = process.communicate()
if process.returncode !=0:
       print(stderr)
print(stdout)
