#!/bin/bash -l
# Job Name
#SBATCH --job-name=VEEGAN
# Output File Name
#SBATCH --output=VEEGAN_output.txt
# Error File Name
#SBATCH --error=VEEGAN_error.log
# Number of Nodes to Use
#SBATCH --nodes=1
# Number of Tasks per Node
#SBATCH --tasks-per-node=2
# Which Partition to Use
#SBATCH --partition=gpucompute
# Memory to allocate in Each Node
#SBATCH --mem=30GB
# Number of GPUs to use per Node
#SBATCH --gres=gpu:2

# Load module
module load cuda11.1/toolkit/11.1.1

# Activate Conda Env
conda activate deepmtd

# python3 train.py --model 'veegan' --dataset 'Data/imputed_SweatBinary.csv' --cat_col "('Sex','Recerational.Athlete','Birth.Control','PsychDistress')" --target_col_ix 18 --k 3 --num_obs 100 --epochs 500

python3 train.py --model 'veegan' --dataset 'Data/urban_land.csv' --target_col_ix 0 --k 3 --num_obs 100 --epochs 500
