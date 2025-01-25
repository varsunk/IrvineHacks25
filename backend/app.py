from flask import Flask, request, jsonify
import llm
import tts
from flask_cors import CORS

app = Flask(__name__)

chat_history = []

# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     text = request.form.get('text')
#     file = request.files.get('file')
#     if file:
#         file.save(f"./uploads/{file.filename}")
#     return jsonify({"message": "File uploaded successfully", "text": text})

CORS(app, resources={r"/api/*": {"origins": "http://localhost:5174"}})


@app.route('/api/chat', methods=['POST'])
def chat_handler():
    global chat_history
    
    data = request.get_json()  # Get the JSON body as a dictionary

    # Validate the presence of 'medium' and 'prompt'
    medium = data.get('medium')  # This will now work with JSON
    prompt = data.get('prompt')  # This will now work with JSON
    
    # medium = request.form.get('medium') # "medium" should either be "text", "audio", or "video"
    # prompt = request.form.get('prompt') # "prompt" should be plaintext that the user enters in the chat box

    # parameter validation
    if not medium or medium not in ["text", "audio", "video"]:
        return jsonify({"error": "Invalid 'medium' parameter. Accepted values are 'text', 'audio', or 'video'."}), 400

    if not prompt:
        return jsonify({"error": "Missing 'prompt' parameter."}), 400

    # acquire response from an LLM (abstract out the actual prompting logic) and update chat history
    text_response, hist_record = llm.get_response(history=chat_history, prompt=prompt) 
    chat_history += hist_record
    print("Current history:")
    for msg in chat_history:
        print(msg)

    # TODO: optionally filter out non-text characters (LLM could accidentally include formatting)

    response = {
        "text_response": text_response,
        "file_url": None
    }

    if medium == "text":
        return jsonify(response)
    elif medium == "audio":
        # acquire tts by feeding in the text_response to our TTS API
        tts_file = tts.generate_tts(text_response)
        response["file_url"] = tts_file
        
        return jsonify(response)
    elif medium == "video":
        # acquire tts by feeding in the text_response to our TTS API
        dummy_output = None
        # acquire video by feeding the TTS audio and one of our hosted videos into our LipSync API
        dummy_output2 = None



    


if __name__ == '__main__':
    app.run(debug=True)
