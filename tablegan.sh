#!/bin/bash -l
# Job Name
#SBATCH --job-name=TableGAN
# Output File Name
#SBATCH --output=TableGAN_output.txt
# Error File Name
#SBATCH --error=TableGAN_error.log
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

python3 train.py --model 'tablegan' --file 'Data/imputed_SweatBinary.csv' --cat_col "('Sex','Recerational.Athlete','Birth.Control','PsychDistress')" --target_col_ix 18 --k 3 --num_obs 100 --epochs 500