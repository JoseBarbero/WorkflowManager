# coding: utf8
import os
import datetime
import time
from bioblend.galaxy import GalaxyInstance

# Connect to galaxy server
# TODO que las credenciales las meta el usuario
# ┌─────┐
# │ CGO │
# └─────┘
#   import getpass
#   from myCredentials import * # to initialize dni and pwd externally
#                               # in myCrentials.py only the initialization of
#                               # the variables password and email
#   # in case there are not credentials defined in myCredentials
#   email = globals().get('email', None) or input("Email? ")
#   password = globals().get('password', None) or getpass.getpass("Password? ")
# Other common pattern is to define the value as environment variables
#    and use os.environ['PASSWORD'] and os.environ['EMAIL']
#    more on this at: https://www.reddit.com/r/learnpython/comments/264ffw/what_is_the_pythonic_way_of_storing_credentials/

gi = GalaxyInstance('http://localhost:8080/', email='admin@galaxy.org', password='admin')

# Import the workflow
wf_name = "test"
if wf_name not in [wf["name"] for wf in gi.workflows.get_workflows()]:
    gi.workflows.import_workflow_from_local_path("./Workflows/"+wf_name+".ga", True)

# Create histories for input and output
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
history_name = "MyWorkflowHistory"+timestamp
results_history_name = "ResultsHistory"+timestamp
hist = gi.histories.create_history(history_name)
hist_id = hist["id"]

# Uploading Datasets to a History
folders = ["./Forward", "./Reverse"]
input_files_names = []
files = [folder+"/"+file for folder in folders for file in os.listdir(folder)]
files.sort()
for file in files:  # Flat list of files of both paths
    if not file.split("/")[-1].startswith("."):
        gi.tools.upload_file(file, hist_id)
	input_files_names.append(file.split("/")[-1])

# Check datasets
forward_list = []
reverse_list = []
for dataset in gi.histories.show_matching_datasets(hist_id):
    data_name = dataset["name"]
    data_id = dataset["dataset_id"]
    data_description = {'id': data_id,
                        'name': data_name,
                        'src': 'hda'}
    if "R1" in data_name:
        forward_list.append(data_description)
    elif "R2" in data_name:
        reverse_list.append(data_description)

# Create input collections
forward_description = {'collection_type': 'list',
                       'element_identifiers': forward_list,
                       'name': 'Forward_collection'}
reverse_description = {'collection_type': 'list',
                       'element_identifiers': reverse_list,
                       'name': 'Reverse_collection'}
forward_collection = gi.histories.create_dataset_collection(hist_id, forward_description)
reverse_collection = gi.histories.create_dataset_collection(hist_id, reverse_description)

# Get workflow id
wf_id = [wf["id"] for wf in gi.workflows.get_workflows() if wf['name'] == "test"][0]

# Set workflow inputs
wf_inputs = dict()
wf_inputs['0'] = {'src': 'hdca', 'id': forward_collection["id"]}
wf_inputs['1'] = {'src': 'hdca', 'id': reverse_collection["id"]}

# Run Workflow
gi.workflows.invoke_workflow(wf_id, wf_inputs, history_name=results_history_name)

# Exportar ficheros de salida
while any([gi.jobs.get_state(job["id"]) != "ok" for job in gi.jobs.get_jobs()]):
    time.sleep(10)
    print("Please, wait. The job is running...")
output_history_id = gi.histories.get_histories(name=results_history_name)[0]["id"]

output_dir = results_history_name
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for dataset in gi.histories.show_matching_datasets(output_history_id):
    if dataset["name"] not in input_files_names:
		file_name = dataset["name"]+"."+dataset["file_ext"]
		file_name = file_name.replace(" ", "_")
		file_name = file_name.replace(":", "_")
		gi.histories.download_dataset(output_history_id, dataset["dataset_id"], output_dir+"/"+file_name, False)
print("DONE")
