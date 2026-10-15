
import { useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const fileInput = useRef(null);
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function chooseFile(event) {
    const selected = event.target.files?.[0];
    if (!selected) return;

    if (!["image/png", "image/jpeg"].includes(selected.type)) {
      setError("Please select a PNG or JPEG image.");
      return;
    }

    if (selected.size > 10 * 1024 * 1024) {
      setError("Please select an image smaller than 10 MB.");
      return;
    }

    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setResult(null);
    setError("");
  }

  async function analyzeImage() {
    if (!file) {
      setError("Choose a retinal image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Prediction failed.");
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message.includes("Failed to fetch")
          ? "Cannot reach the API. Make sure the FastAPI server is running."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="navbar">
        <a className="brand" href="#home">
          <span className="brand-icon">R</span>
          <span>retinal<span className="brand-accent">.ai</span></span>
        </a>

        <nav>
          <a href="#home">Home</a>
          <a href="#screening">AI Screening</a>
          <a href="#about">About</a>
        </nav>

        <a className="nav-cta" href="#screening">Try the demo <span>↗</span></a>
      </header>

      <main>
        <section className="hero" id="home">
          <div className="hero-copy">
            <div className="eyebrow"><span className="status-dot" /> AI-POWERED RETINAL RESEARCH</div>
            <h1>A clearer view of <span>retinal health.</span></h1>
            <p>
              Explore an experimental deep-learning model that classifies
              retinal images into five diabetic retinopathy severity grades.
            </p>
            <div className="hero-actions">
              <a className="primary-button" href="#screening">Explore screening <span>→</span></a>
              <a className="secondary-button" href="#about">How it works</a>
            </div>
            <div className="hero-note">
              <span className="note-icon">✳</span>
              Research demonstration · ResNet18 · Five-class classification
            </div>
          </div>

          <div className="hero-visual">
            <div className="visual-orbit orbit-one" />
            <div className="visual-orbit orbit-two" />
            <div className="visual-card">
              <div className="visual-card-top"><span>RETINAL IMAGING</span><span className="live-label">DEMO</span></div>
              <div className="retina-art">
                <div className="retina-core">
                  <div className="retina-disc" />
                  <svg viewBox="0 0 320 320" aria-hidden="true">
                    <g fill="none" strokeLinecap="round">
                      <path d="M160 160 C130 130 105 100 76 62 M155 153 C122 143 88 129 45 123 M151 158 C117 172 92 199 57 232 M163 165 C191 188 211 219 238 264 M167 157 C202 133 236 106 270 77 M163 153 C190 117 194 85 201 42 M157 163 C143 205 139 241 126 286" stroke="#b94736" strokeWidth="5"/>
                      <path d="M125 123 L105 95 L88 85 M105 141 L75 150 L57 170 M104 195 L89 220 L71 222 M193 189 L221 189 L244 211 M204 135 L228 130 L251 111 M191 115 L180 87 L180 67 M141 223 L158 246 L169 267 M221 232 L247 244 L258 259 M78 62 L62 49 M238 264 L260 278 M270 77 L286 64" stroke="#e87964" strokeWidth="3"/>
                      <path d="M160 160 L147 129 L139 103 M160 160 L183 174 L204 207 M160 160 L190 145 L218 143 M160 160 L137 180 L116 205" stroke="#f4a38c" strokeWidth="2"/>
                    </g>
                  </svg>
                </div>
              </div>
              <div className="visual-card-bottom"><span>Retinal image analysis</span><span className="scan-indicator">● Experimental</span></div>
            </div>
            <div className="floating-tag tag-top"><span>✦</span> Deep learning</div>
            <div className="floating-tag tag-bottom"><span>◎</span> Image classification</div>
          </div>
        </section>

        <section className="stats-strip" aria-label="Project overview">
          <div><strong>01</strong><span>Image input</span></div>
          <div><strong>02</strong><span>AI inference</span></div>
          <div><strong>03</strong><span>Result preview</span></div>
          <div><strong>05</strong><span>Output grades</span></div>
        </section>

        <section className="screening-section" id="screening">
          <div className="section-heading">
            <div className="eyebrow">THE INTERACTIVE DEMO</div>
            <h2>Explore retinal image analysis</h2>
            <p>Upload a retinal photograph to see how the experimental classifier responds.</p>
          </div>

          <div className="screening-grid">
            <div className="upload-panel">
              <div className="panel-heading"><div><span className="step-number">01</span><h3>Upload an image</h3></div><span className="file-type">PNG / JPG</span></div>
              <button className={`drop-zone ${preview ? "has-image" : ""}`} onClick={() => fileInput.current?.click()}>
                {preview ? (
                  <img className="image-preview" src={preview} alt="Selected retinal image preview" />
                ) : (
                  <>
                    <span className="upload-icon">↑</span>
                    <strong>Choose a retinal image</strong>
                    <span>Click to browse files on your device</span>
                    <small>PNG or JPEG · Maximum 10 MB</small>
                  </>
                )}
              </button>
              <input ref={fileInput} type="file" accept="image/png,image/jpeg" hidden onChange={chooseFile} />
              {file && <div className="selected-file"><span>▧</span><span>{file.name}</span><span>{(file.size / 1024 / 1024).toFixed(2)} MB</span></div>}
              <button className="primary-button analyze-button" disabled={!file || loading} onClick={analyzeImage}>
                {loading ? "Analyzing image…" : "Analyze retinal image"} <span>→</span>
              </button>
              {error && <p className="error-message" role="alert">{error}</p>}
              <p className="privacy-note">Demo only. Use non-identifiable sample images.</p>
            </div>

            <div className="result-panel">
              <div className="panel-heading"><div><span className="step-number">02</span><h3>Analysis result</h3></div><span className="result-status">{loading ? "PROCESSING" : result ? "COMPLETE" : "AWAITING IMAGE"}</span></div>
              {!result && !loading && (
                <div className="empty-result">
                  <div className="result-symbol">✳</div>
                  <h3>Your result will appear here</h3>
                  <p>Upload an image and run the demo to see the model's predicted class.</p>
                  <div className="grade-preview">{["No DR", "Mild", "Moderate", "Severe", "Proliferative"].map((grade, i) => <span key={grade}><i>{i}</i>{grade}</span>)}</div>
                </div>
              )}
              {loading && <div className="empty-result"><div className="loader" /><h3>Processing image</h3><p>The model is generating its prediction.</p></div>}
              {result && (
                <div className="result-content">
                  <span className="result-kicker">PREDICTED CLASS</span>
                  <h2>{result.predicted_class}</h2>
                  <p className="result-description">The model assigned this image to severity grade {result.predicted_grade}.</p>
                  <div className="result-grade"><span>Predicted grade</span><strong>{result.predicted_grade} <small>/ 4</small></strong></div>
                  <div className="probability-row"><span>Model probability <small>(not clinically calibrated)</small></span><strong>{(result.predicted_probability * 100).toFixed(1)}%</strong></div>
                  <div className="probability-track"><div style={{width: `${Math.min(100, Math.max(0, result.predicted_probability * 100))}%`}} /></div>
                  <div className="clinical-warning">⚠ {result.warning}</div>
                </div>
              )}
            </div>
          </div>
          <p className="medical-disclaimer"><strong>Medical safety notice</strong> — This is an experimental educational demonstration, not a medical device. It has not been clinically validated and must not be used to diagnose, rule out, or guide treatment for diabetic retinopathy. Consult a qualified eye-care professional for medical concerns.</p>
        </section>

        <section className="about-section" id="about">
          <div className="about-copy"><div className="eyebrow">BEHIND THE DEMO</div><h2>From retinal image to model output.</h2><p>The project uses a ResNet18 convolutional neural network to classify retinal photographs into five severity categories. The API preprocesses an uploaded image and returns the model's predicted class.</p></div>
          <div className="workflow">
            <div><span>01</span><strong>Upload</strong><p>Select a PNG or JPEG image.</p></div>
            <div><span>02</span><strong>Preprocess</strong><p>Resize and normalize for inference.</p></div>
            <div><span>03</span><strong>Classify</strong><p>Run the ResNet18 model.</p></div>
            <div><span>04</span><strong>Display</strong><p>Show the predicted grade.</p></div>
          </div>
        </section>
      </main>

      <footer className="footer"><a className="brand" href="#home"><span className="brand-icon">R</span><span>retinal<span className="brand-accent">.ai</span></span></a><span>Experimental AI project · For demonstration only</span><a href="#home">Back to top ↑</a></footer>
    </div>
  );
}
