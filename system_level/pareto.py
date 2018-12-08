import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import normalize


weight_light_range = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
light_values =  np.array([717.8, 732.55, 741.41, 747.8, 749.89, 759.34, 753.87, 759.27, 759.07])
cost_values = np.array([173.73, 176.67, 181.17, 184.98, 186.87, 191.09, 189.64, 192.12, 194.56])

light_values = light_values / np.linalg.norm(light_values)
cost_values = cost_values / np.linalg.norm(cost_values)



plot = plt.figure()
plt.plot(weight_light_range, light_values)
plt.plot(weight_light_range, cost_values)
plt.legend(['Light', 'Cost'])
plt.title('Pareto Set ')
plt.xlabel('Light Weight Factor')
plt.ylabel('Normalised Minimum Light Intensity and Cost')
plt.show()