import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hey there! I am Alok"

tokens = enc.encode(text)

print ("Tokens", tokens)

# Tokens [25216, 1354, 0, 357, 939, 1667, 525]

decoded = enc.decode([25216, 1354, 0, 357, 939, 1667, 525])
print("decoded", decoded)