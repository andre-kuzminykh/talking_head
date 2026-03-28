"""
UI texts, commands, and button labels.
"""

TEXTS = {
    "welcome": (
        "Welcome to <b>Talking Head Bot</b>!\n\n"
        "I can create talking head videos from your photos.\n\n"
        "Send me a photo to get started, or select a saved one."
    ),
    "photo_saved": "Photo saved! Now send me the text you want to be spoken.",
    "photo_select_prompt": "Select a saved photo or upload a new one:",
    "no_photos": "You have no saved photos yet. Please upload a photo first.",
    "awaiting_photo": "Please send me a photo (not a file).",
    "awaiting_text": "Now send me the text you want the talking head to say.",
    "text_empty": "Text cannot be empty. Please send a non-empty message.",
    "generating": (
        "Generating your talking head video...\n"
        "This may take a few minutes. Please wait."
    ),
    "generation_error": "An error occurred during generation. Please try again.",
    "video_ready": "Here is your talking head video!",
}

BUTTONS = {
    "upload_photo": "Upload new photo",
    "select_photo": "Select saved photo",
    "generate": "Generate video",
}

COMMANDS = {
    "start": "Start the bot",
}
