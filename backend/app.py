from flask import Flask, request, jsonify
import llm

app = Flask(__name__)

# @app.route('/api/upload', methods=['POST'])
# def upload_file():
#     text = request.form.get('text')
#     file = request.files.get('file')
#     if file:
#         file.save(f"./uploads/{file.filename}")
#     return jsonify({"message": "File uploaded successfully", "text": text})

# import requests

# url = "https://api.sync.so/v2/generate"

# payload = {
#     "model": "lipsync-1.7.1",
#     "input": [
#         {
#             "type": "video",
#             "url": "https://example.com/your-video.mp4"
#         },
#         {
#             "type": "audio",
#             "url": "https://example.com/your-audio.mp3"
#         }
#     ],
#     "options": {"pads":[0,5,0,0],"output_format":"mp4","sync_mode":"silence","active_speaker":false},
#     "webhookUrl": "https://your-server.com/webhook"
# }
# headers = {
#     "x-api-key": "<api-key>",
#     "Content-Type": "application/json"
# }

# response = requests.request("POST", url, json=payload, headers=headers)

# print(response.text)

@app.route('/api/chat', methods=['POST'])
def chat_handler():
    medium = request.form.get('medium') # "medium" should either be "audio" or "video"
    prompt = request.form.get('prompt') # "prompt" should be plaintext that the user enters in the chat box

    # acquire response from an LLM (abstract out the actual prompting logic)
    text_response = llm.get_response(prompt=prompt) 

    # TODO: optionally filter out non-text characters (LLM could accidentally include formatting chars)

    # acquire tts by feeding in the text_response to our TTS API
    dummy_output = 


if __name__ == '__main__':
    app.run(debug=True)
