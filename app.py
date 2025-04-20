from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This allows cross-origin requests from your frontend

# Function to extract video ID from YouTube URL
def extract_video_id(url):
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    return query.get("v", [None])[0]

# Route to handle transcript requests
@app.route("/api/transcript", methods=["POST"])
def get_transcript():
    data = request.get_json()
    url = data.get("url")
    video_id = extract_video_id(url)

    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        # Fetch the transcript using YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi().get_transcript(video_id)
        # Combine transcript text
        combined_text = "\n".join([line["text"] for line in transcript])
        return jsonify({"transcript": combined_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)
