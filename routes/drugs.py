from fastapi import APIRouter, HTTPException
from models.schemas import TextInput, TextResponse, Generate3DInput, Generate3DResponse
from pindora import Pindora
from utils.generate_3d import Molecule3DGenerator
import json

router = APIRouter(
    prefix="/api",
    tags=["pindora"],
    responses={404: {"description": "Not found"}},
)

@router.post("/drug_konsi_doge", response_model=TextResponse)
async def process_text(request: TextInput):
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    print("Received text:", request.text)
    Pindora_instance = Pindora()
    mol_gen = Pindora_instance.drug_discovery_pipeline(request.text)


    return {
        "input_text": request.text,
        "results": mol_gen,
        "status": "success",
        "message": f"Drug discovery pipeline completed. Found {len(mol_gen)} molecules."
    }

@router.post("/generate-3d", response_model=Generate3DResponse)
async def generate_3d_endpoint(request: Generate3DInput):
    if not request.input_smile or len(request.input_smile.strip()) == 0:
        raise HTTPException(status_code=400, detail="SMILES string is required")

    try:
        generator = Molecule3DGenerator()
        path = generator._generate_3d(request.input_smile)
        return {
            "message": "3D model generated successfully",
            "file_path": path,
            "status": "success",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))