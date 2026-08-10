# Ced1e GitHub terminal profile

This version intentionally uses a generated **PNG** for the final display.
GitHub renders PNGs reliably, unlike the previous SVG text/shape approaches.

The portrait is generated from `profile-photo.png` using character-density
mapping, then combined with the terminal information panel.

## Generate locally

```bash
pip install -r requirements.txt
python generate_profile.py
```

Then commit `profile.png` and `README.md`.

## GitHub

The README embeds:

```html
<img src="./profile.png" width="100%">
```

Do not embed the SVG versions from the earlier attempts.
