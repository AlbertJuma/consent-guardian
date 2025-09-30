# Installation and Setup Guide

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher**
- **Node.js 20 or higher** 
- **npm or yarn**
- **Docker and Docker Compose** (optional, for containerized deployment)
- **Git**

## Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.11+

# Check Node version
node --version  # Should be 20+

# Check npm version
npm --version

# Check Docker (optional)
docker --version
docker-compose --version
```

## Installation Methods

### Method 1: Quick Start with Docker Compose (Recommended)

This is the easiest way to run the complete demo:

```bash
# 1. Clone the repository
git clone https://github.com/AlbertJuma/consent-guardian.git
cd consent-guardian

# 2. Start all services
docker-compose up

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs

# 4. Stop services
# Press Ctrl+C or run:
docker-compose down
```

### Method 2: Local Development Setup

For development or if you prefer running without Docker:

#### Step 1: Clone Repository

```bash
git clone https://github.com/AlbertJuma/consent-guardian.git
cd consent-guardian
```

#### Step 2: Set Up Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Return to root directory
cd ..
```

#### Step 3: Set Up Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Return to root directory
cd ..
```

#### Step 4: Run Backend

```bash
# From the backend directory (with venv activated)
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Backend will be available at http://localhost:8000
```

#### Step 5: Run Frontend (in a new terminal)

```bash
# Navigate to frontend directory
cd frontend

# Start development server
npm run dev

# Frontend will be available at http://localhost:3000
```

### Method 3: CLI Demo Only

If you just want to see the demo without running the full application:

```bash
# 1. Clone the repository
git clone https://github.com/AlbertJuma/consent-guardian.git
cd consent-guardian

# 2. Install Python dependencies
pip install -r backend/requirements.txt

# 3. Run the demo script
python demo_run.py

# This will run a complete demo using synthetic images and output to console
```

## Verification Steps

### 1. Verify Safety Configuration

Run the safety verification script:

```bash
python verify_safety.py
```

All checks should pass with green checkmarks (✓).

### 2. Run Tests

```bash
# Install test dependencies
pip install -r backend/requirements.txt
pip install -r tests/requirements.txt

# Run unit tests
cd tests
pytest test_hash.py -v

# All 16 tests should pass
```

### 3. Test Backend API

```bash
# Test health endpoint
curl http://localhost:8000/

# Test hash computation (with backend running)
curl -X POST "http://localhost:8000/hash-local" \
  -F "file=@backend/demo_data/consent_photos/demo_image_1.jpg"

# You should see a JSON response with the computed hash
```

### 4. Access Frontend

Open your browser and navigate to:
- http://localhost:3000

You should see the Consent Guardian interface with safety warnings.

## Configuration (Optional)

### Custom Configuration

If you want to customize settings:

```bash
# Copy example config
cd backend/app
cp config.example.yaml config.yaml

# Edit config.yaml (this file is gitignored)
# Note: Keep allow_external_fetch: false for demo
```

### Environment Variables

For the frontend, you can set the API URL:

```bash
# Create .env file in frontend directory
cd frontend
echo "VITE_API_URL=http://localhost:8000" > .env
```

## Troubleshooting

### Port Already in Use

If port 8000 or 3000 is already in use:

```bash
# For backend, use a different port:
uvicorn app.main:app --port 8001

# For frontend, update vite.config.js or use:
npm run dev -- --port 3001
```

### Python Virtual Environment Issues

```bash
# Deactivate current venv
deactivate

# Remove old venv
rm -rf venv

# Create new venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Node/npm Issues

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Docker Issues

```bash
# Remove all containers and volumes
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Start fresh
docker-compose up
```

## Development Workflow

### Making Code Changes

1. **Backend changes**: Edit files in `backend/app/`, the server will auto-reload
2. **Frontend changes**: Edit files in `frontend/src/`, Vite will hot-reload
3. **Run tests** after changes: `pytest tests/test_hash.py -v`

### Adding Dependencies

#### Backend
```bash
# Add to requirements.txt
echo "new-package==1.0.0" >> backend/requirements.txt
pip install -r backend/requirements.txt
```

#### Frontend
```bash
cd frontend
npm install new-package
```

## Production Deployment

⚠️ **IMPORTANT**: This POC is NOT ready for production deployment.

Before any real-world use:
1. Complete legal review
2. Establish partnerships
3. Security audit
4. Privacy impact assessment
5. See [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md) for complete requirements

## Uninstallation

### Remove Local Installation

```bash
# Remove project directory
rm -rf consent-guardian
```

### Stop Docker Containers

```bash
# Stop and remove containers
docker-compose down -v

# Remove images (optional)
docker-compose down --rmi all
```

## Next Steps

After installation:

1. **Read the documentation**:
   - [README.md](../README.md) - Project overview
   - [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md) - Critical safety info
   - [presenter_script.md](docs/presenter_script.md) - How to demo safely

2. **Run the CLI demo**:
   ```bash
   python demo_run.py
   ```

3. **Explore the API**:
   - API Documentation: http://localhost:8000/docs
   - Try the interactive Swagger UI

4. **Test the frontend**:
   - Upload a demo image from `backend/demo_data/consent_photos/`
   - Follow the workflow steps

## Getting Help

- **Technical issues**: Open a GitHub issue
- **Safety concerns**: See [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md) for hotline contacts
- **Questions**: Review the documentation first

## Important Reminders

- ✅ This is a **DEMO ONLY**
- ✅ Use only **synthetic/consenting images**
- ✅ All external features are **DISABLED by default**
- ✅ **Never** process suspected illegal content
- ✅ **Always** have explicit consent

---

**Safety First, Always.**
