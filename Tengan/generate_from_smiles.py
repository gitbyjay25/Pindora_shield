import json
import torch

try:
    from .mol_metrics import Tokenizer
    from .generator import GeneratorModel, GenSampler
except ImportError:
    from mol_metrics import Tokenizer
    from generator import GeneratorModel, GenSampler

try:
    from rdkit import Chem
except ImportError:
    Chem = None

class MoleculeGenerator:
    def __init__(self, model_path: str, batch_size: int = 64, max_len: int = 70):
        self.tokenizer = Tokenizer()
        self.tokenizer.build_vocab()
        n_tokens = self.tokenizer.n_tokens

        self.model = GeneratorModel(
            n_tokens=n_tokens,
            d_model=128,
            nhead=4,
            num_encoder_layers=4,
            dim_feedforward=1024,
            max_length=200
        )
        state = torch.load(model_path, map_location="cpu")
        self.model.load_state_dict(state, strict=True)
        self.model.eval()

        self.sampler = GenSampler(
            model=self.model,
            tokenizer=self.tokenizer,
            batch_size=batch_size,
            max_len=max_len
        )
    
    def _clean_smiles(self, smiles: str) -> str:
        if smiles is None or not smiles.strip():
            return None
        
        smiles = smiles.strip().rstrip('$').strip()
        
        if '$' in smiles:
            smiles = smiles.split('$')[0].strip()
        
        if not smiles or smiles == self.tokenizer.start or smiles == self.tokenizer.end:
            return None
            
        return smiles
    
    def _is_valid_smiles(self, smiles: str) -> bool:
        if Chem is None or not smiles:
            return False
        
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return False
            if mol.GetNumAtoms() < 2:
                return False
            return True
        except:
            return False
    
    def generate(self, num_samples: int):
        return self.sampler.sample_multi(num_samples)
    
    def generate_from_smiles(self, input_smiles: str, num_samples: int):
        cleaned_input = self._clean_smiles(input_smiles)
        
        if not self._is_valid_smiles(cleaned_input):
            print(f"Warning: Invalid input SMILES: {input_smiles}")
            return []
        
        all_samples = []
        batch_size = max(self.sampler.batch_size, num_samples)
        
        for _ in range(2):
            raw_samples = self.sampler.sample_multi(batch_size)
            
            for smiles in raw_samples:
                cleaned = self._clean_smiles(smiles)
                
                if cleaned and self._is_valid_smiles(cleaned):
                    all_samples.append(cleaned)
                    if len(all_samples) >= num_samples:
                        break
            
            if len(all_samples) >= num_samples:
                break
        
        unique_samples = []
        seen = set()
        for smiles in all_samples:
            if smiles not in seen:
                unique_samples.append(smiles)
                seen.add(smiles)
        
        return unique_samples[:num_samples]