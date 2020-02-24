#!/bin/bash

CLUSTER_NAME=spark-cluster

peg fetch ${CLUSTER_NAME}

for item in ssh aws ; do
  peg install ${CLUSTER_NAME} $item
done

for item in zookeeper kafka hadoop spark ; do
  peg install ${CLUSTER_NAME} $item
  peg service ${CLUSTER_NAME} $item start
done