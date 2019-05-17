# WorkflowManager
## Resumen
Docker and Galaxy based tool for bacterial sequence analysis.

El auge de las nuevas técnicas de secuenciación masiva está generando una necesidad de
análisis de gran cantidad de datos que provoca el acercamiento a la bioinformática de nuevos
grupos de investigación antes ajenos a ella. Grupos que solían encargar los análisis de sus datos a
otros grupos de investigación están comenzando a desarrollar sus propios workflows para tratar
los datos personalmente.

En este contexto, el grupo de investigación Tecnofood de la Universidad de Burgos, con una
larga trayectoria en investigación sobre las fuentes de contaminación en la cadena alimentaria,
ha decidido desarrollar un workflow destinado al análisis genómico de la bacteria Campylobacter
jejuni. Este trabajo estudia su proceso de creación, orientado a establecer una primera herramienta
accesible al grupo con la que tendrán la posibilidad de realizar análisis, tanto de las cepas
de esta bacteria, como de otras similares en un futuro. La interfaz gráfica de la infraestructura
utilizada para su soporte, Galaxy, hace posible que el workflow pueda sufrir modificaciones de
manera sencilla en un futuro. Esto permitirá dar lugar a variaciones del workflow sin necesidad
de un nuevo desarrollo poco accesible a usuarios ajenos a la programación.

El sistema se ha desplegado sobre un contenedor Docker con la intención de ahorrar trabajo
al usuario evitando la instalación y configuración de un entorno apropiado.

El workflow consta de 6 utilidades principales que resuelven los aspectos de filtrado de calidad
(Trimmomatic y Prinseq), ensamblado (SPAdes), etiquetado (Prokka), análisis de resistencia a
antibióticos (ABRicate) y análisis pangenómico (Roary).

Finalmente, el funcionamiento de este workflow se ha puesto a prueba utilizando cuarenta
y seis cepas de Campylobacter jejuni, secuenciadas con un equipo Illumina, procedentes de un
matadero del norte de España.

## Abstract

The rise of NGS techniques is generating a need for large amount of data to be analysed.
This is encouraging new research groups to approach to the field of bioinformatics when they
were previously unrelated to it. Groups that used to commission the analysis of their data to
other research groups are beginning to develop their own workflows in order to analyse their
data by themselves.

In this context, Tecnofood, a University of Burgos research group with a long research history
on sources of contamination in the food chain, has decided to develop a workflow to analyse the
genome of the bacterium Campylobacter jejuni. This work studies its creation process, oriented
to establish a first tool accessible to the group with which they will have the opportunity to
make analyses of the strains of this bacterium and of other ones in the future. The interface of
the framework used in its deployment, Galaxy, makes the workflow able to easily undergo modifications
in the future. This will allow non-programmers to make workflow variations without
the need for a new whole development.

The system has been deployed on a Docker container trying to avoid unnecessary configuration
and installation processes of a new environment to the user.

The workflow is made of 6 main tools that solve aspects of quality filtering (Trimmomatic and
Prinseq), assembly (SPAdes), labelling (Prokka), analysis of antibacterial resistance (ABRicate)
and pangenomic analysis (Roary).

Finally, this workflow has been tested using forty-six strains of Campylobacter jejuni, previously
sequenced with an Illumina HiSeq and collected in a slaughterhouse in northern Spain.
