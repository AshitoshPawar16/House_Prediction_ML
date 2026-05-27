import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

data = pd.read_csv("house_data.csv")

X = data[
    [
        "area",
        "bedrooms",
        "bathrooms",
        "floors",
        "age"
    ]
]

y = data["price"]

model = LinearRegression()
model.fit(X, y)

pickle.dump(
    model,
    open("model.pkl", "wb")
)

print("Model trained successfully")