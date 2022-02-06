import os, time
import scratchconnect
from mcstatus import MinecraftServer
from dotenv import load_dotenv

load_dotenv()

username = os.environ['USERNAME']
password = os.environ['PASSWORD']

user = scratchconnect.ScratchConnect(username, password)
project = user.connect_project(project_id=601861832)
variables = project.connect_cloud_variables()

def lookup(server_ip):
    server = MinecraftServer.lookup(server_ip)
    status = server.status()
    #query = server.query()
    
    return status.players.online

#lookup('mc.hypixel.net')

while True:
    request = variables.get_cloud_variable_value(variable_name="request", limit=1)  # Returns the cloud variable value
    server_ip = variables.decode(request[0]) #decode first item on the list response
    print(server_ip)
    print(lookup(server_ip))
    # Program to set cloud variables:
    #set = variables.set_cloud_variable(variable_name="Name", value=123)  # Set a Cloud Variable
    time.sleep(5)
