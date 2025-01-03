#!/usr/bin/python3
import datetime
import sys
from pyzabbix import ZabbixMetric, ZabbixSender
import boto3
import time
import json
from botocore.config import Config
from neptune_var import get_data
import os
from lambda_status_instance import get_status, get_cluster_status

ZABBIX_HOST = os.environ['ZABBIX_PASSIVE']
ZABBIX_PORT = int(os.environ['ZABBIX_PASSIVE_PORT'])

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
REGION = os.environ['REGION']
METRIC = os.environ['METRIC']
DATABASE = os.environ['DATABASE']
HOST_IN_ZABBIX = os.environ['ZABBIX_HOST_DST']
ITEM_KEY = os.environ['ITEM_KEY']

def convert(string):
    li = list(string.split(","))
    return li

database = convert(DATABASE)
hosts = convert(HOST_IN_ZABBIX)

zabbix_sender = ZabbixSender(zabbix_server=ZABBIX_HOST, zabbix_port=ZABBIX_PORT, use_config=None, chunk_size=2)

def cria_string(var):
	result = '{ "data": ['
	for i in range(len(var)):
		new_line ='{"Label":' +'"'+ str(var[i]["Label"])+'"'+ ',"Values":'+str(Average(var[i]["Values"]))+'}'
		result = result + new_line
		if (i+1) < len(var):
			result = result + ","
	result = result + "]}"
	return result

def Average(lst):
	if len(lst) < 1:
		return 0
	else:
		return sum(lst) / len(lst)

def neptune(database,i):
	if not ACCESS_KEY or not SECRET_KEY:
		use_roles = True
	else:
		use_roles = False

	end = datetime.datetime.utcnow()
	start = end - datetime.timedelta(minutes=10)

	if use_roles:
		conn = boto3.client('cloudwatch', region_name=REGION)
	else:
		conn = boto3.client('cloudwatch', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY,
							region_name=REGION)

	try:
		if int(METRIC) == 0:
			res = conn.get_metric_data(MetricDataQueries=get_data(database,0), StartTime=start, EndTime=end)
		else:
			res = conn.get_metric_data(MetricDataQueries=get_data(database,1), StartTime=start, EndTime=end)
			status = get_status(database)
			cluster_status = get_cluster_status(database)

	except Exception as e:
		print("status err Error running neptune_stats: %s" % e)
		sys.exit(1)
		
	var = res['MetricDataResults']

	result = cria_string(var)

	if int(METRIC) == 0:
		packet = [
		ZabbixMetric(hosts[i], ITEM_KEY, result),
		]
		zabbix_sender.send(packet)

		return {
			"statusCode": 200,
			"body": str(result)
		}
	else:
		packet = [
		ZabbixMetric(hosts[i], ITEM_KEY, result),
		ZabbixMetric(hosts[i], "cluster.database.info" , status),
		ZabbixMetric(hosts[i], "cluster.status.info" , cluster_status)
		]
		zabbix_sender.send(packet)

		return {
			"statusCode": 200,
			"body": str(result)
		}


def run_lambda(event, lambda_context):
	for i in range (len(database)):
		valor = database[i]
		neptune(valor,i)

run_lambda("a", "b")