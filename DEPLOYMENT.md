# Deployment Guide

## Frontend on Vercel

Project settings:

- Root directory: `frontend`
- Framework preset: `Vite`
- Build command: `npm run build`
- Output directory: `dist`

Environment variables:

- `VITE_API_URL=https://your-backend-domain`

The frontend already reads `VITE_API_URL`, so once that variable points to your backend, Vercel can build and serve the app correctly.

## Backend deployment

Recommended backend settings for Render, Railway, or a similar Python host:

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Python version: `3.11.9` (the repo pins this with `backend/.python-version`)

Environment variables:

- `ALLOWED_ORIGINS=https://your-frontend-domain`

You can provide multiple frontend origins as a comma-separated list:

`ALLOWED_ORIGINS=https://app-one.vercel.app,https://app-two.vercel.app`

Health checks:

- `/`
- `/health`

## Notes

- `PDF to Image` now exports as `png`, which matches the backend converter implementation.
- Backend upload and converted-file directories now use absolute paths so they behave consistently in hosted environments.
- `aspose-words` and `aspose-slides` were updated to currently available PyPI versions.
- `aspose-slides` documents a Linux runtime dependency on `libgdiplus`. If `PPTX -> PDF` fails after deploy, install `libgdiplus` on the backend host or choose a host that already provides it.
