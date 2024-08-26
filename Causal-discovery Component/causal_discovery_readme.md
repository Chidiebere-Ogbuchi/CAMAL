# Testing Causal Discovery Notebook

This Python scripts and notebook contains the implementation and testing of the Causal Discovery algorithm using Py-why (Causal-learn)

## Getting Started

To get started with this project, clone the repository and open the latest version of .py.

### Prerequisites

You need to have the following installed:

- Python 3
- requirement txt

## Following Next steps

### Generating raw data (preferably run on cluster)
1. Open experimental_framework.py scripts and edit visitor, BW and period parameters as directed on the scipt.
2. Run Prototype as usual to open raw data in zip format with name as day_week_BW.zip in the results folder  e.g. Sunday_01_25.100.zip
   
### Preprocessing.py
1. Place all generated zips from above into same directory as the Preprocessing.ipynb
2. Run the script  <!sudo python3 preprocessing.py!>
3. A file named final_results.csv and .zip in the final folder containing the combined results will be generated

### Running the CausalDiscovery_PC Algorithm.py or CausalDiscovery_GES Algorithm.ipynb
1. Place final_results.zip in same directory root directory as causalDiscovery_pc.py
2. Execute code as instructed in notebook.
Run the PC Causal Algorithm or GES Algorithm. Consider adjusting the parameters if needed before executing the notebook in your python environment.
The scripts and notebook contains the implementation of the Causal Discovery algorithms, along with various tests and visualizations.

## Notebook Contents
experimental_framework.py >> preprocessing.py >> CausalDiscovery_PC Algorithm.py or CausalDiscovery_GES Algorithm.ipynb


NB: If there is an existing dataset, the PC or GES scripts can be used directyl.


## Contributing

Contributions are welcome. Please submit a pull request.

## Citation

@article{causallearn,
  title={Causal-learn: Causal Discovery in Python},
  author={Yujia Zheng and Biwei Huang and Wei Chen and Joseph Ramsey and Mingming Gong and Ruichu Cai and Shohei Shimizu and Peter Spirtes and Kun Zhang},
  journal={arXiv preprint arXiv:2307.16405},
  year={2023}
}

