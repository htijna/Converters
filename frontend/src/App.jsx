import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, 
  FileImage, 
  Files, 
  UploadCloud, 
  Download, 
  X, 
  CheckCircle2, 
  AlertCircle,
  Loader2,
  Moon,
  Sun,
  LayoutTemplate,
  History,
  Trash2
} from 'lucide-react';
import './index.css';
import logoDark from './assets/logodark.png';
import logoLight from './assets/logolight.png';

const API_URL = "";

const CONVERSION_OPTIONS = [
  { id: 'pdf_docx', from: 'pdf', to: 'docx', label: 'PDF to Word', icon: <FileText size={20} /> },
  { id: 'docx_pdf', from: 'docx', to: 'pdf', label: 'Word to PDF', icon: <FileText size={20} /> },
  { id: 'pptx_pdf', from: 'pptx', to: 'pdf', label: 'PPT to PDF', icon: <Files size={20} /> },
  { id: 'img_pdf', from: 'image', to: 'pdf', label: 'Image to PDF', icon: <FileImage size={20} /> },
  { id: 'pdf_img', from: 'pdf', to: 'png', label: 'PDF to Image', icon: <FileImage size={20} /> },
];

function App() {
  const [file, setFile] = useState(null);
  const [targetFormat, setTargetFormat] = useState('');
  const [status, setStatus] = useState('idle'); // idle, uploading, converting, success, error
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [downloadUrl, setDownloadUrl] = useState('');
  const [downloadName, setDownloadName] = useState('');
  const [history, setHistory] = useState(() => {
    const saved = localStorage.getItem('conv_history');
    return saved ? JSON.parse(saved) : [];
  });
  const [darkMode, setDarkMode] = useState(true);
  
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark');
      document.body.classList.remove('light');
    } else {
      document.body.classList.add('light');
      document.body.classList.remove('dark');
    }
  }, [darkMode]);

  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.size > 25 * 1024 * 1024) {
      setError("File size exceeds 25MB limit.");
      return;
    }
    setFile(selectedFile);
    setError('');
    
    // Auto-detect conversion options
    const ext = selectedFile?.name.split('.').pop().toLowerCase();
    const options = CONVERSION_OPTIONS.filter(o => o.from === ext || (ext && ['jpg', 'png', 'jpeg'].includes(ext) && o.from === 'image'));
    if (options.length > 0) setTargetFormat(options[0].id);
  };

  const handleConvert = async () => {
    if (!file || !targetFormat) return;

    setStatus('uploading');
    setProgress(10);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    const selectedOption = CONVERSION_OPTIONS.find(o => o.id === targetFormat);
    formData.append('target_format', selectedOption.to);

    let progressInterval;
    
    try {
      // Start a slow auto-increment for the 'converting' phase
      
      const response = await axios.post(`${API_URL}/convert`, formData, {
        onUploadProgress: (progressEvent) => {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          const uploadProgress = percent / 2; // 0-50%
          setProgress(uploadProgress);
          
          if (percent === 100) {
            setStatus('converting');
            // Fake progress from 50 to 95 while waiting for the server
            let current = 50;
            progressInterval = setInterval(() => {
              if (current < 94) {
                current += Math.random() * 0.5; // Slower, more constant updates
                setProgress(current);
              }
            }, 300); // 300ms for more fluid, constant moving
          }
        }
      });

      if (progressInterval) clearInterval(progressInterval);
      setProgress(100);
      
      setTimeout(() => {
        const finalUrl = `${response.data.download_url}?dname=${encodeURIComponent(response.data.filename)}`;
        setDownloadUrl(finalUrl);
        setDownloadName(response.data.filename);
        setStatus('success');

        // Update History
        const newEntry = {
          id: Date.now(),
          originalName: file.name,
          targetName: response.data.filename,
          url: finalUrl,
          date: new Date().toLocaleString()
        };
        const updatedHistory = [newEntry, ...history].slice(0, 5);
        setHistory(updatedHistory);
        localStorage.setItem('conv_history', JSON.stringify(updatedHistory));
      }, 500);

    } catch (err) {
      if (progressInterval) clearInterval(progressInterval);
      console.error("Conversion Error:", err);
      const msg = err.response?.data?.detail || "The conversion engine encountered an issue. Check the file format or try again.";
      setError(msg);
      setStatus('error');
    }
  };

  const handleDownload = async (url, filename) => {
    try {
      const response = await axios.get(`${API_URL}${url}`, { responseType: 'blob' });
      const blobUrl = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = blobUrl;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    } catch (err) {
      console.error("Download failed:", err);
      setError("Download failed. Please try again.");
    }
  };

  const reset = () => {
    setFile(null);
    setTargetFormat('');
    setStatus('idle');
    setProgress(0);
    setDownloadUrl('');
    setDownloadName('');
    setError('');
  };

  const clearHistory = () => {
    setHistory([]);
    localStorage.removeItem('conv_history');
  };

  const currentOption = CONVERSION_OPTIONS.find(o => o.id === targetFormat);

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="logo-section">
          <div className="logo-circle-wrapper">
            <div className="logo-inner-circle">
              <img src={darkMode ? logoDark : logoLight} alt="AKJ Logo" className="logo-icon" />
            </div>
          </div>
          <a href="#" className="logo-text">AKJ Converter</a>
        </div>
        <button className="theme-toggle" onClick={() => setDarkMode(!darkMode)} title="Toggle Theme">
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </nav>

      <section className="hero">
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Transform Your Files <br /> With Precision
        </motion.h1>
        <p>Swift, secure, and smart file conversions for the modern user.</p>
      </section>

      <main className="converter-box">
        <AnimatePresence mode="wait">
          {status === 'idle' && (
            <motion.div 
              key="idle"
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }} 
              exit={{ opacity: 0 }}
            >
              <div 
                className="dropzone"
                onDragOver={(e) => { e.preventDefault(); e.currentTarget.classList.add('active'); }}
                onDragLeave={(e) => e.currentTarget.classList.remove('active')}
                onDrop={(e) => {
                  e.preventDefault();
                  e.currentTarget.classList.remove('active');
                  const droppedFile = e.dataTransfer.files[0];
                  handleFileSelect({ target: { files: [droppedFile] } });
                }}
                onClick={() => fileInputRef.current.click()}
              >
                <UploadCloud size={60} color="var(--accent-blue)" strokeWidth={1.5} />
                <h3>{file ? file.name : "Choose a file or drag it here"}</h3>
                <p>Support for PDF, DOCX, PPTX, JPG, PNG (Max 25MB)</p>
                <input 
                  type="file" 
                  hidden 
                  ref={fileInputRef} 
                  onChange={handleFileSelect}
                  accept=".pdf,.docx,.pptx,.jpg,.png,.jpeg"
                />
              </div>

              {file && (
                <div className="options-section">
                  <h4>Select Conversion Type</h4>
                  <div className="options-grid">
                    {CONVERSION_OPTIONS.filter(o => 
                      o.from === file.name.split('.').pop().toLowerCase() ||
                      (['jpg', 'png', 'jpeg'].includes(file.name.split('.').pop().toLowerCase()) && o.from === 'image')
                    ).map(opt => (
                      <div 
                        key={opt.id}
                        className={`option-card ${targetFormat === opt.id ? 'selected' : ''}`}
                        onClick={() => setTargetFormat(opt.id)}
                      >
                        {opt.icon}
                        <span>{opt.label}</span>
                      </div>
                    ))}
                  </div>
                  <button className="download-btn" style={{marginTop: '2rem'}} onClick={handleConvert}>
                    Convert Now
                  </button>
                </div>
              )}
            </motion.div>
          )}

          {(status === 'uploading' || status === 'converting') && (
            <motion.div 
              key="processing"
              className="processing-state"
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }}
            >
              <Loader2 className="spinner" size={48} />
              <h3>{status === 'uploading' ? 'Uploading File...' : 'Converting...'}</h3>
              <div className="progress-bar">
                <div className="progress-inner" style={{ width: `${Math.round(progress)}%` }}></div>
              </div>
              <p>{Math.round(progress)}% completed</p>
            </motion.div>
          )}

          {status === 'success' && (
            <motion.div 
              key="success"
              className="result-state"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
            >
              <CheckCircle2 size={64} color="#10b981" />
              <h3>Conversion Successful!</h3>
              <p>Your file is ready for download.</p>
              <div className="result-actions">
                <button 
                  onClick={() => handleDownload(downloadUrl, downloadName)} 
                  className="download-btn"
                >
                  Download {downloadName}
                </button>
                <button className="secondary-btn" onClick={reset}>Convert Another</button>
              </div>
            </motion.div>
          )}

          {status === 'error' && (
            <motion.div 
              key="error"
              className="result-state"
              initial={{ opacity: 0 }} 
              animate={{ opacity: 1 }}
            >
              <AlertCircle size={64} color="var(--accent-red)" />
              <h3 className="error-msg">{error}</h3>
              <button className="download-btn" onClick={reset}>Try Again</button>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {history.length > 0 && status === 'idle' && (
        <motion.section 
          className="history-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="history-header">
            <h3><History size={20} /> Recent Conversions</h3>
            <button onClick={clearHistory} className="clear-btn"><Trash2 size={16} /> Clear</button>
          </div>
          <div className="history-list">
            {history.map(item => (
              <div key={item.id} className="history-item">
                <div className="item-info">
                  <span className="item-name">{item.targetName}</span>
                  <span className="item-date">{item.date}</span>
                </div>
                <button 
                  onClick={() => handleDownload(item.url, item.targetName)} 
                  className="item-download"
                  style={{border:'none', cursor:'pointer'}}
                >
                  <Download size={18} />
                </button>
              </div>
            ))}
          </div>
        </motion.section>
      )}

      <footer className="footer">
        <p>&copy; 2026 AKJ. Secure & Private conversion.</p>
      </footer>

    </div>
  );
}

export default App;
