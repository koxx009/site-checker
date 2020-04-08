#!/usr/bin/python3

import requests
import argparse
import subprocess
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument('endpoint', type=str, help='enter your URL')
arg_dict = parser.parse_args()
arg_endpoint = arg_dict.endpoint

cwd = (os.path.dirname(os.path.realpath(__file__)))

try:
    r = requests.get(arg_endpoint, timeout=60)
except requests.exceptions.RequestException as e:
	ans_status = 'Connection error'
	ans_time = '60'
	check_cnt = 1
	try:
	    r = requests.get(arg_endpoint, timeout=60)
	except requests.exceptions.RequestException as e:
		ans_status = 'Connection error'
		ans_time = '120'
		check_cnt = 2
else:
	i = 0
	while i < 2:
		check_site = requests.get(arg_endpoint)
		ans_status = check_site.status_code
		ans_time = check_site.elapsed.total_seconds()
		if ans_status != 200:
			if i < 1:
				time.sleep(60)
			pass
			i = i + 1
			check_cnt = i
		else:
			i = 2
	pass

if ans_status != 200:
	tg_message = '"' + "URL: " + str(arg_endpoint) + "\nHTTP Code: " + str(ans_status) + "\nResponse time: " + str(ans_time) + "\nCheck counter: " + str(check_cnt) +'"'
	tg_sent = "./telega.sh " + str(tg_message)
	subprocess.run(tg_sent, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
pass
