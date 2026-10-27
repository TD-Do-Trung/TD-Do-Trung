# Neil Do — Animated GitHub Profile Starter

This starter uses original Python code to turn your photo into an animated ASCII SVG. All animation runs inside the generated SVG using SMIL, so the GitHub README needs no JavaScript.

## 1. Make your GitHub profile repository
Create a PUBLIC repository whose name exactly equals your GitHub username, e.g. `YOUR_USERNAME/YOUR_USERNAME`.

## 2. Copy the starter files into that repository
Copy `scripts/`, `requirements.txt`, `README.md`, and the empty `assets/` directory.

## 3. Prepare a photo
Use a centered square portrait, ideally with a light/transparent background. Save it as `portrait.png` in the repository root. Avoid committing the photo if you prefer; only the SVG is necessary for the final README.

## 4. Generate
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_ascii.py portrait.png --name "Neil Do" --handle "neildo" --duration 5.5
```

The output is `assets/neildo-ascii.svg`.

## 5. Publish
```bash
git add README.md assets/neildo-ascii.svg scripts/generate_ascii.py requirements.txt
git commit -m "Add animated ASCII portrait to profile"
git push
```

The README appears on `https://github.com/YOUR_USERNAME`.

## Customize
- `--name "Your Name"`: displayed name
- `--handle yourhandle`: terminal handle (need not equal GitHub username)
- `--duration 8`: slower loading animation (seconds)
- `--columns 125`: finer image detail
- `--out assets/other.svg`: output filename, then update README `<img src>`

## Troubleshooting
- ASCII is noisy: remove background or use high-contrast image, preferably on white background.
- SVG looks static on refresh: GitHub image proxy/browser cache may keep the old animation state; try a fresh tab/incognito or update the file URL for testing.
- This is a README image, NOT the circular account avatar GitHub draws on the left.
