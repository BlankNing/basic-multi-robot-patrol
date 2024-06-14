import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# Initial trust parameters
alpha = 2  # Initial count of successes (high values indicate initial trust)
beta_param = 2  # Initial count of failures (high values indicate initial distrust)

# Generate a range of trust probabilities to visualize the Beta distribution
x = np.linspace(0, 1, 100)  # Probabilities from 0 to 1

# Simulate some interactions with the robot
interactions = 100
success_prob = 0.7  # The actual success probability of the robot

# Keep track of the number of successes and failures
success_count = alpha
failure_count = beta_param

# Record the evolution of the trust distribution
trust_evolution = []

for i in range(interactions):
    if np.random.random() < success_prob:
        success_count += 1
    else:
        failure_count += 1

    # Update the Beta distribution with the new alpha and beta values
    beta_dist = beta(success_count, failure_count)
    trust_evolution.append(beta_dist.pdf(x))

# Plot the evolution of the trust distribution over time
plt.figure(figsize=(12, 6))
for i, trust_dist in enumerate(trust_evolution):
    if i % 10 == 0:
        plt.plot(x, trust_dist, label=f'Interaction {i}')
plt.title("Evolution of Robot Trust with Beta Distribution")
plt.xlabel("Trust Probability")
plt.ylabel("Probability Density")
plt.legend()
plt.show()
