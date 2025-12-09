# Virtual Story Generator

A creative application that generates unique stories based on user prompts using the Gemini AI model.

## Features

- Modern, responsive web interface with TailwindCSS styling
- Real-time story creation using Gemini AI
- Professional gradient design with glassmorphism effects
- Adjustable creativity level and story length controls
- Character counter for prompts
- Copy and save functionality for generated stories
- Random story prompt generator for inspiration
- Multi-language support: English, Swahili, Chichewa, Zulu, Yao, French, Portuguese, Tumbuka, and Kinyarwanda
- Mobile-friendly responsive design
- Clean and intuitive user experience

## Prerequisites

- Python 3.7 or higher
- A Gemini API key from Google AI Studio

## Installation

1. Clone or download this repository to your local machine
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key:
   - Create a `.env` file in the project root directory
   - Add your API key to the file: `GEMINI_API_KEY=your_actual_api_key_here`
   - Alternatively, set the environment variable directly

## Usage

1. Run the application:

```bash
python run_app.py
```

2. Open your web browser and go to `http://localhost:5000`
3. Enter your story prompt in the text area, or click "Random Prompt" for inspiration
4. Adjust creativity level, story length, and language as desired
5. Click "Generate Story" to create your unique story
6. Use "Copy Story" to copy the text or "Save Story" to download as a text file

## Environment Variables

The application requires the following environment variable:

- `GEMINI_API_KEY` - Your Gemini API key for authentication

## API Integration

The application uses the Gemini API. The integration is set up to use the `gemini-pro` model which is well-suited for creative text generation like stories.

## Command Line Version

For a command-line version of the story generator, run:

```bash
python story_generator.py
```

This provides a text-based interface for story generation.

## Customization

You can customize the story generation by modifying the parameters in `app.py`:
- `max_tokens` - Controls the length of the generated story
- `temperature` - Adjusts the creativity level (0.0 to 1.0)
- `model` - Change to a different Qwen model if desired

You can also customize the UI by modifying:
- `templates/index.html` - The main interface
- `static/style.css` - Custom styles (requires Tailwind build process)

## Troubleshooting

If you encounter issues:
1. Ensure your API key is correctly set
2. Check that you have an internet connection
3. Verify that the required dependencies are installed

## License

This project is created for educational purposes. Please respect the terms of the Qwen API when using this application.