#!/bin/bash

CLUSTER_NAME=spark-cluster

peg sshcmd-cluster ${CLUSTER_NAME} "sudo apt-get install bc"

    peg sshcmd-node ${CLUSTER_NAME} 1 "wget -P ~// https://jdbc.postgresql.org/download/postgresql-42.2.9.jar"
    peg sshcmd-node ${CLUSTER_NAME} 1 "wget -P ~// https://repo1.maven.org/maven2/com/databricks/spark-csv_2.10/1.1.0/spark-csv_2.10-1.1.0.jar"

done