#!/bin/bash -l
# Job Name
#SBATCH --job-name=GVAE
# Output File Name
#SBATCH --output=GVAE_output.txt
# Error File Name
#SBATCH --error=GVAE_error.log
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

# python3 train.py --model 'GVAE' --dataset 'Data/imputed_SweatBinary.csv' --target_col_ix 18 --k 3 --num_obs 100 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/cleveland_heart.csv' --target_col_ix 13 --k 5 --num_obs 10 --epochs 200

python3 train.py --model 'GVAE' --dataset 'Data/urban_land.csv' --target_col_ix 0 --k 10 --num_obs 10 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/mammography.csv' --target_col_ix 5 --k 5 --num_obs 100 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/immunotherapy.csv' --target_col_ix 7 --k 8 --num_obs 100 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/cryotherapy.csv' --target_col_ix 6 --k 6 --num_obs 100 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/caesarian.csv' --target_col_ix 5 --k 6 --num_obs 100 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/cervical.csv' --target_col_ix 19 --k 3 --num_obs 100 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/breast.csv' --target_col_ix 10 --k 3 --num_obs 100 --epochs 200

# python3 train.py --model 'GVAE' --dataset 'Data/post_operative.csv' --target_col_ix 8 --k 6 --num_obs 100 --epochs 200

