# Galaxy - BioinfWorkflow
#
# VERSION       0.2

FROM serux/docker-galaxy-bioinfworkflow

MAINTAINER Björn A. Grüning, bjoern.gruening@gmail.com

ENV GALAXY_CONFIG_BRAND BioinfWorkflow

WORKDIR /galaxy-central

RUN add-tool-shed --url 'http://testtoolshed.g2.bx.psu.edu/' --name 'Test Tool Shed'

# Install Visualisation
RUN install-biojs msa

# Job config
ADD job_conf.xml $GALAXY_ROOT/config/job_conf.xml
RUN pip install pbs

# Adding the tool definitions to the container
ADD my_tool_list.yml $GALAXY_ROOT/my_tool_list.yml

# Install deepTools
RUN install-tools $GALAXY_ROOT/my_tool_list.yml

# Install workflow
ADD workflows/* $GALAXY_HOME/workflows/
ADD install_workflows_wrapper.sh $GALAXY_ROOT/install_workflows_wrapper.sh
RUN $GALAXY_ROOT/install_workflows_wrapper.sh $GALAXY_HOME/workflows/CJ_Worfklow.ga

# Mark folders as imported from the host.
VOLUME ["/export/", "/data/", "/var/lib/docker"]

# Expose port 80 (webserver), 21 (FTP server), 8800 (Proxy)
EXPOSE :80
EXPOSE :21
EXPOSE :8800

# Autostart script that is invoked during container start
CMD ["/usr/bin/startup"]


