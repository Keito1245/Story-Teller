AI Storybook Reader

This is a web application that presents a virtual bookshelf of stories. Users can select a book and read it page-by-page, with a "Read Aloud" feature powered by the ElevenLabs API.

(To use this screenshot, add your image_7cf60b.png file to the main folder of your repository)

Features

Virtual Bookshelf: Browse a gallery of book covers.

Interactive Reader: A clean interface for reading page-by-page.

Text-to-Speech: Generates high-quality audio for any story page using the ElevenLabs API.

Customizable: Easily add new books, pages, and cover art by editing the app.py file.

Tech Stack

Backend: Python (Flask)

Frontend: HTML, CSS, JavaScript (all in one index.html file)

API: ElevenLabs Text-to-Speech

Setup and Installation

Follow these steps to get the project running on your local machine.

1. Clone the Repository

git clone [https://github.com/Keito1245/Storyteller.git](https://github.com/Keito1245/Storyteller.git)
cd Storyteller



2. Create a Python Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
.\venv\Scripts\activate



3. Install Dependencies

This project requires a few Python libraries, listed in requirements.txt.

pip install -r requirements.txt



4. Set Up Environment Variables (CRITICAL)

This project uses your secret ElevenLabs API key. You must never share this key or commit it to Git.

Find the file .env.example.

Make a copy of it and rename the copy to .env.

Open the .env file with a text editor.

Add your ElevenLabs API key:

ELEVENLABS_API_KEY="your_secret_api_key_goes_here"



The .gitignore file is already set up to ignore .env, so you are safe to commit your code.

How to Run

Add Your Content:

Place your book cover images (e.g., remy_rabbit.jpeg) inside the static/images/ folder.

Open app.py and edit the all_stories list to match your books, cover filenames, and story pages.

Run the Flask Server:

python app.py



View the App:
Open your web browser and go to: http://127.0.0.1:5000

Project Structure

/your_storybook_project
├── app.py              # The main Flask server
├── requirements.txt    # Python dependencies
├── .env                # Your secret API key (Ignored by Git)
├── .env.example        # Template for environment variables
├── .gitignore          # Tells Git to ignore .env and cache
├── /templates
│   └── index.html      # The frontend (HTML, CSS, JS)
└── /static
    └── /images         # Your book cover JPEGs

