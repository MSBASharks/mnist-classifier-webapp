# Handoff: Workstreams B, D, E

Workstream C (infrastructure) is done and the app is **live right now** at:

**https://balcony-lapped-silicon.ngrok-free.dev**
Login: `dan` / `Optimization1234`

⚠️ **This URL changes every time the ngrok tunnel restarts** (free plan doesn't
support a fixed domain). Don't treat it as permanent — see the E3 note below
for what this means at submission time.

Because the Django app had to exist early to test the Docker/deploy pipeline,
**most of Workstream B is already built** — not stubbed, actually built and
tested. This doc is about what's real, what's still a placeholder, and
exactly which files each of you owns from here.

---

## For Workstream B owners (P2 — Core & Auth, P4 — Classifier Flow)

You're inheriting a working app, not starting from scratch. Here's the
honest status of each task:

| Task | Status | File(s) |
|---|---|---|
| B1. Project scaffolding | ✅ Done | Whole repo structure |
| B2. Authentication | ✅ Done | `mysite/urls.py`, `mysite/settings.py`, `classifier/management/commands/create_instructor.py` |
| B3. Write-up page | 🟡 Placeholder only | `classifier/templates/classifier/writeup.html` — this is D2's job, see below |
| B4. Upload & classify page | ✅ Done | `classifier/views.py` (`classify` view), `classifier/forms.py`, `classifier/templates/classifier/classify.html` |
| B5. Input validation | ✅ Done | `_parse_pixel_csv()` in `classifier/views.py` — handles wrong dims, non-numeric, out-of-range, non-CSV |
| B6. Local integration test | ✅ Done | Verified via Django test client (login, valid upload, bad CSVs, logged-out redirect) and live on the deployed URL above |

**What you should actually do:**
1. Read `README.md` in the repo root first — it explains what's real vs.
   placeholder and how to run locally without Docker.
2. Pull the repo and get it running locally (`pip install -r
   requirements.txt`, `python manage.py migrate`, `python manage.py
   create_instructor`, `python manage.py runserver`) so you're not editing
   blind.
3. `ml/model.py` is the real trained model, already wired in and working —
   don't touch it unless the model itself changes.
4. If B5's validation needs to be stricter or looser (e.g. different error
   wording, different edge cases), that's in `_parse_pixel_csv()` and
   `classify()` in `classifier/views.py`.
5. Test cases worth trying by hand (from the project plan's own B5 list):
   wrong file type, 27×28, 28×27, header row present, non-numeric cells,
   values out of range, empty file. All of these are currently handled —
   confirm they still work if you touch the validation logic.

---

## For Workstream D owners (D1 — Design, D2 — Write-up article)

### D1: Design pass (50% of the grade — this is the big one)

The current styling is intentionally minimal placeholder CSS, explicitly
**not** meant to be final. Everything you need to restyle lives in:

- `classifier/static/classifier/style.css` — all current styling, replace freely
- `classifier/templates/classifier/base.html` — shared layout/nav, wraps every page
- `classifier/templates/classifier/login.html`
- `classifier/templates/classifier/writeup.html`
- `classifier/templates/classifier/classify.html`

**Safe to change:** all CSS, all HTML structure/classes/layout, colors,
fonts, images, adding your own static assets under `classifier/static/classifier/`.

**Don't remove these** (they're load-bearing, not just placeholder):
- `{% csrf_token %}` in both `<form>` tags — Django will reject the POST without it
- The `name="csv_file"` on the file input (comes from `{{ form.as_p }}` in
  `classify.html` — if you rebuild that form manually instead of using
  `form.as_p`, keep the field name `csv_file` exactly)
- The `{% if messages %}` loop in `base.html` — this is how validation errors
  (B5) actually reach the user; if you restyle it, keep the loop, just
  change how each message *looks*
- `{% url '...' %}` tags — these generate the actual links; don't hardcode
  URLs as plain strings

After restyling, re-run through the B5 test cases above to confirm error
messages still display — a redesign that accidentally drops the messages
loop would silently break input validation from the user's perspective.

### D2: Process write-up article

This is the actual content that replaces the placeholder in
`classifier/templates/classifier/writeup.html`. Source material for it:

- The architecture search story: `Project_1_Plan.pdf`'s NModel1→NModelFinal
  table (what was tried, what worked, what didn't) — Workstream A's log
- Final architecture: `Group_1_Project_1.ipynb`, the `NModelFinal` cell
- Test-set results: same notebook, the misclassification analysis cells
  (confusion matrix, most-confident-wrong, most-confident-right)
- Well-classified vs. misclassified images: **the notebook generates these
  as matplotlib plots but doesn't save them as files.** You'll need to
  export them as PNGs (e.g. `plt.savefig(...)` right before `plt.show()`
  in those cells) and add them to
  `classifier/static/classifier/images/`, then reference them in
  `writeup.html` with `{% static 'classifier/images/yourfile.png' %}`
  (note: `{% load static %}` is already at the top of `base.html`, so
  `writeup.html` inherits that).
- The "is 100% accuracy ever possible" question the assignment asks for is
  still an open checkbox in the project plan — this write-up is where that
  answer belongs.

---

## For Workstream E owners (Integration & Submission)

**E1. Requirements audit** — walk the assignment's bullet list against the
live URL above, not against local dev. A few things worth checking
specifically since they're easy to miss: the "start over" button (works —
it's just a link back to the same page), the file-type/dimension rejection
messages (all implemented, listed under B5 above), and the login gate on
*every* page (confirmed: `/classify/` redirects anonymous users to
`/login/?next=/classify/`).

**E2. Fresh-eyes test** — have someone who didn't build the upload page
throw bad files at it live on the ngrok URL: wrong dimensions, a `.txt`
renamed to `.csv`, a file with a header row, empty file.

**E3. Submission package — two things need attention before you finalize:**

1. **The ngrok URL is not stable.** It's whatever the tunnel gets assigned
   *right now*, and changes if the AWS instance reboots or the tunnel
   restarts. Don't lock in the URL for submission until you're at the point
   where nothing else will touch the instance — get the live URL as close
   to submission time as practical, and confirm it still loads right before
   you submit.
2. **The GitHub repo is currently Private**, which satisfies "include a way
   to get access to your repo" only if you actually grant that access
   explicitly — a private repo link alone won't let the instructor in. Add
   the instructor as a collaborator (Settings → Collaborators on
   github.com/MSBASharks/mnist-classifier-webapp), or confirm with the
   assignment instructions whether they want it public instead.

Also for the screengrab requirement (C7): a Lightsail console screenshot
showing the running instance satisfies this — that's already been captured
as part of Workstream C, just make sure it ends up in the final submission
package.
