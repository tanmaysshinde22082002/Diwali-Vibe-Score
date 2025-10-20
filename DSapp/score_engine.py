from PIL import Image, ImageDraw, ImageFont, ImageFilter

import cv2
import numpy as np
import os


def calculate_score(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    brightness = np.mean(hsv[:, :, 2]) / 255 * 100
    colorfulness = np.std(img)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    face_score = min(len(faces) * 15, 30)

    sparkle = np.sum(hsv[:, :, 2] > 200) / img.size * 100
    final_score = (0.25 * brightness + 0.25 * (colorfulness / 50) + 0.3 * face_score + 0.2 * sparkle)

    return round(min(final_score, 100), 2)

def add_watermark(image_path, score):
    img = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # Default font (safe from OS errors)
    font = ImageFont.load_default(40)

    text = f"My Diwali Score is : {score:.2f}/100 "

    # Measure text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Padding and position
    padding_x = 20
    padding_y = 30
    box_width = text_width + padding_x * 2
    box_height = text_height + padding_y * 2
    x = img.width - box_width - 40
    y = img.height - box_height - 40

    # Create rounded rectangle background
    box_color = (255, 165, 0, 210)  # orange with transparency
    draw.rounded_rectangle(
        [x, y, x + box_width, y + box_height],
        radius=20,
        fill=box_color
    )

    # Add subtle border/glow
    shadow = ImageDraw.Draw(txt_layer)
    for offset in range(3):
        shadow.rounded_rectangle(
            [x - offset, y - offset, x + box_width + offset, y + box_height + offset],
            radius=20,
            outline=(255, 140, 0, 100)
        )

    # Add text (white)
    text_x = x + padding_x
    text_y = y + padding_y
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

    # Combine layers
    watermarked = Image.alpha_composite(img, txt_layer).convert("RGB")

    # Save file
    watermarked_path = image_path.replace(".jpg", "_watermarked.jpg").replace(".png", "_watermarked.png")
    watermarked.save(watermarked_path)

    return watermarked_path