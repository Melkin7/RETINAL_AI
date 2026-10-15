# 🩺 Retinal AI — Diabetic Retinopathy Detection

An AI-powered web application for classifying diabetic retinopathy severity from retinal fundus images using deep learning.

**Built with:** Python · PyTorch · FastAPI · React · Vite

> **Research/demo project:** This application is experimental and is not intended for clinical diagnosis or treatment decisions.

## 🌟 Overview

Retinal AI explores how deep learning can support the early screening of diabetic retinopathy (DR), a diabetes-related eye disease that can lead to vision loss.

The project uses a convolutional neural network trained on the APTOS 2019 Blindness Detection dataset. A React frontend lets users upload retinal images, while a FastAPI backend processes the image and returns a predicted severity class.

The project aims to explore accessible, mobile-friendly retinal screening workflows, particularly for underserved communities.

## ✨ Features

- 🖼️ Upload retinal fundus images in JPEG or PNG format.
- 🧠 Predict one of five diabetic retinopathy severity classes.
- ⚡ Run model inference through a FastAPI REST API.
- 🌐 Use a responsive React web interface.
- 📊 View the predicted class and model-reported probability.
- 🛡️ Validate image uploads and enforce a 10 MB file-size limit.
- 📖 Explore API endpoints through FastAPI's interactive documentation.

## 🩺 Classification Classes

| Grade | Class | Description |
|---|---|---|
| 0 | No DR | No diabetic retinopathy identified by the model |
| 1 | Mild DR | Mild non-proliferative diabetic retinopathy |
| 2 | Moderate DR | Moderate non-proliferative diabetic retinopathy |
| 3 | Severe DR | Severe non-proliferative diabetic retinopathy |
| 4 | Proliferative DR | Proliferative diabetic retinopathy |

Predictions are model outputs, not confirmed medical diagnoses. The displayed probability is not clinically calibrated.

## 🏗️ Architecture

```text
User
  |
  v
React + Vite Frontend
  |
  | HTTP POST /predict
  v
FastAPI Backend
  |
  v
Image Validation and Preprocessing
  |
  v
PyTorch Classification Model
  |
  v
Predicted Class and Probability
  |
  v
Result Display in Browser
```

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Frontend | React, JavaScript, CSS |
| Frontend tooling | Vite, npm |
| Backend | Python, FastAPI |
| API server | Uvicorn |
| Machine learning | PyTorch, TorchVision |
| Image processing | Pillow |
| Dataset | APTOS 2019 Blindness Detection |
| Version control | Git, GitHub |

## 📂 Project Structure

```text
RETINAL_AI/
├── api.py
├── model.py
├── blindness.py
├── train_model.py
├── train_model_baseline.py
├── train_model_frozen_head.py
├── model_baseline.py
├── model_frozen_head.py
├── evaluate_model.py
├── evaluate_frozen_head.py
├── download_sample.py
├── download_evaluation.py
├── download_expanded_train.py
├── requirements.txt
├── README.md
├── sampleimages/
├── images/
└── frontend/
    ├── package.json
    ├── package-lock.json
    ├── index.html
    └── src/
        ├── App.jsx
        ├── App.css
        └── main.jsx
```

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.11 recommended
- Node.js and npm
- Git
- The trained model checkpoint, `classifier_improved.pt`

### 1. Clone the repository

```bash
git clone https://github.com/Melkin7/RETINAL_AI.git
cd RETINAL_AI
```

### 2. Create and activate a Python virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install backend dependencies

Install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

If additional dependencies are missing, install the packages required by `api.py` and `model.py`, including FastAPI, Uvicorn, PyTorch, TorchVision, Pillow, and `python-multipart`.

### 4. Obtain the model checkpoint

Place the trained `classifier_improved.pt` file in the repository root, alongside `model.py` and `api.py`.

The checkpoint is not included in the Git repository because it exceeds GitHub's regular Git file-size limit. You must obtain it separately before running predictions.

### 5. Start the FastAPI backend

From the repository root:

```bash
python -m uvicorn api:app --reload
```

The backend runs at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Keep this terminal running.

### 6. Start the React frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local frontend address printed by Vite, usually:

http://localhost:5173

Keep both servers running while using the application.

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome information and class labels |
| GET | `/health` | Check API health and model loading status |
| POST | `/predict` | Upload a retinal image and receive a prediction |

### Example prediction response

```json
{
  "predicted_grade": 2,
  "predicted_class": "Moderate DR",
  "predicted_probability": 0.79,
  "warning": "Experimental model; not for clinical diagnosis."
}
```

This is an illustrative response format. Actual predictions and probabilities depend on the uploaded image.

### Test the API

Open http://127.0.0.1:8000/docs, expand `POST /predict`, upload a JPEG or PNG image, and execute the request.

## 📊 Dataset and Evaluation

The project uses the [APTOS 2019 Blindness Detection dataset](https://www.kaggle.com/competitions/aptos2019-blindness-detection/data).

The dataset contains retinal fundus images labeled with diabetic retinopathy severity grades from 0 to 4. Training and evaluation scripts are included in the repository.

Model performance depends on the checkpoint, dataset split, preprocessing, and evaluation procedure. Results from experimental checkpoints should not be interpreted as evidence of clinical readiness.

## 🔒 Privacy and Security

- Do not commit virtual environments, credentials, API secrets, or local user databases.
- Uploaded images are processed by the local API in the current demo configuration.
- Review and configure data handling before deploying the application publicly.
- Use appropriate security, privacy, and access controls before handling real patient data.

## ⚠️ Limitations and Medical Disclaimer

Retinal AI is a student research and demonstration project. It has not been established as a clinically validated diagnostic system.

- Predictions may be incorrect, including for severe disease.
- Model probabilities are not clinically calibrated confidence estimates.
- Image quality and differences between datasets may affect performance.
- The application must not replace professional eye examinations or advice from qualified healthcare professionals.

## 🚀 Future Improvements

- Deploy the frontend and backend for remote demonstrations.
- Host the model checkpoint through an appropriate large-file storage service.
- Add automated testing and continuous integration.
- Improve model evaluation across diverse populations and image conditions.
- Explore explainability tools for retinal image analysis.
- Investigate multilingual support, including Tamil.

## 👥 Team

### Team Lead
**Adithya S** — System architecture, AI workflow planning, project coordination

### Core Contributors
**Nhowmitha S** — GUI design, preprocessing, model integration, evaluation

**Melkin S** — AI module development, dataset preparation, model training, performance analysis

### Key Contributor
**Bhavadharini G** — Application workflow design, UI/UX support, testing, documentation

### Mentor
**Mr. DL Mathew Valan** — Technical guidance and project review

## 🙏 Acknowledgments

- APTOS and the Kaggle community for the retinal image dataset.
- The project team and mentor for their contributions and guidance.

## 📄 License

The project previously described itself as MIT-licensed. Ensure a corresponding `LICENSE` file is present in the repository before distributing it under that license.

---

**Retinal AI — Empowering Vision Through Intelligence.** 👁️