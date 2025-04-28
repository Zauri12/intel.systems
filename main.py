import requests
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

import subprocess

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
BOT_TOKEN = '8188999641:AAFKZchy7sHCF0NPxYR0zBhpC99EEYzPf3Q'

# FastAPI server URL for image to LaTeX conversion
FASTAPI_URL = "http://localhost:8000/predict/"
# NotesAI API URL
NOTESAI_URL = "https://notesai-ten.vercel.app/translate/"

# Store the user's comments temporarily while processing an image 
user_comments = {}

def clean_latex_response(latex_code):
    """Remove LaTeX block delimiters and clean up the response."""
    # Remove $$ from the start and end of the LaTeX code
    latex_code = re.sub(r'^\$\$', '', latex_code)
    latex_code = re.sub(r'\$\$', '', latex_code)
    
    # You can add more cleaning steps here if needed, for example removing unnecessary spaces
    latex_code = latex_code.strip()
    return latex_code

def escape_markdown_v2(text):
    """
    Escape all special characters required for Telegram MarkdownV2.
    """
    special_chars = r"_*[]()~`>#+-=|{}.!"
    return re.sub(f"([{re.escape(special_chars)}])", r"\\\1", text)

def format_math_response(response):
    """ Convert LaTeX-style equations from the API response to Telegram-friendly MarkdownV2 format. """
    # Remove LaTeX delimiters like \( \), \[ \]
    response = re.sub(r"\\\\\\(|\\\\\\)", "", response)
    # Inline math delimiters
    response = re.sub(r"\\\\\\\[|\\\\\\\]", "", response)
    # Escape characters for MarkdownV2
    response = escape_markdown_v2(response)
    return response

async def handle_math_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any incoming message as a math query."""
    
    user_message = update.message.text  # Capture the user's message
    print(f"user_message: { user_message}")
    try:
        # Data to send to your API
        data = {
            "sys_message": "Отвечайте как эксперт по математике по русскому языку. Определите, относится ли вопрос к математике или нет. Если вопрос не относится к математике, скажите ему, что вы только эксперт по математике. Если вопрос относится к математике, ответьте на вопрос.",
            "human_message": user_message
        }

        # Make a POST request to the API
        api_response = requests.post("https://notesai-ten.vercel.app/translate/", json=data)
        api_response_data = api_response.json()
        print(api_response_data)
        # Parse and format the response
        if "AI Answer" in api_response_data:
           # formatted_response = api_response_data["AI Answer"]
            #generate_latex_pdf(api_response_data["AI Answer"], "output_with_preamble")
          
            await update.message.reply_text(api_response_data["AI Answer"])
            
            #await update.message.reply_document(document=open( "output_with_preamble.pdf", 'rb'))
            
                
        else:
            await update.message.reply_text("Result not found in API response.")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def handle_image_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    """Handle image uploads and send them to the FastAPI backend for predictions."""
    photo_file = await update.message.photo[-1].get_file()  # Get the highest resolution image
    photo_bytes = await photo_file.download_as_bytearray()  # Download the image as bytes
    user_id = update.message.from_user.id
    user_comment = user_comments.get(user_id, "")  # Retrieve any comments the user may have sent
    print(f"user_comment : {user_comment}")

    try:
        # Send image to FastAPI backend
        files = {'file': ('telegram_image.jpg', photo_bytes)}
        api_response = requests.post("http://127.0.0.1:8000/predict/", files=files)
        response_data = api_response.json()
        print(f"response_data: {str(response_data['results'] )}")
        # Handle and format the response
        if "results" in response_data: 
            data = {
                    "sys_message": "Отвечайте как эксперт по математике по русскому языку. Определите, относится ли вопрос к математике или нет. Если вопрос не относится к математике, скажите ему, что вы только эксперт по математике. Если вопрос относится к математике, ответьте на вопрос.",
                    "human_message": str(response_data['results'] )
                }
            # Add user comments if available
            if user_comment:
                    data["human_message"] += f"\n\nComment: {user_comment}"
            
            # Send LaTeX code to NotesAI
            api_ai_response = requests.post(NOTESAI_URL, json=data)
            api_ai_response_data = api_ai_response.json()
            print(api_ai_response_data)
            if 'AI Answer' in api_ai_response_data:
                    
                    #generate_latex_pdf(api_ai_response_data["AI Answer"], "output_with_preamble")
                    #await update.message.reply_document(document=open( "output_with_preamble.pdf", 'rb'))
                    await update.message.reply_text(api_ai_response_data["AI Answer"])
                    
                    
            else:
                    await update.message.reply_text("Result not found in API AI response.")
        else:
            await update.message.reply_text("Prediction not found in the response.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")



def add_latex_preamble(text):
    """Automatically adds the necessary LaTeX preamble for UTF-8 and Russian support."""
    preamble = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T2A]{fontenc}
\usepackage[russian]{babel}
\begin{document}
"""
    end_document = r"\end{document}"
    
    # Return the complete LaTeX document
    return preamble + text + end_document

def generate_latex_pdf(text, filename):
    """Generates a PDF from LaTeX code."""
    # Prepare the LaTeX code by adding the necessary preamble
    latex_code = add_latex_preamble(text)
    
    # Save the LaTeX code to a .tex file
    with open(f"{filename}.tex", "w", encoding="utf-8") as f:
        f.write(latex_code)
    
    # Run LaTeX command to generate the PDF using subprocess
    try:
        # Generate the .dvi file from .tex
        subprocess.run(["latex", f"{filename}.tex"], check=True)

        # Convert .dvi to .pdf
        subprocess.run(["dvipdf", f"{filename}.dvi"], check=True)

        print(f"PDF saved as {filename}.pdf")
    except subprocess.CalledProcessError as e:
        print(f"Error during LaTeX processing: {e}")



if __name__ == '__main__':
    print("bot is Running......")
    # Initialize the bot application
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Add handlers for messages and photos
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_math_query))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image_query))
    
    # Start polling to receive messages
    app.run_polling()