import os
import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .score_engine import calculate_score, add_watermark


def home(request):
    """
    Renders the main homepage where users upload their Diwali photo.
    """
    return render(request, 'DSapp/home.html')


def upload_photo(request):
    if request.method == 'POST' and 'photo' in request.FILES:
        photo = request.FILES['photo']

        # Save original photo
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(photo.name, photo)
        saved_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)

        # Calculate score
        score = calculate_score(saved_path)

        # Generate watermarked image
        watermarked_path = add_watermark(saved_path, score)

        # ✅ Important: Create a new URL for the watermarked image
        watermarked_filename = os.path.basename(watermarked_path)
        watermarked_url = settings.MEDIA_URL + 'uploads/' + watermarked_filename

        # Send correct URL to result page
        context = {
            'score': score,
            'photo_url': watermarked_url,  # changed here
            'watermarked_url': watermarked_url,
        }


        return render(request, 'DSapp/result.html', context)


    return render(request, 'DSapp/home.html')
