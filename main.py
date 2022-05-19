#self-hosting guide: https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f
#updated to use scratchcloud

from scratchcloud import CloudClient, CloudChange
import scEncoder
import os, time, json
from mcstatus import JavaServer
from dotenv import load_dotenv
from random import randint

#get .env passcodes
load_dotenv()
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

client = CloudClient(username=username, project_id='690926913')
encoder = scEncoder.Encoder()
chars = scEncoder.ALL_CHARS

def lookup(server_ip):
    try:
        server = JavaServer(server_ip)
        status = server.status()
        #query = server.query()

        modt = status.description
        print(modt)
        description = ''.join([i for i in modt if i in chars])
        print(description)

        raw = status.raw
        rawjson = json.dumps(raw)
        rawdata = json.loads(str(rawjson))

        players = []
        for name in rawdata['players']['sample']:
            print(name['name'])
            players.append(name['name'])
        print(players)
        players1 = players[0:6]
        playersample=' '.join([str(item) for item in players1])
        print(playersample)
    
        return randint(0, 10000), server_ip, "{0}/{1}".format(status.players.online, status.players.max), status.version.name, status.latency, description, playersample
    except:
        try:
            server = JavaServer(server_ip)
            status = server.status()

            return randint(0, 10000), server_ip, "{0}/{1}".format(status.players.online, status.players.max), status.version.name, status.latency
        except:
            return "Error"

@client.event
async def on_connect():
  print('Project connected.')

@client.event
async def on_disconnect():
  print('Project disconnected!')

@client.cloud_event('REQUEST')
async def on_request(var: CloudChange):
  print(f'The {var.name} variable was changed to {var.value}!')
  server_ip = encoder.decode(var.value)
  response = lookup(server_ip)

  if response == "Error":
    await client.set_cloud('RESPONSE', '400')
    print("Error response sent")
    await client.set_cloud('REQUEST', '400')

  else:
    print(response) #response object needs to be sent in two pieces to avoid scratch cloud character limit
    print(encoder.encode_list(list(response)))
    await client.set_cloud('RESPONSE', encoder.encode_list(list(response[0:5])))
    await client.set_cloud('modt', encoder.encode(response[5]))
    await client.set_cloud('playersample', encoder.encode(response[6]))
    await client.set_cloud('REQUEST', '200')

client.run(password)
