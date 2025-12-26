import os
import joblib
import pandas as pd


class PindoraShield:
    """
    PindoraShield
    -------------
    Unified inference engine for molecular prediction models.

    Loaded models:
    - IC50 regression
    - Association score regression
    - max phase  classifier
    - pChEMBL baseline regression
    - Target symbol classifier (exploratory)
    """

    def __init__(self, model_dir: str = "matriX_model"):
        self.model_dir = model_dir
        self._validate_model_dir()
        self._load_models()

    # -----------------------
    # Setup
    # -----------------------
    def _validate_model_dir(self):
        if not os.path.isdir(self.model_dir):
            raise FileNotFoundError(
                f"Model directory not found: {self.model_dir}"
            )

    def _load_models(self):
        self.ic50_model = joblib.load(
            os.path.join(self.model_dir, "ic50_catboost.pkl")
        )
        self.assoc_model = joblib.load(
            os.path.join(self.model_dir, "association_catboost.pkl")
        )
        self.phase_model = joblib.load(
            os.path.join(self.model_dir, "maxphase_cb.pkl")
        )
        self.pchembl_model = joblib.load(
            os.path.join(self.model_dir, "pchembl_cb.pkl")
        )
        self.target_model = joblib.load(
            os.path.join(self.model_dir, "trget_symbol.pkl")
        )

    # -----------------------
    # Core predictions
    # -----------------------
    def predict_ic50(self, X: pd.DataFrame):
        return self.ic50_model.predict(X)

    def predict_association(self, X: pd.DataFrame):
        return self.assoc_model.predict(X)

    def predict_phase_probability(self, X: pd.DataFrame):
        return self.phase_model.predict_proba(X)[:, 1]

    def predict_pchembl(self, X: pd.DataFrame):
        return self.pchembl_model.predict(X)

    def predict_target(self, X: pd.DataFrame):
        return self.target_model.predict(X)

    # -----------------------
    # Unified inference
    # -----------------------
    def predict_all(self, X: pd.DataFrame):
        """
        Run all models and return predictions.
        """
        return {
            "log_ic50": self.predict_ic50(X),
            "association_score": self.predict_association(X),
            "phase4_probability": self.predict_phase_probability(X),
            "pchembl": self.predict_pchembl(X),
            "target_symbol": self.predict_target(X),
        }

    # -----------------------
    # Sanity test
    # -----------------------
    def sanity_check(self, X: pd.DataFrame, n: int = 5):
        """
        Lightweight internal check to verify model loading and inference.
        """
        outputs = self.predict_all(X)

        for key, values in outputs.items():
            print(f"{key}: {values[:n]}")

        return outputs
