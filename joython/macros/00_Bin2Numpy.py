import sys
sys.path.insert(0, '../')

import pandas as pd
from lib.first_data_process import Bin2Np_excel


# ## First Week: Apsaia VIS
# in_path ="/media/rodrigoa/DiscoDuro/SBND_XA_PDE/APSAIA_VIS/"
# out_path="/media/rodrigoa/DiscoDuro/SBND_XA_PDE/APSAIA_VIS/joython/"

## Second Week: Apsaia VUV
in_path ="/media/rodrigoa/DiscoDuro/SBND_XA_PDE/APSAIA_VUV/"
out_path="/media/rodrigoa/DiscoDuro/SBND_XA_PDE/APSAIA_VUV/joython/"

Bin2Np_excel("APSAIA_VUV.xlsx",compressed=False,i_path=in_path,o_path=out_path)
