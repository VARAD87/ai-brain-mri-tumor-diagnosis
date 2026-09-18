import matplotlib.pyplot as plt


epochs = [1, 2, 3, 4, 5]

train_loss = [0.7791, 0.4466, 0.3845, 0.2924, 0.2501]
val_loss   = [0.5371, 0.4137, 0.3575, 0.2878, 0.2323]

train_acc = [0.7286, 0.8251, 0.8578, 0.8857, 0.9009]
val_acc   = [0.7796, 0.8429, 0.8497, 0.8825, 0.9108]


plt.figure()
plt.plot(epochs, train_loss, label="Train Loss")
plt.plot(epochs, val_loss, label="Validation Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()
plt.grid()
plt.savefig("reports/figures/loss_curve.png", dpi=300)
plt.show()


plt.figure()
plt.plot(epochs, train_acc, label="Train Accuracy")
plt.plot(epochs, val_acc, label="Validation Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy")
plt.legend()
plt.grid()
plt.savefig("reports/figures/accuracy_curve.png", dpi=300)
plt.show()
