from flask import Flask
from config import Config
from azure.iot.device.aio import IoTHubDeviceClient
import asyncio

app = Flask(__name__)
# app.config.from_object(Config)

from app.iothub import measure_temp
import os
import time
import datetime
import json

@app.cli.command("azure")
def run_send():
    asyncio.run(send_to_azure())

async def send_to_azure():
    # Fetch the connection string from an enviornment variable
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
    
    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the device client.
    await device_client.connect()

    data = {"time": str(datetime.datetime.now()), "devices": [{"name": "Raspberry Pi", "sensors": [{"sensor":"CPU Temp", "value": measure_temp()}]}]}
    jsonData = json.dumps(data)
    # Send a single message
    print(str(datetime.datetime.now()) + "    Sending message...")
    await device_client.send_message(jsonData)
    print(str(datetime.datetime.now()) + "    Message successfully sent!")

    # finally, disconnect
    await device_client.disconnect()


# from app import iothub