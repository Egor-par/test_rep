import pyvisa
import pandas as pd
import eel
from random import randint
import json
import sqlite3
import json
from datetime import date
import datetime
import pytz
from numpy.random.mtrand import random
import string
import secrets
import numpy as np

address = "TCPIP0::localhost::5025::SOCKET"

def closest_value(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return arr[i]


class Messager():
    def __init__(self):
        rm = pyvisa.ResourceManager()

        self.res = rm.open_resource(address, timeout=500)
    def query(self, message:str):
        self.res.read_termination = '\n'
        self.res.write_termination = '\n'

        try:
            tmp = self.res.query(message)
            print("{:30}".format("Message: " + message) + "{:>40}".format(" return: " + tmp))
            return tmp
        except pyvisa.errors.VisaIOError:
            print("{:30}".format("Message: " + message) + "{:>40}".format(" not answer"))
            return ''


    def write(self, message: str):
        self.res.read_termination = '\n'
        self.res.write(message)
        print("{:30}".format("Message: " + message))




@eel.expose
def request_caban():
    messager = Messager()
    messager.query("SENS:FREQ:STAR 8 GHz")
    messager.query("SENS:FREQ:STOP 12 GHz")
    tmp = messager.query("CALC1:DATA:FDAT?").split(",")
    tmp_x = messager.query("CALC1:DATA:XAXis?").split(",")
    arr_end = []
    i_q = 1
    for i in tmp:
        if i_q % 2 != 0:
            arr_end.append(i)
            print(i)
        i_q += 1
    print(arr_end)
    print(tmp_x)
    print(min(arr_end))
    return {'x': tmp_x, 'y': arr_end}
    # return json.dumps(' , '.join(map(str, arr_end)))


@eel.expose
def ferro_query(method, pharams):
    if(pharams != 0):
        arr_method = json.dumps(pharams)
        nn = json.loads(arr_method)
        list_from_dict = list(zip(nn.keys(), nn.values()))
        arr_data = {}
        for i in list_from_dict:
            arr_data[i[0]] = i[1]
        print(arr_data)

    match method:
        case 'new_create':
            key = secrets.token_urlsafe(16)
            print('Create method')
            current_time = datetime.datetime.now(pytz.timezone('Europe/Samara'))
            match arr_data['method']:
                case '1':
                    name = 'МФЧ'
                    subtitle = 'Исследование по методу фиксированной частоты.'
                case '2':
                    name = 'МФД'
                    subtitle = 'Исследование по методу фиксированной длины.'
                    arr_data_metod = arr_data
                case '3':
                    name = 'СО'
                    subtitle = 'Исследование по методу стержневых образцов.'
                case '4':
                    name = 'СВЧФ'
                    subtitle = 'Исследование по методу СВЧ ферритов.'
                case _:
                    name_method = ''

            name_method = name + '_' + str(randint(1, 30)) + '_' + str(current_time.day) + str(current_time.month) + str(current_time.year)
            answer = {'id': key, 'title': name_method, 'subtitle': subtitle}
            date = str(current_time.day) + '-' + str(current_time.month) +'-'+ str(current_time.year)
            time = str(current_time.hour) + ':' + str(current_time.minute)

            data = request_caban()
            arr_end = data['y'][:500]
            float_list = [float(i) for i in arr_end]
            index_res = float_list.index(min(float_list))
            f0 = data['x'][index_res]
            f1 = data['x'][float_list.index(closest_value(float_list[(index_res-50):index_res], (min(float_list) + 3)))]
            f2 = data['x'][float_list.index(closest_value(float_list[index_res:index_res+50], (min(float_list) + 3)))]
            A0 = min(float_list)
            AE = 0

            data_file = {'data_param': arr_data_metod, 'f0': f0,'f1': f1,'f2': f2, 'A0': A0, 'AE': AE,'date': date, 'time': time, 'x': data['x'], 'y_res':  data['y'],'y_samples': [] }
            print(data_file)

            f = open('data_ferro/'+key+'.txt', 'w')
            f.write(json.dumps(data_file))
            f.close()

            return json.dumps(answer)
        case 'new_sample':
            id_file = pharams
            data = request_caban()
            arr_end = data['y'][:500]
            float_list = [float(i) for i in arr_end]
            index_res = float_list.index(min(float_list))
            fe = data['x'][index_res]
            AE = min(float_list)
            f = open(id_file, 'r+')

        case 'create_graph':
            data = request_caban()
            return json.dumps(' , '.join(map(str, data['y'])))
        case _:
            print('Неизвестный метод.')


eel.init("ferro_web_v1")
eel.start("home.html", mode='brave', size=(1920,1080),  cmdline_args=[ '--start-fullscreen'])
