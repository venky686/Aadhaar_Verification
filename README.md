# Aadhaar Verification AI System

A production-ready AI system for Aadhaar document verification and fraud detection using Azure AI, YOLOv8, and Deep Learning.

## 🎥 Project Demo

[**▶️ Watch Project Demo Video**](staticFileDoc/Video/Project%20Demo.mp4)

*(Note: Click the link above to play the video locally or download it)*

---

## 📖 Detailed Project Explanation

### Overview
This project is an end-to-end solution designed to automate the verification of Indian Aadhaar cards. It addresses the challenge of identity fraud by combining traditional OCR (Optical Character Recognition) with advanced Computer Vision and Deep Learning techniques. The system not only extracts data but also actively looks for signs of tampering, forgery, and poor image quality.

### Architecture & Workflow

The system follows a microservices-like architecture within a modular Python application:

1.  **Input Layer**: The user uploads an image (JPG/PNG) or PDF via the FastAPI REST endpoint.
2.  **Preprocessing Module**:
    *   **Cleaning**: Removes noise and normalizes lighting.
    *   **Deskewing**: Corrects the orientation of scanned documents.
    *   **Quality Check**: Rejects images that are too blurry or dark to process.
3.  **Fraud Detection Engine**:
    *   **YOLOv8**: Scans for specific object classes like the Aadhaar logo, QR code, and face. It also detects "tampered text" artifacts.
    *   **Anomaly Detection**: A deep learning model (Autoencoder) checks if the overall document structure deviates from a "normal" Aadhaar card.
    *   **Forgery Rules**: Checks for metadata inconsistencies (e.g., edited by Photoshop).
4.  **OCR & Extraction (Azure AI)**:
    *   The image is sent to **Azure AI Document Intelligence** (formerly Form Recognizer).
    *   The `prebuilt-idDocument` model extracts fields like Name, DOB, Gender, and Aadhaar Number.
5.  **Validation & Refinement (Azure OpenAI)**:
    *   Extracted text is validated (e.g., Verhoeff algorithm for Aadhaar numbers).
    *   **Azure OpenAI (GPT)** is used to correct OCR typos (e.g., '0' vs 'O') and normalize address formats.
6.  **Scoring & Decision**:
    *   A weighted algorithm calculates a **Final Risk Score** based on OCR confidence, fraud probability, and anomaly score.
    *   The system outputs a decision: **SAFE**, **REVIEW**, or **FRAUD**.

---

## ☁️ Azure Configuration & Setup

This project relies on Azure AI services. Below are the steps and screenshots for setting them up.

### 1. Azure Document Intelligence (Form Recognizer)
Used for extracting text and structured data from the ID cards.

*Create a Document Intelligence resource in the Azure Portal and get your Endpoint and Key.*

![Azure Form Recognizer Setup](staticFileDoc/Azure/FORM_RECOGNIZER_IMAGE/Screenshot%202025-12-17%20204957.png)
![Keys and Endpoint](staticFileDoc/Azure/FORM_RECOGNIZER_IMAGE/Screenshot%202025-12-17%20205017.png)

### 2. Azure OpenAI
Used for intelligent text correction and data normalization.

*Deploy a GPT model (e.g., gpt-35-turbo) in Azure OpenAI Studio.*

![Azure OpenAI Resource](staticFileDoc/Azure/OPENAI/Screenshot%202025-12-17%20205521.png)
![Model Deployment](staticFileDoc/Azure/OPENAI/Screenshot%202025-12-17%20205550.png)

---

## 🚀 Features

- **AI-Powered OCR**: Extracts data using Azure AI Document Intelligence.
- **Fraud Detection**: Detects tampering, photo manipulation, and missing security features using YOLOv8.
- **Data Validation**: Rule-based and LLM-based (Azure OpenAI) validation of extracted fields.
- **Quality Check**: Analyzes image blur, lighting, and skew.
- **Risk Scoring**: Calculates a comprehensive risk score to flag fraudulent documents.
- **API First**: Built with FastAPI for easy integration.

## 📂 Project Structure

```
aadhaar-verification/
├── api/                # FastAPI application
├── data/               # Dataset for training/testing
├── docker/             # Docker configuration
├── fraud_detection/    # YOLO and Anomaly detection models
├── llm/                # Azure OpenAI integration
├── ocr/                # Azure Document Intelligence integration
├── preprocessing/      # Image cleaning and quality metrics
├── scoring/            # Risk scoring logic
├── utils/              # Config and logging
└── requirements.txt    # Python dependencies
```

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **API**: FastAPI
- **OCR**: Azure AI Document Intelligence
- **LLM**: Azure OpenAI (GPT-4/3.5)
- **Vision**: OpenCV, YOLOv8 (Ultralytics)
- **Container**: Docker

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone <repo-url>
cd aadhaar-verification
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and fill in your Azure credentials.
```bash
cp .env.example .env
```

Required variables:
- `AZURE_FORM_RECOGNIZER_ENDPOINT`
- `AZURE_FORM_RECOGNIZER_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_KEY`
- `AZURE_OPENAI_DEPLOYMENT_NAME`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`.
Swagger documentation: `http://localhost:8000/docs`.

## 🐳 Docker Deployment

Build and run the container:

```bash
docker build -t aadhaar-verification -f docker/Dockerfile .
docker run -p 8000:8000 --env-file .env aadhaar-verification
```

## 📡 API Usage

**Endpoint**: `POST /api/v1/verify-document`

**Request**: `multipart/form-data` with `file` field.

**Response**:
```json
{
  "extracted_data": {
    "name": "John Doe",
    "aadhaar_number": "123456789012",
    ...
  },
  "scores": {
    "ocr_confidence": 0.98,
    "fraud_score": 0.1,
    "final_risk_score": 15.5
  },
  "decision": "SAFE"
}
```

## 🧠 Model Training (YOLOv8)

To train the fraud detection model on your dataset:

1. Organize data in `data/` folder (images and labels).
2. Run training:
```python
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
model.train(data="data/data.yaml", epochs=100)
```
3. Update `YOLO_MODEL_PATH` in `.env`.

## 📝 License

MIT License
