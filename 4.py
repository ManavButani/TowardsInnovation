import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

# Load your data
df = pd.read_csv('data_class.csv')

# Drop any missing values
df.dropna(inplace=True)

# Feature Engineering (Adding SMA, RSI, Volatility)
df['SMA_5'] = df['Close'].rolling(window=5).mean()
df['SMA_10'] = df['Close'].rolling(window=10).mean()
df['Volatility'] = df['Close'].rolling(5).std()

# Fill NaN values created by rolling window
df.fillna(method='bfill', inplace=True)

# Features (X) and Target (y)
X = df[['Close', '% Change']]
y = df['Trade']

# Train-test split (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# **Step 1: Handle Class Imbalance (Using SMOTE)**
smote = SMOTE(sampling_strategy=0.5, random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

# **Step 2: Standardization (Feature Scaling)**
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_resampled)
X_test_scaled = scaler.transform(X_test)

# **Step 3: Train a Better Classifier (XGBoost)**
clf = XGBClassifier(use_label_encoder=False, eval_metric="logloss", scale_pos_weight=2)
clf.fit(X_train_scaled, y_train_resampled)

# **Step 4: Predictions & Evaluation**
y_pred = clf.predict(X_test_scaled)

# **Model Performance Metrics**
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))

# **Step 5: Hyperparameter Tuning (Grid Search)**
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2]
}

grid_search = GridSearchCV(XGBClassifier(use_label_encoder=False, eval_metric="logloss"), 
                           param_grid, scoring='accuracy', cv=5, n_jobs=-1)
grid_search.fit(X_train_scaled, y_train_resampled)

print("Best Parameters:", grid_search.best_params_)