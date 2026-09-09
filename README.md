# RM 294 Group Project 1 — MNIST Classifier Webapp

This is a **placeholder scaffold** for Workstream C testing, built before
Workstream B's real Django app existed. It's a fully working Django site —
login required, an upload-and-classify page, input validation — but the
"classification" in `ml/model.py` is a stub, not the real trained model.

## What's real vs. placeholder

**Real / working:**
- Login-gated site (no self-registration route exists)
- Instructor account (`dan` / `Optimization1234`) auto-created on startup
- CSV upload, parsing, and validation (28x28, no header, numeric, in-range)
- Auto-detects 0-255 vs. 0-1 pixel scaling
- Renders the uploaded array as a visible image
- "Start Over" flow
- User-facing error messages instead of raw Django error pages
- Dockerfile + docker-compose.yml wired for ngrok on port 8000

**Placeholder — replace before final submission:**
- `ml/model.py`: returns a deterministic fake digit, not a real prediction.
  See the TODO comment in that file for exactly what to swap in.
- `classifier/templates/classifier/writeup.html`: Workstream D's content
  (architecture story, results, misclassified examples) goes here.
- Visual design: this uses minimal placeholder CSS. Workstream D's design
  pass is 50% of the grade — don't ship this styling as final.

## Running locally (without Docker)

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py create_instructor
python manage.py runserver
```

Visit http://127.0.0.1:8000, log in as `dan` / `Optimization1234`.

## Running with Docker (matches the AWS deploy flow)

```bash
docker compose build
docker compose up -d
docker compose logs   # confirm no errors, check for startup messages
```

Visit http://localhost:8000 (or the instance's public IP:8000, or through
ngrok once tunneled).

To take it down (e.g. before pulling new code):

```bash
docker compose down
```

## Swapping in the real model (Workstream A hand-off)

1. Place the trained `.keras` file at `ml/tensorflow_file.keras`.
2. Uncomment the `tensorflow-cpu` line in `requirements.txt`.
3. Replace the contents of `ml/model.py` per the TODO comment inside it —
   keep the model loaded at module level, not inside the function.
4. Update `_parse_pixel_csv`'s output shape in `classifier/views.py` if the
   model expects a different input shape than a plain 28x28 array (e.g.
   `(1, 28, 28, 1)` for a CNN).
5. Rebuild: `docker compose down && docker compose build && docker compose up -d`.

**Memory note:** the Lightsail instance in this project has 1GB RAM.
TensorFlow can be memory-hungry even for pure inference. If the container
gets OOM-killed after adding the real model, first try dropping
`--workers 2` to `--workers 1` in `entrypoint.sh`, then consider adding a
swap file on the instance if that's not enough.
