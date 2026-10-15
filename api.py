
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
import io

from model import load_model, inference, CLASSES

app = FastAPI(
    title="Retinal AI API",
    description="Experimental diabetic retinopathy image classification API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Load the trained model once when the API starts.
model = load_model()


@app.get("/")
def home():
    return {
        "message": "Retinal AI API is running",
        "classes": CLASSES,
    }


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(
            status_code=415,
            detail="Upload a JPEG or PNG retinal image.",
        )

    image_bytes = await file.read()

    if not image_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image must be 10 MB or smaller.")

    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            image.verify()

        # Save a validated temporary image for the existing inference function.
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".png") as temp:
            with Image.open(io.BytesIO(image_bytes)) as image:
                image.convert("RGB").save(temp.name, format="PNG")

            grade, prediction, probability = inference(model, temp.name)

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(status_code=400, detail="The uploaded file is not a valid image.")

    return {
        "predicted_grade": grade,
        "predicted_class": prediction,
        "predicted_probability": round(probability, 4),
        "warning": "Experimental model; not for clinical diagnosis.",
    }

