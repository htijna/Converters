# Ultimate Online Converter - Implementation Plan

## 1. Project Structure
```text
converters/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── services/
│   │   ├── converter.py # Core conversion logic
│   │   └── utils.py     # File handling, cleanup
│   └── uploads/         # Temporary storage
└── frontend/
    ├── src/
    │   ├── components/  # DropZone, Navbar, Cards
    │   ├── App.jsx      # Main layout & state
    │   ├── App.css      # Custom styling (Glassmorphism)
    │   └── assets/      # Icons & Images
    └── index.html
```

## 2. Technology Stack
- **Backend**: FastAPI (Python 3.13)
- **Frontend**: Vite + React + Vanilla CSS (Aesthetic focus)
- **Conversion Libraries**:
  - `pdf2docx`: PDF → Word
  - `python-docx`: DOCX metadata/creation
  - `python-pptx`: PPT manipulation
  - `PyMuPDF (fitz)`: PDF to Image, Image to PDF
  - `aspose-words`: DOCX → PDF (High fidelity, no MS Word needed)
  - `aspose-slides`: PPT → PDF (High fidelity, no MS PPT needed)
  - `Pillow`: Image processing

## 3. Key Features
- **Frontend**:
  - **Hero Section**: Clean, inviting introduction with glassmorphism.
  - **Drag-and-Drop Area**: Using `lucide-react` icons and smooth animations.
  - **Conversion History**: Simple local history storage.
  - **Theme Toggle**: Light/Dark mode.
- **Backend**:
  - **Security**: 25MB file size limit.
  - **Temporary Storage**: Files are deleted automatically after conversion/download.
  - **Error Handling**: Graceful error responses for unsupported formats.

## 4. Development Steps
1.  **Backend Setup**: Initialize FastAPI and verify library installs.
2.  **Conversion Logic**: Implement individual conversion functions in `backend/services/converter.py`.
3.  **Frontend Setup**: Build the base layout and design system (CSS variables).
4.  **UI/UX**: Implement the DropZone and conversion progress UI.
5.  **Integration**: Connect the frontend to the backend endpoints.
6.  **Polishing**: Add micro-animations and final design touches.
