#!/usr/bin/python3

import time
import os
import shutil

from mininet.net import Containernet
from mininet.node import Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, error, setLogLevel
import threading
import pandas as pd

setLogLevel('info')



### Replace
# 1. Replace the "Weekday" with the day of the week (e.g., Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday)
# Weekday = "Sunday"
# 2. Replace the "Week" with the week number (e.g., 01, 02, 03, 04, 05, 06, 07, 08, 09, 10)
# Week = "02"
# 3. Replace the "bdwidth" with the bandwidth value (e.g., 1.0, 2.0, 3.0, 4.0, 5.0)
# bdwidth = 3

# Read the piece values from the file
with open('./pieces.txt', 'r') as f:
    piece = int(f.readline().strip())

# # Now you can use the `pieces` list in your script
# print(piece)




execut = piece
# execut = 15

print("Current piece:", execut)


#-----------------------------------------------


network = Containernet(controller=Controller)



info('*** Adding controller\n')
network.addController('c0')

info('*** Adding docker containers\n')



cwd = os.getcwd()

parms = os.path.join(cwd, "params.csv")

df_params = pd.read_csv(parms)
# print(df_params)

# Filter the dataframe for Exec_nr == 88
filtered_df = df_params[df_params['Exec_nr'] == execut]


# Check if any rows are returned for Exec_nr == 88
if not filtered_df.empty:
    # Get the weekday value for the first row
    Week = str(filtered_df['week'].iloc[0])
    Weekday = str(filtered_df['days'].iloc[0])

    # Assign the value of 'cpu_quota' to cpu_quota_sf
    cpu_quota_sf = int(filtered_df['cpu_quota'].iloc[0])

    # Extract time periods into a dictionary
    time_periods = {
        "time_period_1": filtered_df['time_period_1'].values[0],
        "time_period_2": filtered_df['time_period_2'].values[0],
        "time_period_3": filtered_df['time_period_3'].values[0]
    }

    # Attempt to convert bandwidth to an integer, handle the case where it's not possible
    try:
        bdwidth = int(filtered_df['Bandwidth'].iloc[0])
    except ValueError:
        print("Error: Bandwidth value is not convertible to an integer.")
        bdwidth = None  # or assign a default value if needed

    # print("Corresponding weekday for Exec_nr == 88:", Weekday)
else:
    print("No data found for Exec_nr == 88")




# Construct the day of the week
day = Weekday + "_" + Week


# Specify the directory paths
results_dir = os.path.join(cwd, "results")
date_dir = os.path.join(cwd, "date")

#################
# Specify the directory paths
devs_fig = os.path.join(cwd, "date", day, "devices.csv")

df_devs = pd.read_csv(devs_fig)



# Define cpu_period
cpu_period_sf = int(1000000)



# Calculate cpu_quota and assign it to a new column
df_devs['cpu_quota'] = int(cpu_quota_sf * 0.01 * cpu_period_sf)


df_devs.to_csv(devs_fig, index=False)


# Check if the directories exist before attempting to remove them
if os.path.exists(results_dir):
    shutil.rmtree(results_dir)
    print(f"Directory '{results_dir}' removed successfully.")
else:
    print(f"Directory '{results_dir}' does not exist.")


# Create folders
create_folder = ["entrance", "hall1", "hall2", "hall3", "shop", "rest", "edge", "metaverse"]

for folder in create_folder:
    if not os.path.exists(cwd + "/results/" + folder):
        os.makedirs(cwd + "/results/" + folder)

print("Results directory created successfully.")


##-------Broker-------

brokerDocker = network.addDocker(
	'broker',
	ip='10.0.0.240',
	dimage='emqx-experiments:latest',		
	dcmd="/opt/emqx/bin/emqx foreground",
	ports=[1883, 18083, 8883, 8083, 8084, 8780, 9900],
	port_bindings={1883: 1883, 18083: 18083, 8883: 8883, 8083: 8083, 8084: 8084, 8780: 8780, 9900:9900}
)

entrance = int(df_devs[df_devs['Location'] == 'hall2']['cpu_quota'].iloc[0])
entranceDocker = network.addDocker(
	'entrance',
	ip='10.0.0.241',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/entrance:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=entrance 
)

hall1 = int(df_devs[df_devs['Location'] == 'hall1']['cpu_quota'].iloc[0])
hall1Docker = network.addDocker(
	'hall1',
	ip='10.0.0.242',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/hall1:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=hall1
)

hall2 = int(df_devs[df_devs['Location'] == 'hall2']['cpu_quota'].iloc[0])
hall2Docker = network.addDocker(
	'hall2',
	ip='10.0.0.243',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/hall2:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=hall2
)

hall3 = int(df_devs[df_devs['Location'] == 'hall3']['cpu_quota'].iloc[0])
hall3Docker = network.addDocker(
	'hall3',
	ip='10.0.0.244',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/hall3:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=hall3
)

shop = int(df_devs[df_devs['Location'] == 'shop']['cpu_quota'].iloc[0])
shopDocker = network.addDocker(
	'shop',
	ip='10.0.0.245',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/shop:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=shop
)

rest = int(df_devs[df_devs['Location'] == 'rest']['cpu_quota'].iloc[0])
restDocker = network.addDocker(
	'rest',
	ip='10.0.0.246',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/rest:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=rest
)

edge = int(df_devs[df_devs['Location'] == 'edge']['cpu_quota'].iloc[0])
edgeDocker = network.addDocker(
	'edge',
	ip='10.0.0.247',
	dimage="location:latest",
	ports=[1883, 9900],	
	volumes=[cwd + "/deployments/edge:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],			
	ports_binding={1883: 1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=edge
)

metaverse = int(df_devs[df_devs['Location'] == 'metaverse']['cpu_quota'].iloc[0])
metaverseDocker = network.addDocker(
	'metaverse',
	ip='10.0.0.248',		
	dimage="location:latest",
	ports=[1883, 9900],
	volumes=[cwd + "/deployments/metaverse:/mnt/deployment:rw", cwd + "/results:/mnt/results:rw"],
	ports_binding={1883:1883, 9900:9900},
    cpu_period=cpu_period_sf, cpu_quota=metaverse
)





info('*** Adding switches\n')
edgeSwitch = network.addSwitch('s7')
metaverseSwitch = network.addSwitch('s8')
brokerSwitch = network.addSwitch('s9')

info('*** Creating links\n')
##Connecting hosts to switches
network.addLink(edgeDocker, edgeSwitch)
network.addLink(metaverseDocker, metaverseSwitch)
network.addLink(brokerDocker, brokerSwitch)



network.addLink(brokerDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(entranceDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall1Docker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall2Docker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall3Docker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(shopDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(restDocker, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(edgeSwitch, brokerSwitch, cls=TCLink, bw=bdwidth)
network.addLink(metaverseSwitch, brokerSwitch, cls=TCLink, bw=bdwidth)


##Connecting switches to edge switch
# network.addLink(entranceDocker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(hall1Docker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(hall2Docker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(hall3Docker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(shopDocker, edgeSwitch, cls=TCLink, bw=2.0)
# network.addLink(restDocker, edgeSwitch, cls=TCLink, bw=2.0)


##Connecting switches to metaverse switch

network.addLink(entranceDocker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall1Docker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall2Docker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(hall3Docker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(shopDocker, metaverseSwitch, cls=TCLink, bw=bdwidth)
network.addLink(restDocker, metaverseSwitch, cls=TCLink, bw=bdwidth)


info('*** Starting network\n')
network.start()

info('*** Testing connectivity\n')
network.pingAll([])

info('*** Setting up experiment \n')

time.sleep(2)

info('\n*** Launching "entrance" Docker... \n')
entranceDocker.cmd('java -jar location.jar entrance&')

info('\n*** Launching "hall-1" Docker... \n')
hall1Docker.cmd('java -jar location.jar hall1 &')

info('\n*** Launching "hall-2" Docker... \n')
hall2Docker.cmd('java -jar location.jar hall2 &')

info('\n*** Launching "hall-3" Docker... \n')
hall3Docker.cmd('java -jar location.jar hall3 &')

info('\n*** Launching "shop" Docker... \n')
shopDocker.cmd('java -jar location.jar shop &')

info('\n*** Launching "rest" Docker... \n')
restDocker.cmd('java -jar location.jar rest &')

info('\n*** Launching "edge" Docker... \n')
edgeDocker.cmd('java -jar location.jar edge &')

info('\n*** Launching "metaverse" Docker... \n')
metaverseDocker.cmd('java -jar location.jar metaverse&')

info('\n*** Starting network \n')
# info('*** Running CLI\n')
# CLI(network)

time.sleep(100)

# Send "exit" command to the CLI
# os.system('echo "exit" | mn -c')


info('*** Stopping network')
network.stop()


# #### Comment-out if making historical data for CD
raw_path = os.path.join(cwd, "rawdata")

if os.path.exists(raw_path):
    shutil.rmtree(raw_path)
    print(f"Directory '{raw_path}' removed successfully.")
else:
    print(f"Directory '{raw_path}' does not exist.")


os.makedirs(raw_path, exist_ok=True)


day_dir = os.path.join(date_dir, day)

# Move the directory to the new path
save_path = os.path.join(cwd, "date", day)
new_path = os.path.join(cwd, "results", day)
shutil.move(day_dir, new_path)

print(f"Directory moved successfully from {day_dir} to {new_path}")



# Construct the archive name without adding a "/" at the beginning
archive_name = day + "_" + str(bdwidth) + "_" + str(cpu_quota_sf)

zip_file_path = os.path.join(cwd, archive_name)

# After the process, zip the created diexitrectories
shutil.make_archive(zip_file_path, 'zip', os.path.join(cwd, "results"))


zip_destination = os.path.join(raw_path, archive_name + ".zip")

# Remove the existing zip file if it exists
if os.path.exists(zip_destination):
    os.remove(zip_destination)

# Move the zip archive to the rawdata directory
shutil.move(zip_file_path + ".zip", raw_path)
print(f"Zip archive moved successfully to {raw_path}")

