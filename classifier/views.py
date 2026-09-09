import base64
import csv
import io

import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import CSVUploadForm

# Imported once at module load time, matching the pattern ml/model.py itself
# documents — this is where the trained TensorFlow model will eventually
# get loaded into memory exactly once, not on every request.
from ml.model import classify_image


@login_required
def writeup(request):
    """
    Page 1: the process write-up.

    This is a placeholder. Workstream D owns the real content: how the
    network was built, what worked/didn't, well-classified vs.
    misclassified examples, and the analysis of common confusions.
    """
    return render(request, 'classifier/writeup.html')


@login_required
def classify(request):
    """
    Page 2: upload a CSV, see it rendered as an image, and get a
    (currently stubbed) classification back.
    """
    context = {'form': CSVUploadForm()}

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        context['form'] = form

        if not form.is_valid():
            messages.error(request, 'Please choose a file to upload.')
            return render(request, 'classifier/classify.html', context)

        uploaded_file = request.FILES['csv_file']

        # Reject anything that isn't at least named like a CSV up front.
        if not uploaded_file.name.lower().endswith('.csv'):
            messages.error(request, 'That file is not a CSV. Please upload a .csv file.')
            return render(request, 'classifier/classify.html', context)

        try:
            pixel_array = _parse_pixel_csv(uploaded_file)
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(request, 'classifier/classify.html', context)

        # Auto-detect 0-255 vs 0-1 scaling, then normalize to 0-1 for display
        # and for whatever the eventual model expects.
        if pixel_array.max() > 1.0:
            scaled = pixel_array / 255.0
        else:
            scaled = pixel_array

        image_data_uri = _array_to_png_data_uri(scaled)
        digit, confidence = classify_image(scaled)

        context.update({
            'image_data_uri': image_data_uri,
            'predicted_digit': digit,
            'confidence_pct': round(confidence * 100, 1),
        })

    return render(request, 'classifier/classify.html', context)


def _parse_pixel_csv(uploaded_file):
    """
    Parses an uploaded CSV into a 28x28 float numpy array.

    Raises ValueError with a user-facing message on any problem, so the
    view can turn it into a friendly on-page alert instead of a Django
    error page — per the B5 input-validation requirement.
    """
    try:
        decoded = uploaded_file.read().decode('utf-8-sig')
    except UnicodeDecodeError:
        raise ValueError('That file could not be read as text — is it really a CSV?')

    reader = csv.reader(io.StringIO(decoded))
    rows = [row for row in reader if row]  # skip fully blank lines

    if len(rows) != 28:
        raise ValueError(
            f'Expected exactly 28 rows, found {len(rows)}. '
            'Check that the file has no header row and isn\'t missing/extra lines.'
        )

    parsed_rows = []
    for i, row in enumerate(rows):
        if len(row) != 28:
            raise ValueError(
                f'Row {i + 1} has {len(row)} columns, expected 28.'
            )
        try:
            parsed_rows.append([float(v) for v in row])
        except ValueError:
            raise ValueError(
                f'Row {i + 1} contains a non-numeric value. '
                'Every cell must be a pixel intensity number.'
            )

    array = np.array(parsed_rows, dtype=float)

    if array.min() < 0 or array.max() > 255:
        raise ValueError(
            'Pixel values must be within 0-255 (or 0-1 if pre-scaled). '
            f'Found a value of {array.min() if array.min() < 0 else array.max()}.'
        )

    return array


def _array_to_png_data_uri(scaled_array):
    """
    Renders a 0-1 scaled 28x28 array as a base64 PNG data URI, so it can be
    dropped straight into an <img src="..."> tag with no separate file to
    manage on disk.
    """
    from PIL import Image

    pixels = (scaled_array * 255).astype('uint8')
    image = Image.fromarray(pixels, mode='L').resize((140, 140), Image.NEAREST)

    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('ascii')
    return f'data:image/png;base64,{encoded}'
