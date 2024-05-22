import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import json

# Data
data = None
with open("metrics.json", "r") as f:
    data = json.load(f)

# Extract data into lists
n = [entry["n"] for entry in data]
e = [entry["e"] for entry in data]
d = [entry["d"] for entry in data]
ln_n = [entry["ln_n"] for entry in data]
ln_e = [entry["ln_e"] for entry in data]
ln_d = [entry["ln_d"] for entry in data]

# Perform linear regression
slope_e, intercept_e, r_value_e, p_value_e, std_err_e = linregress(ln_n, ln_e)
slope_d, intercept_d, r_value_d, p_value_d, std_err_d = linregress(ln_n, ln_d)

# Print the results
print(f"Linear regression for ln_e(n): ln_e = {slope_e} * ln_n + {intercept_e}. R = {r_value_e}")
print(f"Linear regression for ln_d(n): ln_d = {slope_d} * ln_n + {intercept_d}. R = {r_value_d}")

# Plot the data and the linear fit
plt.figure(figsize=(12, 6))

# Plot e vs n
plt.subplot(1, 2, 1)
plt.scatter(ln_n, ln_e, label="Data points", color="blue")
plt.plot(ln_n, np.array(ln_n) * slope_e + intercept_e, label=f"Linear fit: ln_e = {slope_e:.5e} * ln_n + {intercept_e:.5f}", color="red")
plt.xlabel("ln_n")
plt.ylabel("ln_e")
plt.legend()
plt.title("Linear Regression of ln_e vs ln_n")

# Plot d vs n
plt.subplot(1, 2, 2)
plt.scatter(ln_n, ln_d, label="Data points", color="blue")
plt.plot(ln_n, np.array(ln_n) * slope_d + intercept_d, label=f"Linear fit: ln_d = {slope_d:.5e} * ln_n + {intercept_d:.5f}", color="red")
plt.xlabel("ln_n")
plt.ylabel("ln_d")
plt.legend()
plt.title("Linear Regression of ln_d vs ln_n")

plt.tight_layout()
plt.show()
