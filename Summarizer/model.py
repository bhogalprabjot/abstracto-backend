import pickle
import numpy as np
import pandas as pd
import math
import io
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_excel(r'Regression_Testing_Database.xlsx')
#print(df.head())

x = df.loc[:, "No. of Lines in Article"]
y = df.loc[:, "No. of Lines in Summary"]

X = np.array(x)
Y = np.array(y)
X = X.reshape(-1,1)
Y = Y.reshape(-1,1)

reg = LinearRegression().fit(X, Y)


pickle.dump(reg, open("model.pkl", "wb"))

'''
For seeing the plot of No of Lines in Article vs No of lines in Summary
'''
# # x axis values
# x = df.loc[:, "No. of Lines in Article"]
# # corresponding y axis values
# y = df.loc[:, "No. of Lines in Summary"]

# plt.figure(figsize=(15,15))
# plt.scatter(x, y)
  
# # naming the x axis
# plt.xlabel("No. of Lines in Article")
# # naming the y axis
# plt.ylabel("No. of Lines in Summary")
  
# # giving a title to my graph
# plt.title('Analysis')
  
# # function to show the plot
# plt.show()