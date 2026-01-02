import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hey there! I am Alok"

tokens = enc.encode(text)
