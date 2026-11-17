# DeepInv spectral imaging scripts

## Setup

### Clone the repository

```bash
git clone https://github.com/<your-username>/DeepInv.git
cd DeepInv
```

### Create and activate a virtual environment

On Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This project’s Python requirements are listed in [requirements.txt](requirements.txt). 

# Overview

This repository contains scripts and utilities for preparing, organizing, and reconstructing spectral data acquired with a Hadamard-coded acquisition setup. The general workflow is:

1. Download raw spectral measurements and metadata.
2. Reorder the acquired Hadamard patterns and unsplit paired measurements.
3. Bin and subsample the spectral data into a format suitable for training or reconstruction.
4. Train or test a model on the formatted dataset, or reconstruct images with Spyrit/DeepInv.


## Structure

- `data/`: raw measurement files, ground-truth reconstructions, metadata, and example datasets.
- `ground_truth/`: reconstructed ground-truth cubes for each sample.
- `ground_truth_formatted/`: spectrally binned ground-truth arrays saved as `.npy` files.
- `measurements/`: raw spectral measurement files (`*_spectraldata.npz`).
- `measurements_formatted/`: processed measurement arrays ready for dataset loading or inversion.
- `metadata/`: acquisition metadata JSON files used to decode pattern ordering and imaging settings.

## Script overview

### `dataset.py`
Main dataset-building script. It defines `format_dataset(...)`, which scans the raw ground-truth and measurement folders, reads each metadata file, reorders the measurement patterns, bins the spectral dimension, subsamples the data, and saves the formatted arrays to `ground_truth_formatted/` and `measurements_formatted/`.

Defines `SpectralDataset`, a PyTorch `Dataset` that loads matching `.npy` files from the formatted folders and returns `(x, y)` pairs for training or evaluation.

For more details or to format data manually, see following script. 

### `format_data.py`
More manual, example-driven formatting script. It shows how to:

- load one raw spectral measurement file,
- read the associated acquisition metadata,
- reorder the Hadamard measurements according to the DMD pattern order,
- subtract paired measurements 
- bin along the spectral axis,
- save a single formatted ground-truth cube and a matching measurement matrix.

Reference for understanding the formatting steps before running the full dataset pipeline.

### `reconstruction.py`
This script showing image reconstruction. It downloads or loads example data, unpacks the acquisition metadata, reconstructs cubes from Hadamard measurements, and demonstrates both direct pseudoinverse-style reconstruction and DeepInv-based reconstruction using the `spyrit` measurement operators.

It is mainly an experimental/research script for testing different reconstruction workflows 

### `tools.py`
This file contains shared helper utilities used across the project.

Key pieces include:

- `binArray(...)`: bins an array along a chosen axis with a user-selected reduction function.
- `read_acquisitionData(...)`: parses JSON metadata and reconstructs an acquisition-parameter object.
- `AcquisitionParameters`: a dataclass storing pattern order, dimensions, wavelengths, timing information, and other scan parameters.
- helper logic for loading acquisition metadata and working with the raw measurement structure.

### `metadata_SPC2D.py`
File for decoding raw files produced by the acquisition system.


### `download_data.py`
This script downloads gives an example of how to download sample datasets from the Pilot warehouse API.

### `good_cubeIDs.py`
This file contains a list of dataset IDs / sample identifiers used for downloading good data cubes. 

### `spyrit_dinv_link_example.py`
This script demonstrates how to connect a `spyrit` measurement model to a DeepInv physics operator. It shows how to simulate a Hadamard acquisition, convert the operator into a DeepInv-compatible form, and reconstruct images using adjoint, pseudoinverse, and learned reconstruction methods.

Example of integrating `spyrit` and `deepinv` for inverse problems

### `formatting_output.txt`
This file stores example console output from data-formatting runs, including sample statistics and array shapes. It is useful for debugging and confirming that the preprocessing pipeline is behaving as expected.

## Typical usage

A typical workflow for this repository is:

1. Use `download_data.py` or `good_cubeIDs.py` to fetch raw files.
2. Run `dataset.py` or the logic in `format_data.py` to format the data.
3. Use the resulting files in `ground_truth_formatted/` and `measurements_formatted/` as input to training or reconstruction experiments.
4. Use `reconstruction.py` or `spyrit_dinv_link_example.py` to test inversion/reconstruction models.
