docker rm $(docker ps -a -q --filter="ancestor=jbarberoaparicio/workflowmanager")
./purge.sh
