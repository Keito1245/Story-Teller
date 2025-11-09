import os
import io
# Import 'url_for' from Flask (this is new)
from flask import Flask, render_template, request, jsonify, send_file, url_for
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from dotenv import load_dotenv

# Load environment variables (your API key)
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Initialize the ElevenLabs client
try:
    client = ElevenLabs(
        api_key=os.environ.get("ELEVENLABS_API_KEY")
    )
    if not os.environ.get("ELEVENLABS_API_KEY"):
        print("API key not found. Please check your .env file.")
    else:
        print("ElevenLabs client initialized.")
except Exception as e:
    print(f"Error initializing ElevenLabs client: {e}")
    client = None

# --- Your Stories Data ---
# UPDATED: 'cover_image' is now just the filename
all_stories = [
    {
        "id": "remy_rabbit",
        "title": "Remy the Curious Rabbit",
        "author": "RR",
        "cover_image": "curious_rabbit.jpg", # <-- CHANGED
        "pages": [
            "Once upon a time, in a cozy little cottage nestled in the woods, lived a curious rabbit named Remy.",
            "Remy loved to explore. One sunny morning, he found a shiny, golden key half-buried under an oak tree.",
            "He wondered, 'What does this key unlock?' His adventure was about to begin.",
            "The key fit a small, wooden box he'd never noticed before. Inside, there was a map with a single red 'X'.",
            "Remy's heart thumped with excitement. He packed a small bag with a carrot and set off on his grand adventure.",
            "After a long journey, he found the 'X' marked spot. It was a giant, ancient tree with a hidden door. The end."
        ]
    },
    {
        "id": "space_cat",
        "title": "A Cat in Space",
        "author": "LS",
        "cover_image": "cat_in_space.jpg", # <-- CHANGED
        "pages": [
            "Meet Whiskers, a cat with dreams as vast as the cosmos. One night, a tiny alien ship landed in his backyard.",
            "The aliens, friendly and purple, invited Whiskers for a ride. He packed his favorite tuna and hopped aboard.",
            "They soared past stars and nebulae, Whiskers gazing out with wide, wondering eyes.",
            "On a distant planet made of yarn balls, he played with adorable alien kittens. It was the best day ever!",
            "Finally, the purple aliens brought Whiskers home, leaving him with stardust in his fur and stories to tell. The end."
        ]
    },
    {
        "id": "magic_forest",
        "title": "The Whispering Forest",
        "author": "Tales",
        "cover_image": "whispering_forest.jpg", # <-- CHANGED
        "pages": [
            "Elara was a young girl who stumbled upon a shimmering path leading into the Whispering Forest.",
            "Trees there had leaves that glowed, and flowers sang gentle lullabies. Magical creatures peeked from behind ancient trunks.",
            "She met a grumpy gnome who guarded a crystal spring. He offered her a sip of its sparkling water.",
            "With each sip, Elara felt a little wiser. The forest seemed to share its ancient secrets with her.",
            "As dusk fell, Elara returned home, her heart full of wonder and her pockets jingling with enchanted pebbles. The end."
        ]
    }
]
# ---

@app.route('/')
def index():
    """ Serves the main HTML page from the 'templates' folder. """
    return render_template('index.html')

@app.route('/get_all_stories', methods=['GET'])
def get_all_stories():
    """
    UPDATED: This function now builds the correct URL for each image.
    """
    story_list = []
    for s in all_stories:
        story_list.append({
            "id": s["id"],
            "title": s["title"],
            "author": s["author"],
            # This generates the correct URL like '/static/images/remy_rabbit.jpeg'
            "cover_image": url_for('static', filename=f'images/{s["cover_image"]}')
        })
    return jsonify({"stories": story_list})

@app.route('/get_page_content', methods=['POST'])
def get_page_content():
    """ Gets the text content for a specific page number for a given book. """
    try:
        story_id = request.json.get('storyId')
        page_number = int(request.json.get('page'))

        current_story = next((s for s in all_stories if s["id"] == story_id), None)

        if not current_story:
            return jsonify({"error": "Story not found"}), 404

        if 0 <= page_number < len(current_story["pages"]):
            return jsonify({"text": current_story["pages"][page_number]})
        else:
            # End of story or page not found
            return jsonify({"error": "Page not found"}), 404
    except Exception as e:
        print(f"Error in get_page_content: {e}")
        return jsonify({"error": str(e)}), 400

# This is your working audio function, UNCHANGED
@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    """ Generates audio from text and returns it as an MP3 file. """
    if not client:
        return jsonify({"error": "ElevenLabs client not initialized."}), 500

    text_to_speak = request.json.get('text')
    if not text_to_speak:
        return jsonify({"error": "No text provided"}), 400

    try:
        # --- NEW CODE using the lower-level function ---
        # This function returns an *iterator* (audio chunks)
        audio_data_iterator = client.text_to_speech.convert(
            text=text_to_speak,
            voice_id='JBFqnCBsd6RMkjVDRZzb', # Your new Voice ID
            model_id='eleven_multilingual_v2', # Model ID passed directly
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
                style=0.0,
                use_speaker_boost=True
            )
        )

        # We must assemble the audio chunks into a single bytes object
        audio_data = b"".join(audio_data_iterator)

        # --- Send Audio Back ---
        # This part is the same as before
        return send_file(
            io.BytesIO(audio_data),
            mimetype='audio/mpeg',
            as_attachment=False
        )

    except Exception as e:
        # This will now catch any new errors
        print(f"Error generating audio: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)