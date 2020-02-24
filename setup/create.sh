#!/bin/bash

for yaml in `master.yml`,`workers.yml` ; do
  peg up $yaml
  wait
done

./install_master_node.sh
./install.sh

# place master.yml and workers.yml in corresponding cluster's folder