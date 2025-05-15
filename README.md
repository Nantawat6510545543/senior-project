# Self-Supervised Learning for EEG-Based Motor Imagery Classification

## Team Members

1. Nantawat Sukrisunt – 6510545543
2. Naytitorn Chaovirachot – 6510545560

Both team members are undergraduate students from the Department of Computer Engineering, Faculty of Engineering,
Kasetsart University.

## Project Overview

This project explores the use of Self-Supervised Learning (SSL) to enhance the classification of EEG-based Motor
Imagery (MI) signals. Traditional supervised learning methods often face limitations in accuracy due to the high
variability of EEG signals across subjects, susceptibility to noise, and the scarcity of labeled data.

To overcome these challenges, we leverage unlabeled data from diverse EEG paradigms—including Steady-State Visual Evoked
Potentials (SSVEPs) and Event-Related Potentials (ERPs)—to learn general-purpose semantic embeddings. These embeddings
are then used to improve MI signal classification through transfer learning.

Our approach significantly reduces reliance on labeled data and enhances cross-subject generalization, aiming to
outperform conventional supervised learning methods. By integrating information from multiple paradigms into a unified
SSL framework, we aim to deliver a more robust and scalable solution for EEG decoding tasks.

**This project is a collaborative effort between Kasetsart University and the Vidyasirimedhi Institute of Science and
Technology (VISTEC), combining expertise in software engineering, neuroscience, and machine learning.**

## Project Execution Guide

This project has two parts:

- Backend: FastAPI (Python)
- Frontend: React + Vite + TypeScript

### Backend (FastAPI)

#### 1. Create and activate virtual environment

```  
python -m venv .venv
# Activate environment
source .venv/bin/activate       # Linux/macOS  
.venv\Scripts\activate          # Windows  
```

#### 2. Install dependencies

Run this in the root directory:  
```  
pip install -r requirements.txt  
```

#### 3. Start the FastAPI server

Navigate to the backend app directory and run:  
```  
cd backend/app  
uvicorn main:app --reload  
```

Access API at:

- API root: http://127.0.0.1:3000
- Swagger UI: http://127.0.0.1:3000/docs

### Frontend (Vite + React + TypeScript)

#### 1. Install dependencies

In the project root (where `package.json` is located), run:  
```  
npm install  
```

#### 2. Start the development server

```  
npm run dev  
```

Access frontend at:  
http://localhost:3000
