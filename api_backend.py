from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import uvicorn

app = FastAPI(title="Placement Metrics API")

# CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data and train model
df = pd.read_csv('data_sample.csv')
features = ['gpa', 'test_score', 'work_experience']
X = df[features]
y = df['placed']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
accuracy = accuracy_score(y_test, model.predict(X_test))

@app.get("/metrics")
def get_metrics():
    total_students = len(df)
    placement_rate = df['placed'].mean() * 100
    avg_package = df[df['placed']==1]['package_placed'].mean()
    top_company = df[df['placed']==1]['company'].value_counts().index[0]
    return {
        "total_students": total_students,
        "placement_rate": round(placement_rate, 1),
        "avg_package": round(avg_package, 1),
        "top_company": top_company,
        "model_accuracy": round(accuracy, 2)
    }

@app.get("/predict")
def predict_placement(gpa: float, test_score: int, work_experience: int):
    pred_data = np.array([[gpa, test_score, work_experience]])
    probability = model.predict_proba(pred_data)[0][1]
    return {"placement_probability": round(probability, 2)}

@app.get("/data")
def get_data(branch: str = "all"):
    if branch == "all":
        return df.to_dict('records')
    else:
        filtered = df[df['branch'] == branch].to_dict('records')
        return filtered

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
