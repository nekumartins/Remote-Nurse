import numpy as np

# Define the number of individuals in the dataset
n_individuals = 100

# Define the data parameters
age = np.random.randint(18, 65, n_individuals)
gender = np.random.randint(0, 2, n_individuals)
med_history = np.random.randint(0, 4, n_individuals)
systolic_bp = np.random.randint(100, 160, n_individuals)
diastolic_bp = np.random.randint(60, 100, n_individuals)
heart_rate = np.random.randint(60, 100, n_individuals)
hypertension_risk_threshold = 140
