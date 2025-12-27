import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator

df = pd.read_csv("tests/use.csv")
morgan_gen = rdFingerprintGenerator.GetMorganGenerator(
    radius=2,
    fpSize=2048
)

def smiles_to_fp(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    fp = morgan_gen.GetFingerprint(mol)
    return np.array(fp)

y_ic50 = np.log10(df["ic50_value"].values)
y_association = np.log10(df["association_score"].values)
y_max_phase = df["max_phase"].values
y_target = df["target_symbol"].values

X = np.vstack(
    df["smiles"].apply(smiles_to_fp).dropna().values
)
import numpy as np
import joblib

from catboost import CatBoostRegressor, CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, accuracy_score

RANDOM_SEED = 42

# ==================================================
# 1️⃣ IC50 REGRESSION (FAST)
# ==================================================
X_train, X_val, y_train, y_val = train_test_split(
    X, y_ic50, test_size=0.2, random_state=RANDOM_SEED
)

ic50_model = CatBoostRegressor(
    iterations=300,          # 🔥 FAST
    depth=6,                 # 🔥 shallow
    learning_rate=0.1,       # 🔥 quick convergence
    loss_function="RMSE",
    random_seed=RANDOM_SEED,
    verbose=50
)

ic50_model.fit(
    X_train, y_train,
    eval_set=(X_val, y_val),
    early_stopping_rounds=30
)

print("IC50 R²:", r2_score(y_val, ic50_model.predict(X_val)))

joblib.dump(
    {"model": ic50_model, "radius": 2, "fp_size": 2048},
    "catboost_ic50_fast.pkl"
)

# ==================================================
# 2️⃣ ASSOCIATION SCORE REGRESSION (FAST)
# ==================================================
X_train, X_val, y_train, y_val = train_test_split(
    X, y_association, test_size=0.2, random_state=RANDOM_SEED
)

association_model = CatBoostRegressor(
    iterations=300,
    depth=6,
    learning_rate=0.1,
    loss_function="RMSE",
    random_seed=RANDOM_SEED,
    verbose=50
)

association_model.fit(
    X_train, y_train,
    eval_set=(X_val, y_val),
    early_stopping_rounds=30
)

print("Association R²:", r2_score(y_val, association_model.predict(X_val)))

joblib.dump(
    {"model": association_model, "radius": 2, "fp_size": 2048},
    "catboost_association_fast.pkl"
)

# ==================================================
# 3️⃣ MAX CLINICAL PHASE (FAST CLASSIFIER)
# ==================================================
X_train, X_val, y_train, y_val = train_test_split(
    X, y_max_phase, test_size=0.2, random_state=RANDOM_SEED
)

max_phase_model = CatBoostClassifier(
    iterations=250,
    depth=5,
    learning_rate=0.1,
    loss_function="MultiClass",
    random_seed=RANDOM_SEED,
    verbose=50
)

max_phase_model.fit(
    X_train, y_train,
    eval_set=(X_val, y_val),
    early_stopping_rounds=25
)

print("Max Phase Accuracy:", accuracy_score(
    y_val, max_phase_model.predict(X_val))
)

joblib.dump(
    {"model": max_phase_model, "radius": 2, "fp_size": 2048},
    "catboost_max_phase_fast.pkl"
)

# ==================================================
# 4️⃣ TARGET SYMBOL (FAST + LABEL ENCODER)
# ==================================================
label_encoder = LabelEncoder()
y_target_enc = label_encoder.fit_transform(y_target)

X_train, X_val, y_train, y_val = train_test_split(
    X, y_target_enc, test_size=0.2, random_state=RANDOM_SEED
)

target_model = CatBoostClassifier(
    iterations=300,
    depth=6,
    learning_rate=0.1,
    loss_function="MultiClass",
    random_seed=RANDOM_SEED,
    verbose=50
)

target_model.fit(
    X_train, y_train,
    eval_set=(X_val, y_val),
    early_stopping_rounds=30
)

print("Target Accuracy:", accuracy_score(
    y_val, target_model.predict(X_val))
)

joblib.dump(
    {
        "model": target_model,
        "label_encoder": label_encoder,
        "radius": 2,
        "fp_size": 2048
    },
    "catboost_target_fast.pkl"
)

print("⚡ ALL 4 QUICK MODELS TRAINED & SAVED")
