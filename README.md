# Accelerator Zoo

This repository contains the TeAAL specification and/or HiFiber loop nests
representing the following accelerators:

- [DSTC](https://dl.acm.org/doi/10.1109/ISCA52012.2021.00088)
- [ExTensor](https://dl.acm.org/doi/10.1145/3352460.3358275)
- [Eyeriss](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7738524)
- [Flexagon](https://dl.acm.org/doi/10.1145/3582016.3582069)
- [FuseMax](https://arxiv.org/abs/2406.10491)
- [Gamma](https://dl.acm.org/doi/pdf/10.1145/3445814.3446702)
- [GraphDynS](https://dl.acm.org/doi/10.1145/3352460.3358318)
- [Graphicionado](https://dl.acm.org/doi/10.5555/3195638.3195707)
- [OuterSPACE](https://ieeexplore.ieee.org/document/8327050)
- [SIGMA](https://ieeexplore.ieee.org/document/9065523)
- [Tensaurus](https://ieeexplore.ieee.org/document/9065579)
- [TPUv1](https://arxiv.org/abs/1704.04760)

We welcome contributions of other designs from the community.


## System Requirements

### Hardware

- x86-64 CPU
- 5GB disk space

### Software

- [Docker](https://www.docker.com/products/docker-desktop/)
- Web browser

## Installation Instructions

#### Step 0: Clone the repository

Submodules must also be recursively cloned.

```bash
git clone --recurse-submodules git@github.com:FPSG-UIUC/accelerator-zoo.git
cd accelerator-zoo
```

### [Recommended] Option 1: Docker

#### Step 1: Prepare your `docker-compose.yaml`

Copy the `docker-compose.yaml.example` file to a new `docker-compose.yaml`

```bash
cp docker-compose.yaml.example docker-compose.yaml
```

Edit the `docker-compose.yaml` with the appropriate `NB_UID` (the user you want
to own the repository).

#### Step 2: Pull the Docker image

We provide two options for obtaining the docker image. Please choose one of the
options listed below.

##### Option 1: Use `docker-compose`

```bash
docker-compose pull
```

##### Option 2: Build the image from source

```bash
cd ./setup/docker/fibertree-docker
make build
cd ../../..
```

#### Step 3: Start the container

Start the container, including the Jupyter lab.

```bash
docker-compose up -d
```

#### Step 4: Open the Jupyter lab

Navigate to `http://localhost:8888` to open and view the repository.

### Option 2: Python Virtual Environment

#### Step 1: Install Python 3.12

- On [Linux](https://docs.python.org/3.12/using/unix.html#getting-and-installing-the-latest-version-of-python)
- On [Mac](https://formulae.brew.sh/formula/python@3.12) via [Homebrew](https://brew.sh/)

#### Step 2: Create the virtual environment

```bash
python3.12 -m venv env
```

### Start the Virtual Environment

```bash
source env/bin/activate
```

### Step 3: Install the required packages

```bash
python3.12 -m pip install -r setup/native/requirements.txt
```

#### Step 4: Start the Jupyter Lab

```bash
jupyter lab
```

### Option 3: Conda Installation

#### Step 1: Install Conda

Instructions can be found [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

#### Step 2: Create the Conda Environment

Start conda environment with
```bash
conda env create -p ./env -f setup/native/environment.yaml
```

#### Step 3: Start the Conda Environment


```bash
conda activate ./env
```

#### Step 4: Start the Jupyter Lab

```bash
jupyter lab
```

## Using the Accelerator Zoo

In the Jupyter lab enviroment, navigate to
`accelerator-zoo/workspace/notebooks/` (if using the Docker container) or
`workspace/notebooks/` (if using a native installation like Pip or Conda) and
select an accelerator.  Each notebook contains instructions specific to that
notebook and accelerator.

## Contributors

The TeAAL specifications presented in this repository are the combined effort
of many people over the course of many years, including:

- Timor Averbuch
- Alex Dicheva
- Joel S. Emer
- Christopher W. Fletcher
- Yuxin Jin
- Nandeeka Nayak
- Toluwanimi O. Odemuyiwa
- Michael Pellaeur
- Jules Peyrat
- Chenxi Wan
- Yingchen Wang
- Frederic Wu
- Xinrui Wu
- Yan Zhu

We would also like to thank the following people, whose insights allowed us to
better understand, describe, and, in some cases, even validate our TeAAL
specifications, including:

- Tae Jun Ham
- Kartik Hegde
- Tushar Krishna
- Francisco Muñoz-Martinez
- Eric Qin
- Daniel Sanchez
- Hanrui Wang
- Lisa Wu Wills
- Guowei Zhang
- Zhekai Zhang
