import openai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import requests
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("API_KEY")

def generate_story(pdf_name):

    name = input("What is your child's name? ")
    age = input("How old are they? ")
    activity = input("What is their favorite activity? ")
    set_at_home = input("Do you want the story to be set in your home town/city? Type Yes or No. ")
    if set_at_home == "Yes":
        location = input("What is your home town/city? ")
    else:
        location = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Write the name of a random African city."}])

    print("Hang on a second while we generate your story...")
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Write a 100 word bedtime story about {activity}. The main character's name should be {name}. The story should be set in {location}. Tailor it for a child aged {age}. Don't describe the location as a 'magical land' because it's a real place in Africa. Write in the style of Chimamanda Ngozi Adichie."}])
    story_text = response.choices[0].message.content

    cover_photo = openai.Image.create(
        prompt=f"Oil painting of a dark-skinned kid playing {activity}",
        n=1,
        size='512x512'
    )

    # Get the image URL from the OpenAI response
    image_url = cover_photo['data'][0]['url']
    image_response = requests.get(image_url)
    image_filename = "cover_photo.png"

    # Save the image locally
    with open(image_filename, "wb") as file:
        file.write(image_response.content)

    # Generate the PDF
    pdf_filename = pdf_name
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Add the cover photo to the PDF
    cover_photo_width = 200
    cover_photo_height = 200
    cover_photo_x = (letter[0] - cover_photo_width) / 2  # Calculate x-coordinate to center the photo
    c.drawImage(image_filename, cover_photo_x, 500, width=cover_photo_width, height=cover_photo_height)

    # Add the story text to the PDF
    text_x = 50
    text_y = 430
    line_spacing = 20  # Adjust the line spacing as needed
    max_text_width = 500  # Maximum width of the text before wrapping
    story_words = story_text.split()
    line = ''
    for word in story_words:
        if c.stringWidth(line + ' ' + word) < max_text_width:
            line += ' ' + word
        else:
            # Check if there is enough space on the page for another line
            remaining_space = text_y - line_spacing
            if remaining_space < line_spacing:
                # Create a new page
                c.showPage()
                text_y = 750  # Reset the text_y position for the new page
            else:
                text_y -= line_spacing

            c.drawString(text_x, text_y, line.strip())
            line = word

    # Add the last line of the story
    remaining_space = text_y - line_spacing
    if remaining_space < (line_spacing*3):
        # Create a new page
        c.showPage()
        text_y = 750  # Reset the text_y position for the new page
    else:
        text_y -= line_spacing

    c.drawString(text_x, text_y, line.strip())

    c.save()

    print(f"The story has been generated! You can download it as a PDF: {pdf_filename}")

generate_story("ntumba.pdf")
