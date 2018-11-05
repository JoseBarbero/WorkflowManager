from bioblend.galaxy import GalaxyInstance

# Connect to galaxy server
# Se puede con key o con user/pass
gi = GalaxyInstance('http://localhost:8080/', email='admin@galaxy.org', password='admin')

# spades_id = gi.tools.get_tools(name="SPAdes")[0]["id"]
# gi.tools.run_tool(history["id"], spades_id, tool_inputs={})

# Get history id
# ToDo hacerlo con un history propio
# hist_id = gi.histories.get_histories()[0]["id"]
hist = gi.histories.get_current_history()
hist_id = hist["id"]

# Uploading Datasets to a History
# gi.tools.upload_file("genomas/200/200_TCCTGAGC-AGAGTAGA_L004_R1_001.fastq", hist_id)
# gi.tools.upload_file("genomas/200/200_TCCTGAGC-AGAGTAGA_L004_R2_001.fastq", hist_id)

# Check datasets
for dataset in hist["state_ids"]["ok"]:
    if gi.datasets.show_dataset(dataset)["name"] == "200_TCCTGAGC-AGAGTAGA_L004_R1_001.fastq":
        id_forward = gi.datasets.show_dataset(dataset)["id"]
    elif gi.datasets.show_dataset(dataset)["name"] == "200_TCCTGAGC-AGAGTAGA_L004_R2_001.fastq":
        id_reverse = gi.datasets.show_dataset(dataset)["id"]

# Get workflow id
wf_id = [wf["id"] for wf in gi.workflows.get_workflows() if wf['name'] == "Main_WF"][0]

# Set workflow inputs
wf = gi.workflows.show_workflow(wf_id)
wf_inputs = wf['inputs']

datamap = dict()
datamap['0'] = {'src': 'hda', 'id': id_forward}
datamap['1'] = {'src': 'hda', 'id': id_reverse}

# Run Workflow
gi.workflows.run_workflow(wf_id, datamap, history_id=hist_id)
