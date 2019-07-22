# OpenFaaS ChEMBL Target Prediction example (2)

This is an example of how to use machine learning algorithms with openfaas platform.
Using new OpenFaaS watchdog: https://github.com/openfaas-incubator/of-watchdog

# Installation

## Build the image:
```
faas-cli build -f openfaas_tp.yml
```

## Push it to docker hub:
```
docker push chembl/openfaas_tp
```

## Deploy it to OpenFaaS
```
faas-cli deploy -f openfaas_tp.yml --replace -e read_timeout=60, write_timeout=60
```