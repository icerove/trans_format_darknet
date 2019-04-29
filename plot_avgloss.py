import matplotlib.pyplot as plt
import numpy as np


avg_loss = np.array([])
with open("avgloss.txt","r") as f:
    for line in f:
        l = line.split(" ")
        avg_loss = np.append(avg_loss,float(l[3]))
print(avg_loss)

N = len(avg_loss)
X = np.arange(1,N+1)

# plt.scatter(X,avg_loss,c="blue",alpha=0.5)
plt.plot(X, avg_loss)
plt.title("Average loss for training YOLOv3 Model for gun detection")
plt.xlabel("batch")
plt.ylabel("loss")
plt.show()