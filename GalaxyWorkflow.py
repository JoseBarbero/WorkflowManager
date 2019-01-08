import os
import datetime
import time
from bioblend.galaxy import GalaxyInstance

# Connect to galaxy server
# TODO que las credenciales las meta el usuario
gi = GalaxyInstance('http://localhost:8080/', email='admin@galaxy.org', password='admin')

# Import the workflow
# TODO Comprobar que el workflow no este ya
gi.workflows.import_workflow_from_local_path("./Workflows/test.ga", True)

# Create new history
# TODO generar con nombre unico con fecha y hora para evitar duplicados
history_name = "MyWorkflowHistory"+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
hist = gi.histories.create_history(history_name)
hist_id = hist["id"]

# Uploading Datasets to a History
# TODO modificar para correr en una ruta cercana
# folders = ["../../../../Desktop/genomas/R1", "../../../../Desktop/genomas/R2"]
folders = ["./R1", "./R2"]
for file in [folder+"/"+file for folder in folders for file in os.listdir(folder)]:  # Flat list of files of both paths
    if not file.split("/")[-1].startswith("."):
        gi.tools.upload_file(file, hist_id)

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
forward_description = {'collection_type': 'list', 'element_identifiers': forward_list, 'name': 'Forward collection'}
reverse_description = {'collection_type': 'list', 'element_identifiers': reverse_list, 'name': 'Reverse collection'}
forward_collection = gi.histories.create_dataset_collection(hist_id, forward_description)
reverse_collection = gi.histories.create_dataset_collection(hist_id, reverse_description)

# Get workflow id
wf_id = [wf["id"] for wf in gi.workflows.get_workflows() if wf['name'] == "test"][0]

# Set workflow inputs
wf_inputs = dict()
wf_inputs['0'] = {'src': 'hda', 'id': forward_collection["id"]}
wf_inputs['1'] = {'src': 'hda', 'id': reverse_collection["id"]}

# Run Workflow
results_history_name = "ResultsHistory"+datetime.datetime.now().strftime('%Y%m%d%H%M%S')
gi.workflows.invoke_workflow(wf_id, wf_inputs, history_name=results_history_name)

# Exportar ficheros de salida
# Esperar a que los trabajos esten terminados para descargar
while any([gi.jobs.get_state(job["id"]) != "ok" for job in gi.jobs.get_jobs()]):
    time.sleep(10)
    print("Please, wait. The job is running...")
output_history_id = gi.histories.get_histories(name=results_history_name)[0]["id"]

output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
for dataset in gi.histories.show_matching_datasets(output_history_id):
    file_name = dataset["name"]+"."+dataset["file_ext"]
    file_name = file_name.replace(" ", "_")
    file_name = file_name.replace(":", "_")
    gi.histories.download_dataset(output_history_id, dataset["dataset_id"], output_dir+"/"+file_name, False)
print("DONE")
