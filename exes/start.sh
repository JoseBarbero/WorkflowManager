./purge.sh
docker start $(docker ps -a -q --filter="ancestor=jbarberoaparicio/workflowmanager")
