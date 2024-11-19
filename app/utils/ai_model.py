# from transformers import AutoTokenizer, AutoModelForCausalLM

# # Load the gpt-neo 
# # MODEL_NAME = "EleutherAI/gpt-neo-1.3B"
# # tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# # gpt_model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# def generate_response(prompt: str, max_length: int = 200):
#     """
#     Generates a response using the loaded gpt-neo .
#     :param prompt: The input prompt for the model.
#     :param max_length: Maximum length of the generated response.
#     :return: The model's response as a string.
#     """
#     inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
#     outputs = gpt_model.generate(inputs["input_ids"], max_length=max_length, num_return_sequences=1)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)
