from summit.strategies.base import Transform
from summit.experiment import Experiment
from summit.domain import *
from summit.utils.dataset import DataSet
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import os
import json
import requests
from requests.auth import HTTPBasicAuth
from time import sleep
import socketserver
import socket
from http.server import BaseHTTPRequestHandler
import ftplib
import csv
from fractions import Fraction


class Allylation1(Experiment):
    outputfile = r'XXX' # Absolute path
    IP_HPLC_PC = '146.64.91.153'
    RasPi_start = 'XXX:1880/start'
    RasPi_run_relay = 'XXX:1880/run_relay'
    IP_Control_PC = '146.64.91.245'
    absolute_path = "XXX" # Directory where JSON templates are located
    username = 'XXX'
    password = 'XXX'
    ftp_password = 'XXX'
    

    def __init__(self, noise_level=0, **kwargs):
        domain = self._setup_domain()
        super().__init__(domain)
        self.rng = np.random.default_rng()
        self.noise_level = noise_level

    def _setup_domain(self):
        domain = Domain()

        # Decision variables
        des_1 = "residence time in minutes"
        domain += ContinuousVariable(name="tau", description=des_1, bounds=[4, 30])

        des_2 = "reactor temperature"
        domain += ContinuousVariable(
            name="temperature", description=des_2, bounds=[40, 90]
        )

        des_3 = "equivalence"
        domain += ContinuousVariable(name='eqv', description=des_3, bounds=[1, 1.39])

        # Objectives
        des_5 = "space time yield (g/dm^3/h)"
        domain += ContinuousVariable(
            name="sty",
            description=des_5,
            bounds=[0, 890],
            is_objective=True,
            maximize=True,
        )

        return domain

    def grab_data(self, IP, prod_theoritical_conc):
        # IP is IP address of HPLC PC
        result = None
        while result is None:
            os.chdir('XXX')

            try:
                sleep(0.2)
                # IP address and credentials of HPLC PC
                ftp = ftplib.FTP(IP)
                ftp.login(username, ftp_password)
                # Move to direcotry where HPLC results are stored
                ftp.cwd('/ClosedLoop')

                ### Copy data file
                # Look for most recent directory
                filename = sorted(ftp.nlst(), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]

                # Go into most recent directory
                ftp.cwd(filename)
                hplc_run = filename
                os.chdir('XXX')

                # Grab data from csv titled 'REPORT-SAD04.CSV'
                data_file_name = 'REPORT-SAD04.CSV'
                ftp.retrbinary("RETR " + data_file_name, open(data_file_name, 'wb').write)
                name = str(filename + '_' + data_file_name)
                ftp.retrbinary("RETR " + data_file_name, open(name, 'wb').write)

                ### Close ftp connection
                ftp.quit()

                os.chdir('XXX')

                ### Load data from csv with pandas
                df = pd.read_csv(
                    name,
                    header=None,
                    encoding="utf_16_le"
                )
                df.columns = ['Peak#', 'RetTime', 'Type', 'Width', 'Area', 'Height', 'Area%']

                # Get area of Isovanillin - peak1, RetTime between 1.85 and 2.2 min
                # Get area of Allyl bromide - peak2, RetTime between 3.95 and 4.2 min
                # Get area of product - peak 3, RetTime between 3.4 and 3.92 min

                ### peak1 -> Iso
                peak1 = df[(df['RetTime'].between(1.85, 2.2))]
                ### peak2 -> allyl
                peak2 = df[(df['RetTime'].between(3.95, 4.2))]
                ### peak3 -> Product
                peak3 = df[(df['RetTime'].between(3.4, 3.92))]

                # if no peak found, df is empty, make area = 0
                if peak1.empty:
                    print('No peak was found in selected RetTime range')
                    data = {'Area': [0, 0, 0]}
                    peak1 = pd.DataFrame(data, columns=['Area'])

                if peak2.empty:
                    print('No peak was found in selected RetTime range')
                    data = {'Area': [0, 0, 0]}
                    peak2 = pd.DataFrame(data, columns=['Area'])

                if peak3.empty:
                    print('No peak was found in selected RetTime range')
                    data = {'Area': [0, 0, 0]}
                    peak3 = pd.DataFrame(data, columns=['Area'])

                # Grab peak with largest area. This is to prevent the selection of any very small peak which might be due to a contamination
                peak1_area = peak1['Area'].max()
                peak2_area = peak2['Area'].max()
                peak3_area = peak3['Area'].max()

                print('peak1_area: ' + str(peak1_area))
                print('peak2_area: ' + str(peak2_area))
                print('peak3_area: ' + str(peak3_area))

                dilution_factor = 1
                sample_vol = 0.005

                iso_area = peak1_area

                # Process peak 1 -  Iso compound
                ### y = mx + c  -->  x = (y - c) / m
                m = 17995  # 304.3
                c = 0
                iso_conc = (peak1_area - c) / m
                ### Dilution
                iso_conc = iso_conc * dilution_factor

                ### Process peak 2 - allyl compound
                ### y = mx + c  -->  x = (y - c) / m
                m = 1151.6
                c = 0
                allyl_conc = (peak2_area - c) / m
                ### Dilution
                allyl_conc = allyl_conc * dilution_factor

                # Process peak 3 - Product
                ### y = mx + c  -->  x = (y - c) / m
                m = 20207  # 19618
                c = 0
                prod_conc = (peak3_area - c) / m
                ### Dilution
                prod_conc = prod_conc * dilution_factor

                # Calculate yield of Product based on theoretical conc.
                prod_yld = (prod_conc / prod_theoritical_conc) * 100

                result = iso_conc, allyl_conc, prod_conc, prod_yld, hplc_run
                print('Result:')
                print('iso_conc, allyl_conc, prod_conc, prod_yld, hplc_run')
                print(result)

                if result is None:
                    continue
                return result

            except:
                sleep(20)
                print('Trying to get LC data again...')
                pass

    def _run(self, conditions, **kwargs):
        
        # Check how many experiments have been run
        with open(outputfile, 'r', encoding='UTF8',
                  newline='') as f:
            reader = csv.reader(f, )
            lines = len(list(reader))
            completed_exp = lines / 2

        print('completed_exp')
        print(completed_exp)

        class MyHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path == '/cont':
                    print('from do_POST')
                    # Insert your code here
                if self.path == '/running':
                    print('from do_POST')
                    # Insert your code here
                if self.path == '/run_relay':
                    print('from do_POST')
                self.send_response(200)

        # If number of experiments is divisible by 3, pause and wait for column to be replaced
        # For the script to continue, an http request needs to be sent to /cont
        if completed_exp % 3 == 0:
            print('Need to wait for new column. Send http message to \'/cont\' when ready')
            http = socketserver.TCPServer((IP_Control_PC, 9001), MyHandler)
            http.handle_request()
            print('Continuing the experiment!')

        print('Number of completed experiments: ' + str(completed_exp))

        ### Sequence for reactor run
        file_path_json1 = absolute_path + '\\json1.json'
        with open(file_path_json1) as f:
            Exp_seq = json.load(f)

        ### Sequence for changing valves to solvent lines
        solv_chg_path = absolute_path + '\\json1-solv_chg.json'
        print(solv_chg_path)
        with open(solv_chg_path) as f:
            Solv_chg = json.load(f)

        ### Sequence for reactor clean up
        file_path_json1_CleanUp = absolute_path + '\\json1_CleanUp.json'
        # print(file_path_json1_CleanUp)
        with open(file_path_json1_CleanUp) as f:
            CleanUp = json.load(f)

        print('Conditions to be tested:')
        print(conditions)
        opt_type = conditions["strategy"][0]
        print('opt_type')
        print(opt_type)

        # Conc of stock solutions for pump A and pump B
        # A = iso, B = allyl
        A_stock_conc = 0.495
        B_stock_conc = 0.679

        ret_time = float(conditions["tau"])
        T = float(conditions["temperature"])
        T = round(T, 1)
        eqv = conditions["eqv"]

        # Calculate total flow rate
        reactor_vol = 7.0
        total_flow_rate = reactor_vol / ret_time
        print('total_flow_rate')
        print(total_flow_rate)

        # Calculate flow rate of pump A & B based on: total flow rate, Eqv, and concentration of stock solutions
        print('eqv')
        print(eqv[0])
        eqv = round(eqv[0], 3)

        print('eqv')
        print(eqv)
        eqv_ratio = Fraction(str(eqv))

        print('eqv_ratio')
        print(eqv_ratio)
        A = eqv_ratio.denominator
        B = eqv_ratio.numerator
        ratio_tot = A + B

        A_change = A / A_stock_conc
        B_change = B / B_stock_conc
        tot_change = A_change + B_change

        flow_A = total_flow_rate / tot_change * A_change
        flow_B = total_flow_rate / tot_change * B_change

        flow_A = round(flow_A, 2)
        flow_B = round(flow_B, 2)
        total_flow_rate = flow_A + flow_B

        ret_time = reactor_vol / (flow_A + flow_B)
        ret_time = round(ret_time, 2)
        conditions["tau"] = ret_time
        conditions["temperature"] = T

        A_ratio = A_stock_conc * flow_A
        B_ratio = B_stock_conc * flow_B

        new_eqv = B_ratio / A_ratio
        new_eqv = round(new_eqv, 3)
        eqv = new_eqv
        conditions["eqv"] = eqv

        print('T, ret_time, flow_A, flow_B, eqv')
        print(T, ret_time, flow_A, flow_B, eqv)

        tube_vol_to_T = 1.1  # volume from selector valve to t-mixer
        pumpA_time = tube_vol_to_T / flow_A
        pumpB_time = tube_vol_to_T / flow_B

        time_dif = pumpB_time - pumpA_time
        time_dif = time_dif * 60  # Convert to seconds
        time_dif = round(time_dif, 1)

        if time_dif <= 0:
            time_dif = 0.1

        # Update parameters before JSON message is sent to reactor
        Exp_seq[1]['set'] = T
        Exp_seq[3]['set'] = flow_B
        Exp_seq[3]['delay'] = time_dif
        Exp_seq[5]['set'] = flow_A

        ### Start run on Uniqsis
        test = requests.post(RasPi_start, json=Exp_seq,
                             auth=HTTPBasicAuth(username, password))
        print(test)

        ### Wait for reactor to start run
        ### Reactor may need so time to heat up or cool down to specified temperature
        class MyHandler(BaseHTTPRequestHandler):
            def do_POST(self):
                if self.path == '/running':
                    print('from do_POST')
                    # Insert your code here

                if self.path == '/run_relay':
                    print('from do_POST')
                self.send_response(200)

        http = socketserver.TCPServer((IP_Control_PC, 9000), MyHandler)
        print('Waiting for reactor to start run')
        http.handle_request()
        print('Reactor is running')

        ### Wait for 8.5ml of A to be injected
        vol_of_A = 8.5
        inj_time = vol_of_A / flow_A
        inj_time = round(inj_time, 2)
        print('Waiting ' + str(inj_time) + ' min for ' + str(vol_of_A) + ' ml of A to be pumped')
        sleep(inj_time * 60)

        print('Switching to solvent')
        test = requests.post('http://csirpharmatech.hopto.org:1880/start', json=Solv_chg,
                             auth=HTTPBasicAuth(username, password))
        # print(test)

        ### Wait for 'steady state' before taking sample
        wait_vol = 4
        wait_time = (wait_vol / total_flow_rate)
        print('Going to wait for ' + str(wait_time) + ' min before taking sample. (' + str(wait_vol) + ' ml)')
        sleep(wait_time * 60)

        ### Use relay to start HPLC run
        test = requests.post(RasPi_run_relay,  # json=Exp_seq,
                             auth=HTTPBasicAuth(username, password))
        sleep(2)

        ### Start clean up of reactor
        print('Starting reactor wash')
        run_clean = requests.post(RasPi_start, json=CleanUp,
                                  auth=HTTPBasicAuth(username, password))

        ### Wait for HPLC to start analysis
        print('Waiting for LC analysis')
        sleep(200)

        ### Calculate the theoritcal product concentration
        prod_theoritical_conc = A_stock_conc * (flow_A / total_flow_rate)
        prod_theoritical_conc = round(prod_theoritical_conc, 5)
        print('prod_theoritical_conc')
        print(prod_theoritical_conc)

        ### Wait/Grab data for response from HPLC ###
        iso_conc, allyl_conc, prod_conc, prod_yld, hplc_run = self.grab_data(IP_HPLC_PC, prod_theoritical_conc)
        results = iso_conc, allyl_conc, prod_conc, prod_yld

        ### Calculate the STY
        MW = 192.21
        sty = ((prod_conc * MW * (total_flow_rate * 0.06)) / (reactor_vol / 1000))

        ### Add results to csv file
        header = ['opt_type', 'T', 'ret_time', 'eqv', 'flow_A', 'flow_B', 'iso_conc', 'allyl_conc', 'prod_conc',
                  'prod_theoritical_conc', 'prod_yld', 'sty', 'hplc_run']
        data_to_save = (
        opt_type, T, ret_time, eqv, flow_A, flow_B, iso_conc, allyl_conc, prod_conc, prod_theoritical_conc, prod_yld,
        sty, hplc_run)
        with open(r'XXX', 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f, )
            writer.writerow(header)
            writer.writerow(data_to_save)

        # Save the STY results for the optimisation algorithm
        conditions[("sty", "DATA")] = sty

        return conditions, {}

    def to_dict(self, **kwargs):
        experiment_params = dict(noise_level=self.noise_level)
        return super().to_dict(**experiment_params)
