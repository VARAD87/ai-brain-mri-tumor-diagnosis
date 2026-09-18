# 🧠 AI-Powered Brain MRI Tumor Detection & Diagnosis System

This project presents an end-to-end **AI-based medical diagnosis system** that detects, classifies, and segments brain tumors from MRI images using deep learning.  
It is designed as a **Doctor Portal System** with a professional web interface and automated medical report generation.

---

## Key Features

-  Brain tumor **classification** (Glioma, Meningioma, Pituitary, No Tumor)
-  **GAN-based data augmentation** for improved robustness
-  **U-Net tumor segmentation** with Dice score evaluation
-  Professional **Doctor Portal (Streamlit)**
-  Tumor **confidence score**
-  **Tumor mask overlay visualization**
-  Automated **PDF diagnostic report generation**
-  **Report history management**
-  Fully offline (runs on local laptop)

---

## 🛠 Technology Stack

### Programming & Frameworks
- Python
- PyTorch
- Streamlit

### Deep Learning Models
- CNN (Tumor Classification)
- DCGAN (Synthetic MRI Image Generation)
- U-Net (Tumor Segmentation)

### Medical Imaging & Processing
- OpenCV
- MONAI
- Nibabel

### Reporting & Visualization
- FPDF / ReportLab
- Matplotlib
- Seaborn

---

##  Project Structure

ai-brain-mri-tumor-diagnosis/
│
├── app.py # Main Doctor Portal
├── pages/ # Multi-page Streamlit UI
│ ├── 1_Patient_Registration.py
│ ├── 2_MRI_Diagnosis.py
│ ├── 3_Report_Generation.py
│ └── 4_Report_History.py
│
├── src/
│ ├── models/ # CNN models
│ ├── gan/ # GAN augmentation
│ ├── segmentation/ # U-Net segmentation
│ ├── training/ # Training scripts
│ └── visualization/
│
├── reports/
│ ├── figures/
│ └── history/
│
├── requirements.txt
└── README.md


---

## Setup Instructions (For Teammates)

### 1️ Clone Repository
```bash
git clone https://github.com/escapist0411/ai-brain-mri-tumor-diagnosis.git
cd ai-brain-mri-tumor-diagnosis
2️ Create Virtual Environment
python -m venv .venv

3️ Activate Environment

Windows (CMD / PowerShell):

.venv\Scripts\activate

4️ Install Dependencies
pip install -r requirements.txt

5️ Run Doctor Portal
streamlit run app.py
