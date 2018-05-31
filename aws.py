import boto3
import paramiko
import scp
import numpy as np
import pickle
import time
import matplotlib.pyplot as plt

python_command = '/home/ubuntu/anaconda3/bin/python ./ising/launch_single.py'

ec2 = boto3.resource('ec2')

key = paramiko.RSAKey.from_private_key_file('./ising.pem')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values':['running']}])


n_instances = len(list(instances.all()))
print("Available instances:", n_instances)

START_TEMPERATURE = 1.0
END_TEMPERATURE = 3.5
N_TEMPERATURES = 20
GRID_SIZE = 100
USE_WOLFF = False
N_CONNECTION_ATTEMPTS = 3

T_c = 2.269
'''
temperatures = np.linspace(START_TEMPERATURE, END_TEMPERATURE, N_TEMPERATURES)
'''

temperatures_below = T_c - T_c * np.logspace(-3, -0.5, num=N_TEMPERATURES/2) 
temperatures_above = T_c + T_c * np.logspace(-3, -0.5, num=N_TEMPERATURES/2)
temperatures = []
temperatures.extend(temperatures_below)
temperatures.extend(temperatures_above)

print("Number of temperatures:", len(list(temperatures)))

batches = int(np.floor(N_TEMPERATURES / n_instances)) + 1

temperature_index = 0
for batch in range(batches):
    outputs = []
    stderrs = []
    temperature_indexes = []
    for instance_number, instance in enumerate(instances):
        if temperature_index == N_TEMPERATURES:
            break
        print("running on instance:", instance.public_dns_name)
        for connection_attempt in range(N_CONNECTION_ATTEMPTS):
            try:
                client.connect(hostname=instance.public_dns_name, username="ubuntu", pkey=key)
                break
            except:
                if connection_attempt == N_CONNECTION_ATTEMPTS - 1:
                    raise("Number of connection attempts maxed out.")
        
        _, stdout, stderr  = client.exec_command('git -C ./ising stash')
        print(stdout.read().decode())
        print(stderr.read().decode())
        _, stdout, stderr  = client.exec_command('git -C ./ising pull')
        # wait for the git pull before executing...
        print(stdout.read().decode())
        print(stderr.read().decode())
        cmd = python_command + ' ' + str(GRID_SIZE) + ' ' + str(temperatures[temperature_index]) + ' ' + str(temperatures[temperature_index]) + '.pkl'
        if USE_WOLFF:
          cmd += ' --wolff' 
        print("command is:", cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
        outputs.append(stdout)
        stderrs.append(stderr)
        temperature_indexes.append(temperature_index)
        temperature_index += 1

    for instance_number, output in enumerate(outputs):
        print("Output {} of {}".format(temperature_indexes[instance_number] + 1, N_TEMPERATURES))
        print("STDOUT")
        print(output.read().decode())
        print("STDERR")
        print(stderrs[instance_number].read().decode())

    for instance_number, instance in enumerate(instances):
        if instance_number >= len(temperature_indexes):
            break
        print("collecting output from instance:", instance.public_dns_name)
        for connection_attempt in range(N_CONNECTION_ATTEMPTS):
            try:
                client.connect(hostname=instance.public_dns_name, username="ubuntu", pkey=key)
                break
            except:
                if connection_attempt == N_CONNECTION_ATTEMPTS - 1:
                    raise("Number of connection attempts maxed out.")
        scp_client = scp.SCPClient(client.get_transport())
        scp_client.get(str(temperatures[temperature_indexes[instance_number]]) + ".pkl", local_path='./experiments')

client.close()

all_metrics = []
for temperature in temperatures:
    with open('./experiments/' + str(temperature) + '.pkl', 'rb') as f:
        metrics = pickle.load(f)
        all_metrics.append(metrics)

class Experiment(object):
    def __init__(self, all_metrics, temperatures):
        self.all_metrics = all_metrics
        self.temperatures = temperatures

experiment = Experiment(all_metrics, temperatures)

with open("metropolis_100x100_critical_5000iter_2sidedlog.pkl", 'wb') as f:
    pickle.dump(experiment, f)



