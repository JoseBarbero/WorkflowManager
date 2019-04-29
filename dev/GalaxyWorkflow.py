# coding: utf8
import os
import datetime
import time
import sys
import getpass

from bioblend.galaxy import GalaxyInstance
from credentials import *

# Connect to galaxy server
email = login['email'] or input("Email? ")
password = login['password'] or getpass.getpass("Password? ")

gi = GalaxyInstance('http://localhost:8080/', email=email, password=password)

# Import the workflow
wf_name = "CJ_Worfklow"
if wf_name not in [wf["name"] for wf in gi.workflows.get_workflows()]:
    gi.workflows.import_workflow_from_local_path("../build/workflows/"+wf_name+".ga", True)

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
wf_id = [wf["id"] for wf in gi.workflows.get_workflows() if wf['name'] == "CJ_Worfklow"][0]

# Set workflow inputs
wf_inputs = dict()
wf_inputs['0'] = {'src': 'hdca', 'id': forward_collection["id"]}
wf_inputs['1'] = {'src': 'hdca', 'id': reverse_collection["id"]}

# Run Workflow
gi.workflows.invoke_workflow(wf_id, wf_inputs, history_name=results_history_name)


# Export output files
output_history_id = gi.histories.get_histories(name=results_history_name)[0]["id"]
ini_time = time.time()

keep=True
while keep:
    try:
        keep = any([gi.jobs.get_state(job["id"]) not in ["ok", "error", "deleted", "new"] for job in gi.jobs.get_jobs()])
        time.sleep(60)
        state = gi.histories.show_history(output_history_id, contents=False)["state_details"]

        ok = state["ok"]
        running = state["running"]
        queued = state["queued"]
        errors = state["error"]
        paused = state["paused"]
        sys.stdout.flush()
        print("Please, wait. Workflow is running...")
        time_running = time.time()-ini_time
        print("Time running: "+str(datetime.timedelta(seconds=time_running)))
        print("\t "+str(ok)+" jobs finished")
        print("\t "+str(running)+" jobs running")
        print("\t "+str(queued)+" jobs queued")
        print("\t "+str(errors)+" jobs failed")
        print("\t "+str(paused)+" jobs paused")
    except:
        print("TIMEOUT")
        pass

# Create output directories
output_dir = results_history_name
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_filter = ("roary", "prokka", "abricate", "spades")

for subdir in output_filter:
    if not os.path.exists(output_dir+"/"+subdir):
        os.makedirs(output_dir+"/"+subdir)

# Download dataset
for dataset in gi.histories.show_history(output_history_id, contents=True):
    if dataset["history_content_type"] == "dataset": # Roary es la única herramienta que no va por colecciones
        if dataset["name"].lower().startswith("roary"): 
            file_name = dataset["name"].split(" ")[0] + dataset["name"].split(" ")[-1]+"."+dataset["extension"]
            gi.histories.download_dataset(output_history_id, dataset["id"], output_dir+"/"+"roary"+"/"+file_name, False)
    elif dataset["history_content_type"] == "dataset_collection":
        for element in gi.histories.show_dataset_collection(output_history_id, dataset["id"])["elements"]:
            file_name = dataset["name"].split(" ")[0]+"_"+element["element_identifier"].split(".")[0]+"."+element["object"]["file_ext"]
            file_name = file_name.replace("_R1", "")
            if file_name.lower().startswith(output_filter):
                for tool in output_filter:
                    if dataset["name"].lower().startswith(tool):
                        subdir = tool
                gi.histories.download_dataset(output_history_id, element["object"]["id"], output_dir+"/"+subdir+"/"+file_name, False)

print("DONE")
