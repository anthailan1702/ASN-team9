# -*- coding: utf-8 -*-

import json
from math import *
import time

import httplib2
import bluetooth


def get_required_data(): # get the temperature and humidity data required from the client
	
	# from client
	temp = 23
	humi = 29
	return temp, humi
	



def main():
    #temp, humi = get_required_data()
    bd_addr = "00:17:E9:F8:72:06" # EV3 Bluetooth Address
    port = 1
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    h = httplib2.Http()
    while(1):
        try:
            sock.connect((bd_addr, port))
            break
        except:
            continue

    while True:
        if sock.recv(1).decode('utf-8') == 't':
            temp1 = sock.recv(5).decode('utf-8')
            humi1 = sock.recv(5).decode('utf-8')
            temp2 = sock.recv(5).decode('utf-8')
            humi2 = sock.recv(5).decode('utf-8')
            warehouse_num = sock.recv(1).decode('utf-8')
            sock.send('g')
            # send these data by http
            change_information = h.request(
                uri='http://api.asnteam09.tk/warehouses',
                method='PUT',
                headers={
                    'Content-Type': 'application/json',
                },
                body=json.dumps({
                    'temp_1': temp1,
                    'temp_2': temp2,
                    'humi_1': humi1,
                    'humi_2': humi2,
                    'warehouse_num': warehouse_num
                })
            )

            print("get tempeture and humidity data")
        break
    while True:
        if sock.recv(1024).decode('utf-8') == 'r': # if receive 'r', means robot ready to go
            print("ok")
            sock.send('r') # send 'r' to tell robot it's ok
            send_ready_request = h.request(
                uri='http://api.asnteam09.tk/robots',
                method='PUT',
                headers={
                    'Content-Type': 'application/json',
                },
                body=json.dumps({
                    'status': 'Ready'
                })
            )
            break

    while True:
        count = sock.recv(1024).decode('utf-8')
        if count == 's': # if receive 's', means robot stop
            send_finish_request = h.request(
                uri='http://api.asnteam09.tk/robots',
                method='PUT',
                headers={
                    'Content-Type': 'application/json',
                },
                body=json.dumps({
                    'status': 'Finish'
                })
            )
            break
        else:
            change_position = h.request(
                uri='http://api.asnteam09.tk/locations',
                method='POST',
                headers={
                    'Content-Type': 'application/json',
                },
                body=json.dumps({
                    'location_id': int(count),
                })
            )

    sock.close()
        

if __name__ == '__main__':
    main()
