# Testing MAML Notebook

This Python scripts and notebook contains the implementation and testing of the MAML algorithm using Pytorch

## Getting Started

To get started with this project, clone the repository.

### Prerequisites

You need to have the following installed:

- Python 3
- requirement txt

## Following Next steps

NB: The Generated raw data are stored in the RAW EDICT files. Another batch can be geratred using the EDICT simulator (If installed)
1. The pre-processed and aggregrated CSV for the 3 scenarios are in the respective folders:
- **Scenario 1 - Normal Loaded System**: The system is tested with moderate data traffic to evaluate MAML's efficiency in predicting performance metrics. The goal is to assess its adaptability to new network configurations based on different application categories.
- **Scenario 2 - Additional Application Category**: This scenario adds a new application category, increasing data flows to the broker. It examines MAML's ability to adapt and maintain performance under unforeseen prioritization settings with more complex network demands.
- **Scenario 3 - Scalability**: The focus is on evaluating MAML's scalability by increasing subscriptions from 20 to 100. It tests the model's capacity to predict and adapt to higher data loads and subscription volumes, reflecting real-world expansion scenarios.

   
### EDICT output - Preprocessing.ipynb
1. Place the scenario files as instructed in the Preprocessing to obtain the final dataset for training the MAML

### Running the MAML.ipynb
1. Place final scenario files in same directory root directory as MAML.ipynb
2. Run each scenario separately by folloowing the instructiion



## Contributing

Contributions are welcome. Please submit a pull request.


