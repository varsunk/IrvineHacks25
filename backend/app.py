from flask import Flask, request, jsonify
import llm
import tts
import lipsync
from flask_cors import CORS

app = Flask(__name__)

chat_history = []
pending_jobs = {}

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
    global chat_history, pending_jobs
    
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
        tts_file = tts.generate_tts(text_response)
        lipsync_response = lipsync.generate_lipsync(tts_file)

        if lipsync_response.status_code == 200:
            # Parse the job ID from the response
            job_id = lipsync_response.json().get('job_id')
            pending_jobs[job_id] = {"status": "processing", "file_url": None}
            return jsonify({"text_response": text_response, "job_id": job_id})
        else:
            return jsonify({"error": "Failed to initiate video generation."}), 500


@app.route('/api/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    signature = request.headers.get('Sync-Signature')

    # Verify webhook signature
    if not lipsync.verify_signature(data, signature):
        return jsonify({'message': 'Invalid signature'}), 400

    job_id = data.get('id')
    file_url = data.get('outputUrl')

    if job_id in pending_jobs:
        pending_jobs[job_id]["status"] = "completed"
        pending_jobs[job_id]["file_url"] = file_url

    return jsonify({'message': 'Webhook processed successfully'}), 200


@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    if job_id not in pending_jobs:
        return jsonify({"error": "Job ID not found"}), 404
    return jsonify(pending_jobs[job_id])


if __name__ == '__main__':
    app.run(debug=True)
