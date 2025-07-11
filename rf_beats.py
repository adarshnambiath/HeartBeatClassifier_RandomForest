import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier #the random forest itself
from sklearn.metrics import classification_report, confusion_matrix #stuff to analyse how the model is faring
from sklearn.utils import resample #some rare beat types are augmented to give everything a similar priority
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_palette("pastel")

train_data = pd.read_csv("mitbih_train.csv", header = None)
test_data = pd.read_csv("mitbih_test.csv", header = None)

train_data[187] = train_data[187].astype('int')
test_data[187] = test_data[187].astype('int')
print(train_data.shape)
print(test_data.shape)

sns.catplot(x = 187, kind = 'count', data = train_data)
sns.catplot(x = 187, kind = 'count', data = test_data)

df=[]
df.append(train_data[train_data[187] == 0])
df.append(train_data[train_data[187] == 1])
df.append(train_data[train_data[187] == 2])
df.append(train_data[train_data[187] == 3])
df.append(train_data[train_data[187] == 4])

#merely cutting down
df_0_down = resample(df[0], replace=False, n_samples=20000, random_state=64)
#augmenting, just duplication here
df_1_up   = resample(df[1], replace=True, n_samples=20000, random_state=64)
df_2_up   = resample(df[2], replace=True, n_samples=20000, random_state=64)
df_3_up   = resample(df[3], replace=True, n_samples=20000, random_state=64)
df_4_up   = resample(df[4], replace=True, n_samples=20000, random_state=64)

train_balanced = pd.concat([df_0_down, df_1_up, df_2_up, df_3_up, df_4_up])

sns.catplot(x = 187, kind = 'count', data = train_balanced)
#sns.catplot(x = 187, kind = 'count', data = test_data)

beat_map=["Normal Heart Beats", "Supraventricular ectopic beats", "Ventricular ectopic beats", "Fusion Beats", "Unknown Beats"]
for i in range(1,5):
  #sns.set_style("darkgrid")
  plt.figure(figsize=(20,8))
  plt.plot(df[0].iloc[0, 0:187],  label = 'Normal Heart Beats')
  plt.plot(df[i].iloc[0, 0:187],  label = beat_map[i])
  plt.title(f"ECG Normal vs {beat_map[i]}", fontsize = 12)
  plt.xlabel("Time (in ms)")
  plt.ylabel("Heart Beat Amplitude")
  plt.legend()
  plt.show()

train_balanced = train_balanced.sample(frac=1, random_state=64)
X_train = train_balanced.iloc[:, :187].values
y_train = train_balanced.iloc[:, 187].values

X_test = test_data.iloc[:, :187].values
y_test = test_data.iloc[:, 187].values
print(y_test.shape)

clf = RandomForestClassifier(n_estimators=100, random_state=64) #creating and setting parameters for the tree
clf.fit(X_train, y_train) #fitting the data to the forest

y_pred = clf.predict(X_test)

print("Classification Report:\n")
print(classification_report(y_test, y_pred))

conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=[0,1,2,3,4], yticklabels=[0,1,2,3,4])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix - Random Forest")
plt.show()

print()

ratio_matrix = conf_matrix.astype('float').copy()
sums=np.sum(conf_matrix, axis=0)
#print(sums)
for i in range(5):
  for j in range(5):
    ratio_matrix[i][j]=conf_matrix[i][j]/sums[j]

plt.figure(figsize=(8, 6))
sns.heatmap(ratio_matrix, annot=True, fmt=".4f", cmap="Blues", xticklabels=[0,1,2,3,4], yticklabels=[0,1,2,3,4])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix of Ratios - Random Forest")
plt.show()

print()

importances = clf.feature_importances_
plt.figure(figsize=(12, 4))
sns.lineplot(x=range(len(importances)), y=importances)
plt.title("Random Forest Feature Importance")
plt.xlabel("ECG Timepoint (0–186)")
plt.ylabel("Importance")
plt.grid(True)
plt.tight_layout()
plt.show()
