#!/bin/bash
#SBATCH --ntasks=24
#SBATCH --tasks-per-node=24
#SBATCH --partition=debug
#SBATCH --time=00:02:00
#SBATCH --output=%A.out

module purge
module load slurm

ulimit -l unlimited

eval "$(conda shell.bash hook)"
conda activate $GEOS694
python derivatives.py 1
