import ollama

# Assuming you have an Ollama client object
client = ollama.Client(host='http://localhost:11434') 

# List all attributes of the client object
print(dir(client)) 