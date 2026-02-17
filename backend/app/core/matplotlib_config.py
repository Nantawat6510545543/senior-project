import matplotlib

# Use a non-GUI backend (CRITICAL for FastAPI servers)
matplotlib.use("Agg")

import matplotlib.pyplot as plt

# Disable interactive mode globally
plt.ioff()