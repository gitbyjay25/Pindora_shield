from fastapi import APIRouter, HTTPException
from models.schemas import Generate3DInput
from utils.copilot import AzureOpenAIChatClient
from utils.matrix_file import MatrixPredictor

router = APIRouter(
    prefix="/metrics",
    tags=["pindora"],
    responses={404: {"description": "Not found"}},
)

@router.post("/metrics_data")
async def metrics_data(request: Generate3DInput):

    # Validate input first to avoid running predictions on invalid/missing input
    if not request.input_smile or len(request.input_smile.strip()) == 0:
        raise HTTPException(status_code=400, detail="SMILES string is required")

    # Instantiate predictor and client lazily and guard against runtime errors
    try:
        matrix = MatrixPredictor()
    except FileNotFoundError as e:
        # Model files missing or not found
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to initialize predictor")

    try:
        results = matrix.predict_all(request.input_smile)
    except ValueError as e:
        # Invalid SMILES or fingerprinting error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Prediction failed")

    try:
        client = AzureOpenAIChatClient()
        report = client.generate_report_from_smiles_ic50_value_association_score_target_symbol_max_phase(
            request.input_smile,
            results["IC50"],
            results["Association_Score"],
            results["Predicted_Target"],
            results["Max_Clinical_Phase"],
        )
    except Exception as e:
        # If report generation fails, return a 500 with a generic message (avoid leaking secrets)
        raise HTTPException(status_code=500, detail="Failed to generate report")

    return {
        "report": report,
        "status": "success",
    }
