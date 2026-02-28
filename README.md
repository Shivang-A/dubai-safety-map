# Dubai Safety Map (GitHub Pages)

This project generates a static `index.html` map that can be hosted free on GitHub Pages.

## 1) Generate the website

```bash
python3 dubai_safety_map_v2.py
```

This creates/updates `index.html`.

## 2) Preview locally (optional)

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000`.

## 3) Publish on GitHub Pages

1. Create a new GitHub repo (for example: `dubai-safety-map`).
2. In this folder, run:

```bash
git init
git add dubai_safety_map_v2.py index.html README.md
git commit -m "Initial safety map site"
git branch -M main
git remote add origin https://github.com/<your-username>/dubai-safety-map.git
git push -u origin main
```

3. On GitHub: `Repo -> Settings -> Pages`.
4. Under **Build and deployment**:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
5. Save and wait 1-3 minutes.

Your site will be live at:

`https://<your-username>.github.io/dubai-safety-map/`

## 4) Update later

Whenever you change the Python data:

```bash
python3 dubai_safety_map_v2.py
git add dubai_safety_map_v2.py index.html
git commit -m "Update safety data"
git push
```

GitHub Pages will auto-redeploy.

## Important

Treat map data as advisory only and verify urgent safety info from official UAE authorities before acting.
