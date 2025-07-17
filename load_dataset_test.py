from datasets import load_dataset

# Allow custom code in dataset repo
dataset = load_dataset("ncbi_disease", split="train", trust_remote_code=True)

# Print the first sample
print(dataset[0])
