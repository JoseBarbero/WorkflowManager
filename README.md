# WorkflowManager
Docker and Galaxy based tool for bacterial sequence analysis.

Trabajo de Fin de Máster en Bioinformática y Biología computacional. 
Universidad Autónoma de Madrid. 
En colaboración con los grupos de investigación ADMIRABLE y TECNOFOOD de la Universidad de Burgos.

Campylobacter jejuni es una bacteria Gram negativa, que a pesar de tener unas condiciones
complicadas de crecimiento, es la zoonosis bacteriana que produce un mayor número de
intoxicaciones alimentarias en los países tanto desarrollados como en vías de desarrollo. Por
ejemplo, en la EU en el año 2016 se declararon del orden de 250.000 casos comprobados. El
coste debido a la campilobacteriosis se estima en la EU en torno a 2,4 billones de euros anuales. La
fuente de contaminación más habitual es el consumo de carne de pollo poco cocinada. El
grupo de investigación Tecnofood lleva varios años investigando sobre las fuentes de
contaminación de este microorganismo a lo largo de la cadena alimentaria. En la actualidad se
dispone de una colección de Campylobacter spp. de alrededor de 2000 cepas. Con el fin de
obtener una información más precisa sobre la persistencia de este microorganismo a lo largo
de la cadena alimentaria, se han aislado varios genotipos persistentes en el matadero. De estos se han secuenciado con un equipo MISeq (Illumina) 45 de ellas.

El proyecto consiste en diseñar un workflow que permita, a partir de los datos obtenidos en
formato fastq proporcionados por el equipo, conseguir realizar las fases de trimming y
evaluación de la calidad de las secuencias obtenidas, obtención de contigs, assembling y
anotación, para poder tener la información de la secuencia de genes del genoma completo de
las cepas de Campylobacter secuenciadas. En la actualidad existen varios programas
desarrollados por varios grupos de investigación internacional que realizan las funciones
demandadas. Se trata de buscar la solución más eficaz y fácil de implementar y que de los
mejores resultados, por lo que habrá que comparar diferentes programas y estrategias.
Adicionalmente, se requiere incorporar en este workflow o en análisis paralelos, la posibilidad
de detectar insertos de origen viral en el genoma y herramientas que permitan la comparación
rápida de los genomas de las distintas cepas aisladas, algunas de ellas pertenecientes a
individuos del mismo genoma. Puesto que los usuarios finales no son expertos informáticos, se
requiere desarrollar un entorno de fácil uso por parte de los usuarios finales, que son los que
han demandado este trabajo.
