import boto3
import paramiko
import scp
import numpy as np
import pickle
import matplotlib.pyplot as plt

python_command = '/home/ubuntu/anaconda3/bin/python ./ising/launch_single.py'

ec2 = boto3.resource('ec2')

key = paramiko.RSAKey.from_private_key_file('./ising.pem')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
instances = ec2.instances.filter(Filters=[{'Name': 'instance-state-name', 'Values':['running']}])

outputs = []
stderrs = []
clients = []
n_instances = len(list(instances.all()))
print("Available instances:", n_instances)

START_TEMPERATURE = 1.5
END_TEMPERATURE = 2.5
GRID_SIZE = 100

temperatures = np.linspace(START_TEMPERATURE, END_TEMPERATURE, n_instances)

print("Number of temperatures:", len(list(temperatures)))

for i, instance in enumerate(instances):
    print("running on instance:", instance.public_dns_name)
    client.connect(hostname=instance.public_dns_name, username="ubuntu", pkey=key)
    _, stdout, _  = client.exec_command('git -C ./ising fetch && git -C ./ising pull')
    print(stdout.read().decode())
    cmd = python_command + ' ' + str(GRID_SIZE) + ' ' + str(temperatures[i]) + ' ' + str(temperatures[i]) + '.pkl'
    print("command is:", cmd)
    stdin, stdout, stderr = client.exec_command(cmd)
    outputs.append(stdout)
    stderrs.append(stderr)

for i, output in enumerate(outputs):
    print("Output {} of {}".format(i+1, len(outputs)))
    print("STDOUT")
    print(output.read().decode())
    print("STDERR")
    print(stderrs[i].read().decode())

for i, instance in enumerate(instances):
    print("collecting output from instance:", instance.public_dns_name)
    client.connect(hostname=instance.public_dns_name, username="ubuntu", pkey=key)
    scp_client = scp.SCPClient(client.get_transport())
    scp_client.get(str(temperatures[i]) + ".pkl", local_path='./experiments')

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

with open("all_metrics.pkl", 'rb') as f:
    pickle.dump(experiment, f)



