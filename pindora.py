from Tengan.generate_from_smiles import MoleculeGenerator
from fetch_data import FetchData
from copilot import AzureOpenAIChatClient
import json

data_processor = FetchData()
copilot=AzureOpenAIChatClient()
model_path = "Tengan/res/save_models/ZINC/TenGAN_0.5/rollout_8/batch_64/druglikeness/g_pretrained.pkl"
generator = MoleculeGenerator(
    model_path=model_path,
    batch_size=8,
    max_len=120
)

disease_c=copilot.generate_desease_name_from_prompt("i have breast cancer and diabetes type 2")
diseases=json.loads(disease_c)["desease"]
all_data = []

for disease_name in diseases:
    efo_ids = data_processor.map_disease_to_efo(disease_name)
    print(f"Disease: {disease_name} -> EFO IDs: {efo_ids}")
    if not efo_ids:
        print(f"No EFO ID found for disease: {disease_name}")
    for i in efo_ids:
        targets = data_processor.get_associated_targets(i, max_targets=50)
        all_data = []
        for i, target in enumerate(targets):
            drugs = data_processor.get_known_drugs_for_target(target["target_id"], max_drugs=10)
            if len(drugs)==0:
                continue
            for j, drug in enumerate(drugs):
                ic50_data = data_processor.get_ic50_data_for_molecule(drug["drug_id"], limit=100)
                features = data_processor.get_molecule_properties(drug["drug_id"])
                for ic50 in ic50_data:
                    row = {
                        "disease_name": disease_name,
                        "efo_id": i,
                        
                        # Target information
                        "target_id": target["target_id"],
                        "target_symbol": target["approved_symbol"],
                        "association_score": target["association_score"],
                        
                        # Drug information
                        "drug_id": drug["drug_id"],
                        "drug_name": drug["pref_name"],
                        "clinical_phase": drug["phase"],
                        
                        # IC50 bioactivity data
                        "ic50_value": ic50["standard_value"],
                        "ic50_units": ic50["standard_units"],
                        "target_chembl_id": ic50["target_chembl_id"],
                        "assay_chembl_id": ic50["assay_chembl_id"],
                        "pchembl_value": ic50["pchembl_value"]
                    }
                    for key, value in features.items():
                        if key != "molecule_chembl_id" and value is not None:
                            row[key] = value

                    all_data.append(row)
                    break
                break

print(f"Total records collected: {len(all_data)}")

gen_mol=[]
for i in all_data:
    input_smiles=i["smiles"]
    results = generator.generate_from_smiles(input_smiles, 5, model_path)
    gen_mol.append({"input_smile": input_smiles, "generated_smiles": results})
    for j, smiles in enumerate(results, 1):
        print(f"Input SMILES: {input_smiles} -> Generated {j}. {smiles}")

with open("generated_molecules.json", "w", encoding="utf-8") as f:
    json.dump(gen_mol, f, indent=2)