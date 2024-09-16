# Conda

## Create a new conda env from the yml

`conda env create -f env.yml`

## Update env to reflect changes in the yml

`conda env update --file env.yml --prune`

## Update yml after pip install

`conda env export > env.yml`

## In case uvicorn is not installed

`pip install uvicorn`

# Running Backend

`litestar run`
