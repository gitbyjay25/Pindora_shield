import json
import torch
from mol_metrics import Tokenizer
from generator import GeneratorModel, GenSampler

tokenizer = Tokenizer()
tokenizer.build_vocab()
n_tokens = tokenizer.n_tokens

model_path = r"res/save_models/ZINC/TenGAN_0.5/rollout_8/batch_64/druglikeness/g_pretrained.pkl"
model = GeneratorModel(n_tokens=n_tokens, d_model=128, nhead=4, num_encoder_layers=4, dim_feedforward=1024, max_length=200)
state = torch.load(model_path, map_location="cpu")
model.load_state_dict(state, strict=True)
model.eval()

batch_size = 10
sampler = GenSampler(model=model, tokenizer=tokenizer, batch_size=batch_size, max_len=120)

generated_smiles = sampler.sample_multi(100)

output_data = {
    "total_generated": len(generated_smiles),
    "smiles": generated_smiles
}

with open("generated_molecules.json", "w") as f:
    json.dump(output_data, f, indent=2)
