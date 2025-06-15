# Simple LLM text generation using Hugging Face Transformers
# This script loads a pre-trained GPT-2 model and generates text from a prompt.

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


def main():
    model_name = "gpt2"  # You can change to 'distilgpt2' for a smaller model
    print(f"Loading model '{model_name}' (first run may take a while)...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    prompt = input("Enter a prompt: ")
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=100,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
        num_return_sequences=1,
    )
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("\nGenerated text:\n")
    print(generated)


if __name__ == "__main__":
    main()
