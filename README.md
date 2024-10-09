# Accelerator Zoo

## Installation Instructions

### Option 1: Docker

TODO

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
