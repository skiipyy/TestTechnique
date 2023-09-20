# DataPipeline

This repository provides a pipeline to process data.


Table of Contents
=================

   * [DataPipeline](#pipeline)
      * [Table of Contents](#table-of-contents)
      * [Project structure](#project-structure)
      * [Jobs description](#jobs-description)
         * [Import job](#import-job)
      * [Airflow Dags](#airflow-dags)
         * [Import dag](#import-dag)
         * [Process dag](#process-dag)
      * [Quickstart](#quickstart)
         * [Local steps](#local-steps)
         * [Run local](#run-local)
         * [With Airflow](#with-airflow)
   * [SQL Query](#SQL-query)
    
## Project structure
```
.
├── config
│   ├── dag_config.yaml
│   ├── file_to_import.yaml
│   ├── file_to_process.yaml
│   └── projects_list.json
├── dags
│   ├── create_dags.py
│   ├── import_dag.py
│   ├── orchestrator_dag.py
│   └── process_dag.py
├── import
│   ├── cloudbuild.yaml
│   ├── Dockerfile
│   ├── config
│   │   └── config.ini
│   └── src
│       ├── csvsource.py
│       ├── import.py
│       ├── jsonsource.py
│       ├── mylogger.py
│       ├── source.py
│       └── utils.py
├── .gitignore
├── README.md
├── requirements.txt
├── run_import.sh
├── run_process.py
├── src
│   └── graph.py
├── tests
│   └── graph.py
└── sql_queries
    ├── query_1.sql
    └── query_2.sql

```

Some explanations regarding structure:
- `config` - folder is where config files about environments and execution context is located.
- `dags` - Airflow dags
- `src` - Class and function that will be used in the dags
- `tests` - Test class and function that will be used in the dags
- `import` - Import job code 
- `run_import.sh` - SH script to run import job
- `run_process.py` - PY script to process data and generate json graph

## Job description

### Tests
To tests the functions of the Graph Class you can run the testsuit
```bash
python -m unittest test_graph.py
```
We can add more tests in the futur.

### Import job
The purpose of the import job is to extract the data from source to `Google Cloud Storage`.
The source could be CSV, JSON, ORACLE, MYSQL, MSSQL ...
For now I just implemented CSV and JSON sources.

In my pipeline, the import job would be in a separeted repository with a `Dockerfile` and a `cloudbuild.yaml` file.

#### Why ?
So each time we will make some modifications on the code, our `cloudbuild.yaml` would trigger `Google Cloud Build` to build and push the docker image on `Google Cloud Registry`.

#### How to run the job ?

The import job would be called on a certain schedule on a server.
We can use `crontab` for example.
`crontab` would pull and run the docker image with specific parameters.
For the technical test you can run locally that command at the root of the repository.
```bash
./run_import.sh
```

###### Parameters
- `--config_file` - Path of the config file giving all data sources
- `--source_type` - Type of the source to import
- `--source_id` - Source id of the source file to import
- `--source` - Path or table name of the source file to import
- `--dest_table` - Name of the destination table
- `--bucket_name` - Bucket name to import in GCS
- `--output_folder` - Output folder, file will be stored in GCS by default
- `--debug` - Set debug level
- `--env` - Environment


### Airflow Dags
Apache Airflow is a robust solution for managing and running complex data pipelines. It offers great flexibility, dependency management, failure recovery, and seamless integration with Google Cloud Platform. It is a smart choice for orchestrating and automating your data flows in a production environment.

In the pipeline we can create dynamic dags by reading configuration files.
The dags files would be stored in `Google Cloud Storage` and they would be read be `Google Cloud Composer`.
#### Import dag
The purpose of this dag is to load the data extracted in `Google Cloud Storage` to `BigQuery` so the data is available to be queried for analytics purposes.
> **_NOTE:_**  
For the technical test, this dag is impemented but it does not work because I do not have available Bigquery buckets.

#### Process dag
The purpose of this dag is to process data imported by our pipeline to generate a json file of the graph.
To generate a json graph, I created a class named `Graph` and methods in the folder `src`.
- `class Graph()` - Class Graph
- `from_json(self, json_graph)` - It will set the graph from a json
- `add_drug(self, drug)` - It will add one drug to the graph
- `add_drugs(self, df_drugs)` - It will add drugs to the graph
- `add_pubmed(self, pubmed)` - It will add one pubmed to the graph
- `add_pubmeds(self, df_pubmeds)` - It will add pubmeds to the graph
- `add_clinical_trial(self, clinical_trial)` - It will add one clinical_trial to the graph
- `add_clinical_trials(self, df_clinical_trials)` - It will add clinical_trials to the graph
- `to_json(self)` - Get json version of the graph
- `get_drugs_of_journal(self, journal)` - Get drugs of one journal
- `get_journals(self)` - Get journals of the graph
- `get_journal_with_most_drugs(self)` -  Get journal with the most drugs. Multiple journals if same number of drugs

For the technical test you can run locally that command at the root of the repository.
```bash
python run_process.py
```

#### Orchestrator dag
The orchestrator will trigger the import dag and then the process dag.


## Quickstart

### Local steps
Perform the following actions in your development environment:
- Create new venv environment and activate it:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
- Install development dependencies:
```bash
pip install -r /path/to/requirements.txt
```
- Install Airflow:
```bash
pip install "apache-airflow[celery]==2.4.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.4.2/constraints-3.7.txt"
```
- Set AIRFLOW_HOME to your local current directory:
```bash
export AIRFLOW_HOME=/path/to/repo/
```
- Init Airflow Database:
```bash
airflow db init
```
- In the '`airflow.cfg`' file set:
```bash
load_examples = False
```
- Create Airflow user:
```bash
airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@admin.com
```

### Run local
Run import job:
- Import files from path to local or `GCS`
```bash
./run_import.sh
```
`imported_data` directory  has been created to the root with parquet files.

Process data and generate JSON graph locally
```bash
python run_process.py
```
`processed_data` directory has been created to the root with json graph.
### With Airflow
- Import dag: Load data imported by the import job, from locally or GCS to BQ.
> **_NOTE:_**  
The import dag is available but it will not work because I do not have real GCS buckets and BQ.
This is just to show you.

- Process dag: Process data imported locally, on GCS or on BQ and generate json graph file.
- Orchestrator dag: Trigger import dag then process dag.

Ideally we would run the orchestrator dag so it will trigger the import dag then the process dag.
To do so, run the airflow webserver
```bash
airflow webserver -D -p 8888
```
Then, run the airflow scheduler
```bash
airflow scheduler -D
```

Go to your browser http://localhost:8888/

Dags are created

## Questions

### Quels sont les éléments à considérer pour faire évoluer votre code afin qu’il puisse gérer de grosses volumétries de données (fichiers de plusieurs To ou millions de fichiers par exemple) ? Pourriez-vous décrire les modifications qu’il faudrait apporter, s’il y en a, pour prendre en considération de telles volumétries ?
Si l'on veut gérer de grosses volumétriees de données:
- Pour le traitement, Cloud Dataflow, Cloud Dataprep ou Cloud Dataproc peuvent être utilisés pour le traitement de données à grande échelle. Utiliser des frameworks de traitement distribué comme Apache Beam (qui peut être utilisé avec Cloud Dataflow) pour paralléliser le traitement des données permettrai de répartir la charge sur plusieurs nœuds, ce qui est essentiel pour traiter de grandes volumétries de données.
- Partitionnement de données : Diviser les données en partitions ou en blocs pour le traitement parallèle. Par exemple, lors de l'ingestion de gros fichiers, les diviser en morceaux gérables et les traiter en parallèle.
- Optimisation des requêtes : S'assurer d'optimiser les requêtes. Utilisez des index appropriés, envisagez le partitionnement des tables si nécessaire, et optimiser les requêtes SQL.
- Streaming vs. Batch : Réfléchir à la manière dont vous traitez les données. Les pipelines de streaming sont adaptés aux données en temps réel, tandis que les pipelines batch sont conçus pour traiter des volumes de données statiques.
- Auto-scaling : Augmenter ou réduire la capacité de traitement en fonction de la charge de travail. Par exemple, Cloud Dataflow prend en charge l'auto-scaling.
- Surveillance et gestion des erreurs : Mettre en place une surveillance proactive de votre pipeline pour détecter les erreurs et les gérer efficacement.
- Tests de performances : Effectuer des tests de performances et d'évolutivité pour identifier les éventuels goulots d'étranglement et les points faibles du pipeline.
- Plan de reprise d'activité : Prévoir un plan de reprise d'activité pour faire face à d'éventuelles pannes ou interruptions de service.
- Optimisation des coûts : Surveiller les coûts associés à votre pipeline et les optimiser en fonction de l'utilisation réelle.


# SQL Query
The queries are in the `sql_queries` folder.