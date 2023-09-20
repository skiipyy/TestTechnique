import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json
import yaml
import os

from networkx.readwrite import json_graph
from datetime import datetime
from airflow import DAG
from airflow.operators import dummy_operator, python_operator

from src.graph import generate_json_graph


def process_dag(env, yaml_path, tags):
    '''
        It creates an process dag.
        It will process data to generate a json graph of drugs, pubmed, cilinical trials and journals

        Parameters:
            env (str): Environment
            yaml_path (str): Path to the yaml config of this dag
            tags ([str]): List of tags of this dag

        Returns:
            dag (Dag): Dag
    '''

    with DAG(
        dag_id=f'process_{env}',
        schedule_interval=None,
        start_date=datetime(2021,1,1),
        catchup=False,
        max_active_runs=1,
        dagrun_timeout=60,
        tags=tags
        ) as dag:

        start = dummy_operator.DummyOperator(
            task_id='start',
            dag=dag
        )

        end = dummy_operator.DummyOperator(
            task_id='end',
            dag=dag
        )

        with open(yaml_path) as yaml_file:
            c = yaml.safe_load(yaml_file)

        python_task	= python_operator.PythonOperator(
            task_id='python_task',
            python_callable=generate_json_graph,
            provide_context=True,
            op_kwargs={
                "path_drugs": c['drugs']['path'],
                "path_clinical_trials": c['clinical_trials']['path'],
                "path_pubmeds": c['pubmeds']['path'],
                "dest_name": c['output']['path']
            },
            dag=dag
        )

        start >> python_task >> end
    
    return dag