import os, time, scratchconnect
from mcstatus import MinecraftServer
from dotenv import load_dotenv
from random import randint

load_dotenv()

username = os.environ['USERNAME']
password = os.environ['PASSWORD']

user = scratchconnect.ScratchConnect(username, password)
project = user.connect_project(project_id=601861832, access_unshared=True)
variables = project.connect_cloud_variables()

def lookup(server_ip):
    try:
        server = MinecraftServer.lookup(server_ip)
        status = server.status()
        query = server.query()
    
        return randint(0, 10000), server.host, "{0}/{1}".format(status.players.online, status.players.max), status.version.name, status.latency, query.motd, query.players.names
    except:
        try:
            server = MinecraftServer.lookup(server_ip)
            status = server.status()
            
            return randint(0, 10000), server.host, "{0}/{1}".format(status.players.online, status.players.max), status.version.name, status.latency
        except:
            return "Error"

event = variables.start_event(update_time=5)  # Start a cloud event loop to check events. Use the 'update_time' parameter to wait for that number of seconds and then update the data.

@variables.event.on('change')
def do_something(**data):
    print(data['variable_name'])
    variables = project.connect_cloud_variables()
    if data['variable_name'] == '☁ request':
        server_ip = variables.decode(data['value'])
        response = lookup(server_ip)
        if response == "Error":
            variables.set_cloud_variable(variable_name="response", value=404)
            print("Response error sent")
        else:
            set = variables.set_cloud_variable(variable_name="response", value=variables.encode_list(list(response)))
            if set:
                print("Response sent!")
