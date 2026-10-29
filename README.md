# FLAME GPU 2 Notebook Template (Python 3)

This repository provides a Notebook Template for using the Python 3 interface for [FLAME GPU 2](https://github.com/FLAMEGPU/FLAMEGPU2).

## Template

This is a template for building a model in FLAME GPU with an array of 2D spatial agents. It contains the basics of a model (which does not perform any behaviour) as a starting point for adaption. It includes a visualiser module to display agent variables via MatPlotLib.

### Google Colab

You can launch the notebook in Colab using the link below. Some additional steps are required within the notebook which are described.

 - [Launch Colab Notebook](https://colab.research.google.com/github/FLAMEGPU/FLAMEGPU2-Notebook-Template/blob/main/FLAMEGPU2-Notebook-Template.ipynb)

### Running this Template Locally

> **Note**: The notebook currently assumes you are using python 3.6, with CUDA 11.0 on a Linux x86_64 machine. This will be corrected in the future.

To run this template locally you will require:

+ Python `>= 3.10`
+ CUDA `>= 13.0` and a [Compute Capability](https://developer.nvidia.com/cuda-gpus) >= 5.0 NVIDIA GPU (note you can use CUDA 12.0+ but will need to modify the extra-index-url in the notebook)
+ Linux with `glibc >= 2.28`
  + Windows support/instructions will be introduced at a later date
+ An `x86_64` CPU
  + Including [`NVRTC`](https://docs.nvidia.com/cuda/nvrtc/index.html)
  + If you wish to run this template on an `ppc64le` or `arm64-sbsa` based-system, you will need to build `pyflamegpu` from source.
  Please see the main [FLAMEGPU/FLAMEGPU2](https://github.com/FLAMEGPU/FLAMEGPU2) repository for instructions on building from source.
+ NodeJS installed to support interactive plotting

1. Clone the repository if you have not already done so

2. Create a new python `venv` or conda environment and activate it
  
    ```bash
    # I.e. if using a venv on linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. [Install Jupyterlab](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) (or jupyter notebook)

    ```bash
    # I.e. if using a venv and pip
    python3 -m pip install -U jupyterlab matplotlib ipympl notebook
    ```

4. Launch `jupyter lab` or the legacy `jupyter notebook` interface and open `FLAMEGPU2-Notebook-Template.ipynb`

    ```bash
    # Using jupyter lab
    jupyter lab FLAMEGPU2-Notebook-Template.ipynb
    # Using jupyter notebook
    jupyter notebook FLAMEGPU2-Notebook-Template.ipynb
    ```

## Known Issues

### Ipympl backend

Colab also has a known [bug](https://github.com/googlecolab/colabtools/issues/5425) with `ipympl` which is used for interactive plotting of the results. Support for `ipympl` is planned in a future release. For now a work-around is included which requires restarting the kernel.