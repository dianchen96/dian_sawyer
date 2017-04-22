import numpy as np
import matplotlib.pyplot as plt
import sys
import csv

if __name__ == "__main__":
	with open('./traj/%s' %sys.argv[1], 'r') as f:
		reader = csv.DictReader(f)
		readings = []
		for l in reader:
			readings.append(l.values())

	data = np.asarray(readings)
	plt.plot(data[:, 0])
	plt.show()