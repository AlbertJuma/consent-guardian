# Quick Start Guide

## 🚀 Get Started in 5 Minutes

This guide will get you up and running with the Consent Guardian POC quickly.

## Prerequisites

- Docker and Docker Compose installed
- OR Python 3.11+ and Node.js 20+ installed

## Option 1: Docker (Easiest - Recommended)

### 1. Clone and Start

```bash
git clone https://github.com/AlbertJuma/consent-guardian.git
cd consent-guardian
docker-compose up
```

### 2. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Try the Demo

1. Open http://localhost:3000 in your browser
2. Click "Choose File" and select `backend/demo_data/consent_photos/demo_image_1.jpg`
3. Click "Compute Hash"
4. Click "Run Safe Search (Demo)"
5. View the results and try "Generate Takedown" for matches

### 4. Stop When Done

```bash
# Press Ctrl+C or run:
docker-compose down
```

## Option 2: CLI Demo (No Server)

Perfect for quick testing:

```bash
# 1. Clone
git clone https://github.com/AlbertJuma/consent-guardian.git
cd consent-guardian

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Run demo
python demo_run.py
```

You'll see a complete demo workflow in your terminal.

## Option 3: Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend at: http://localhost:8000

### Frontend (new terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend at: http://localhost:3000

## Verification

### Check Everything Works

```bash
# Run safety checks
python verify_safety.py

# Run tests
pytest tests/test_hash.py -v

# Test API (if backend running)
curl http://localhost:8000/
```

All should show green checkmarks and pass.

## Demo Workflow

1. **Upload Image**: Use synthetic demo image
2. **Compute Hash**: Get perceptual hash
3. **Run Search**: See mock results (safe)
4. **View Results**: Similarity scores displayed
5. **Generate Template**: Create takedown request
6. **Download Report**: Export metadata JSON

## Important Safety Notes

⚠️ **DEMO ONLY** - Not for production use  
⚠️ **Use synthetic images only** - No real photos  
⚠️ **Mock results** - Real APIs disabled by default  
⚠️ **If you see illegal content** - Report to authorities immediately  

## Resources

- **Full Documentation**: [README.md](README.md)
- **Safety Guidelines**: [docs/SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md)
- **Installation**: [docs/INSTALLATION.md](docs/INSTALLATION.md)
- **Presenting**: [docs/presenter_script.md](docs/presenter_script.md)

## Troubleshooting

**Port already in use?**
```bash
# Change backend port
uvicorn app.main:app --port 8001

# Change frontend port
npm run dev -- --port 3001
```

**Dependencies failing?**
```bash
# Clear and reinstall
pip install --upgrade pip
pip install -r backend/requirements.txt --force-reinstall
```

**Docker issues?**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

## Next Steps

After quick start:

1. ✅ Read [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md)
2. ✅ Explore the API docs at http://localhost:8000/docs
3. ✅ Run the CLI demo: `python demo_run.py`
4. ✅ Review the code in `backend/app/`
5. ✅ Check out the frontend in `frontend/src/`

## Questions?

- Check [README.md](README.md) for detailed info
- Review [docs/INSTALLATION.md](docs/INSTALLATION.md) for setup help
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

---

**Remember**: This is a safe, educational demo. Always prioritize safety and ethics.

Happy exploring! 🎉
