import json
import random

# Save messages for retrieval later on
def get_recent_messages():

  # Define the file name
  file_name = "stored_data.json"
  learn_instruction = {"role": "system", 
                       "content": "Tu nombre es Mia y eres asesor de estándares de UL Solutions. Todas tus preguntas y respuestas seran unicamente en idioma español y acerca UL. Siempre saluda y pregunta por el producto para el cual se desea buscar la norma o estandard UL. Explicar los requisitos de la norma que aplican una vez encontrado el producto. Mantenga las respuestas en menos de 12 palabras y siempre confirme con una pregunta el nombre del producto antes de encontrar la norma UL. Si te preguntan cosas distintas a UL Solutions por favor responde que puedes responder unicamente preguntas sobre UL Si te preguntan por la guia de informacion del producto intenta buscar el link en internet."}
                      #  "Quiero que actúes como un asesor de UL Solutions. Ayudame a identificar normas de productos que el cliente diga. Tu nombre es Mia, el usuario es Arturo. Manten tus respuestas en no mas de 30 palabras."}
  
  # Initialize messages
  messages = []

  # Add Random Element
  x = random.uniform(0, 1)
  if x < 0.2:
    learn_instruction["content"] = learn_instruction["content"] + "Tu respuesta debe ser en tono formal, calmado, serio y sin ahogarse. "
  elif x < 0.5:
    learn_instruction["content"] = learn_instruction["content"] + "Su respuesta puede incluir normas similares o preguntar si el producto solicitado es correcto. "
  else:
    learn_instruction["content"] = learn_instruction["content"] + "Tu respuesta debe confirmar primero el producto antes de buscar la norma."

  # Append instruction to message
  messages.append(learn_instruction)

  # Get last messages
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      
      # Append last 5 rows of data
      if data:
        if len(data) < 5:
          for item in data:
            messages.append(item)
        else:
          for item in data[-5:]:
            messages.append(item)
  except Exception as e:
    print(e)
    pass

  
  # Return messages
  return messages

# Save messages for retrieval later on
def store_messages(request_message, response_message):

  # Define the file name
  file_name = "stored_data.json"

  # Get recent messages
  messages = get_recent_messages()[1:]

  # Add messages to data
  user_message = {"role": "user", "content": request_message}
  assistant_message = {"role": "assistant", "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)

  # Save the updated file
  with open(file_name, "w") as f:
    json.dump(messages, f)

# Save messages for retrieval later on
def reset_messages():

  # Define the file name
  file_name = "stored_data.json"

  # Write an empty file
  open(file_name, "w")
