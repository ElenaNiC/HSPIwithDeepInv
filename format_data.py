
#%% -------------------- FORMATTING MEASUREMENTS ---------------------------------------------------------
from tools import read_acquisitionData
import numpy as np
import os

os.makedirs("measurements_formatted", exist_ok=True)


# for each measurement file: 
# read correspondning meta_Data pattern list
# unsplit and reorder measurements according to pattern list
# bin spectrally and subsample measurement wise


# example for one file:


# Get spectral data
raw_data = np.load("./measurements/obj_Cat_bicolor_thin_overlap_source_white_LED_Walsh_im_64x64_ti_9ms_zoom_x1_spectraldata.npz", allow_pickle=True)["spectral_data"]
P, L = raw_data.shape

# Get pattern order
meta_path = "./metadata/obj_Cat_bicolor_thin_overlap_source_white_LED_Walsh_im_64x64_ti_9ms_zoom_x1_metadata.json"
meta = read_acquisitionData(meta_path)
acquisition_parameters = meta['acquisition_params']


wavelengths = acquisition_parameters.wavelengths # list of wavelengths measure
N = acquisition_parameters.pattern_dimension_x  # probably np.sqrt(P//2) for uncompressed sensing
s = acquisition_parameters.patterns_wp # order of acquisition patterns - some acquisitions taken in non crono order


#%% REORDERING
import re
# patterns = [int(x) for x in re.findall(r'np\.int32\((\d+)\)', s)]
# ind = np.array(patterns[0::2])//2 # corresponding hadamard rows


order = acquisition_parameters.patterns # order of acquisition patterns
ind = np.array(order) # corresponding acquisition rows

m_reordered = np.zeros((P, L)) # create space first
m_reordered[ind, :]  = raw_data # place rows of m_unsplit following order of ind :)
m_unsplit = m_reordered[0::2, :] - m_reordered[1::2, :]


print("raw_data: ", raw_data.shape)
print("m_reordered: ", m_reordered.shape)
print("m_unsplit: ", m_unsplit.shape)
#%% BINNING
# bin along spectral dimension 

from tools import binArray
m_binned = binArray(m_unsplit, -1, 4, 4, np.sum)

K = 1024 # or whatever number of measures you want to use
m_subsampled = m_binned[0:K, :]
np.save(f"measurements_formatted/y_{K}_17", m_subsampled)



#%% --------------------- FORMATTING GT -------------------------------------------------------------------
import os
os.makedirs("ground_truth_formatted", exist_ok=True)

# bin spectrally
gt = np.load("./ground_truth/obj_Cat_bicolor_thin_overlap_source_white_LED_Walsh_im_64x64_ti_9ms_zoom_x1_had_reco.npz", allow_pickle=True)["arr_0"]
gt = binArray(gt, -1, 4, 4, np.sum)
np.save(f"ground_truth_formatted/cube17", gt)


# %% ---------------- CHECK --------------------------------------------------------------------------------
import matplotlib.pyplot as plt
from spyrit.misc.walsh_hadamard import walsh_matrix_2d

i = 17
gt_recon = np.load(f"ground_truth_formatted/cube{i}.npy").squeeze()
y = np.load(f"measurements_formatted/y_{K}_{i}.npy")


print("cube:", gt_recon.shape)
print("sybsampled measurements:", y.shape)
Nx, Ny, L = gt_recon.shape


plt.imshow(gt_recon.sum(-1)[:,:])
plt.title("GT")
plt.figure()

# reconstruct
H = walsh_matrix_2d(Nx)
f = np.matmul(H,m_binned.sum(-1))
f_presum= np.reshape(f, (Nx,Ny))// (Nx*Ny)

plt.imshow(f_presum) # plot wavelength sum
plt.title("presummed Direct Reconstruction (all measures)")


# %%
