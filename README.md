# Engine Life Analysis: Remaining Useful Life Prediction

An end-to-end machine learning system for predictive maintenance using NASA's CMAPSS turbofan engine dataset.

## Setup Instructions

### 1. Local Development Setup

**Backend API:**
```bash
# Install required Python dependencies
pip install -r requirements.txt

# Start the FastAPI backend
python backend/main.py
# The server will start on http://localhost:8000
```

**Frontend Dashboard:**
```bash
# Navigate to the frontend directory
cd frontend

# Install Node dependencies (only required the first time)
npm install

# Start the React development server
npm run dev
# The interactive dashboard will be available at http://localhost:5173
```

### 2. Docker Deployment (Backend)

For a reproducible, portable deployment, you can run the machine learning backend entirely inside a Docker container.

**Build the Docker Image:**
Run this command from the root of the repository:
```bash
docker build -t engine-life-analysis .
```

**Run the Docker Container:**
```bash
docker run -p 8000:8000 engine-life-analysis
```

The API will be available at `http://localhost:8000`. You can test it by visiting the interactive documentation at `http://localhost:8000/docs`.

*(Note: The React frontend can still be run locally using `npm run dev` and will seamlessly connect to your new Dockerized backend!)*
