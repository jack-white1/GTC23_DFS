# AstroAccelerate DFS Installation and Usage

**Root/admin permissions are required by the NVML library**

## Download
1. Clone the git repo 
`git clone https://github.com/jack-white1/GTC23_DFS`
2. Change into the created directory 
`cd GTC23_DFS/astro-accelerate-energy-optimise/`
3. Download the input data file (this might take ~20 mins as OxFile is quite slow)
`wget https://oxfile.ox.ac.uk/oxfile/files/121723636254ADF8CA7/E5D050BF-47EA-47F3-A96B-661C0A894EE2/SKA_STD_10ms.fil`

## Setup
4. Change the python script to include the correct file path
    1. Copy the output from running `pwd`
    2. Open `dfs.py` in text editor of choice
    3. On line 50, change `/home/PATH/TO/PARENT/FOLDER/astro-accelerate-energy-optimise/` to the full path to the folder ending with `/astro-accelerate-energy-optimise/`
5. Change AstroAccelerate input file to point to the .fil file
    1. Open `ska_input.txt` in text editor of choice
    2.  Change last line of `ska_input.txt` to include the path of the `.fil` file downloaded in step 3, e.g. `file /home/user/GTC23_DFS/astro-accelerate-energy-optimise/SKA_STD_10ms.fil`
    3. Save the file
6. **This step is only required if a gencode other than `sm_90` is required, update the gencode in the Makefiles:**
    1. `cd astro-accelerate-power-bfloat/astro-accelerate/`
    2. Open `Makefile` in text editor of choice
    3. change `$(GENCODE_SM90)` to `$(GENCODE_SMXX)` on line 39
    4. save the Makefile
    5. `cd ../../astro-accelerate-power-single/astro-accelerate/`
    6. Open `Makefile` in text editor of choice
    7. change `$(GENCODE_SM90)` to `$(GENCODE_SMXX)` on line 39
    8. save the Makefile
    9. `cd ../..`
7. Make the executables for the bfloat16 and single precision versions of the code
	1. `cd astro-accelerate-power-bfloat/astro-accelerate/`
	2. `make`
	3. `cd ../../astro-accelerate-power-single/astro-accelerate/`
	4. `make`

## Run
8. Run the code from the `/GTC23_DFS/astro-accelerate-energy-optimise/` directory using `sudo python3 dfs.py`
9. The output should be saved in `.json` format in files called `bfloatDFSresults.json` and `singleDFSresults.json`

   
