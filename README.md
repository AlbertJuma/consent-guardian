# Consent Guardian - Proof of Concept

> ⚠️ **CRITICAL SAFETY NOTICE**: This is a **PROOF-OF-CONCEPT DEMONSTRATION ONLY**. This software is NOT intended for production use or for handling actual cases of non-consensual image distribution. See [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md) for complete safety guidelines.

## One-Paragraph Legal Disclaimer

**This software is provided "AS IS" without warranty of any kind. It is a demonstration of technical concepts only and must NOT be used to process suspected illegal content (especially CSAM - immediately report to NCMEC/law enforcement). This software does NOT scrape websites, does NOT store images, and uses MOCK search results by default. Users are solely responsible for ensuring their use complies with all applicable laws. By using this software, you agree to use it only for educational purposes with explicit consent for all processed images. THE AUTHORS DISCLAIM ALL LIABILITY FOR MISUSE.**

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Safety Constraints](#safety-constraints)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Demo Workflow](#demo-workflow)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Legal and Ethical Considerations](#legal-and-ethical-considerations)
- [Resources and Support](#resources-and-support)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Consent Guardian is a proof-of-concept demonstration that shows how perceptual hashing and reverse image search APIs could potentially help people identify non-consensual images online. This POC demonstrates:

- **Local-first image processing** using perceptual hashing (pHash)
- **Mock reverse image search** workflow (real APIs disabled by default)
- **In-memory thumbnail comparison** without persistence
- **Takedown request template generation** for potential matches
- **Strict safety and legal safeguards** throughout

### What This Project IS:

✅ An educational demonstration  
✅ A technical feasibility study  
✅ A starting point for discussion about ethical AI  
✅ A showcase of safety-first design principles  

### What This Project IS NOT:

❌ Production-ready software  
❌ A complete solution to non-consensual image distribution  
❌ Suitable for processing suspected illegal content  
❌ A web scraping tool (NO scraping functionality)  
❌ A replacement for professional legal or counseling services  

---

## Key Features

### Technical Features

- **Perceptual Hashing**: Compute pHash fingerprints of images using the `imagehash` library
- **Similarity Comparison**: Compare images using Hamming distance on perceptual hashes
- **Mock Search API**: Demonstrates reverse image search workflow with safe mock data
- **Takedown Templates**: Generate pre-filled takedown request messages
- **Metadata Export**: Download JSON reports with URLs and similarity scores (no images)

### Safety Features

- **No Image Persistence**: All processing in memory using `BytesIO` - no files saved
- **Mock APIs by Default**: External fetch disabled (`allow_external_fetch=false`)
- **Strict Size Limits**: Max 10MB uploads, 256KB thumbnail fetches
- **Timeouts**: 10-second timeout on all external requests
- **Safe Logging**: Only URLs, timestamps, and similarity scores - no PII
- **Consent-First**: Explicit warnings about consent requirements throughout UI

---

## Safety Constraints

### 🚨 CRITICAL: Before Using This Software

1. **Read [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md)** in full
2. **Never process images without explicit consent**
3. **If you encounter suspected CSAM**:
   - STOP immediately
   - Report to NCMEC CyberTipline: https://www.cybertipline.org
   - Contact law enforcement
   - DO NOT process or investigate further

4. **This software does NOT**:
   - Scrape websites
   - Store images
   - Connect to real APIs (by default)
   - Handle production use cases

---

## Quick Start

### Prerequisites

- Python 3.11+ (for backend)
- Node.js 20+ (for frontend)
- Docker & Docker Compose (optional, for containerized deployment)

### Option 1: Docker Compose (Recommended for Demo)

```bash
# Clone the repository
git clone https://github.com/AlbertJuma/consent-guardian.git
cd consent-guardian

# Start all services
docker-compose up

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
uvicorn app.main:app --reload

# Backend now running at http://localhost:8000
```

#### Frontend Setup

```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Run the frontend
npm run dev

# Frontend now running at http://localhost:3000
```

### Option 3: CLI Demo Only

```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Run the demo script
python demo_run.py

# This will run a complete demo using synthetic test images
```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (React)                    │
│  - Upload UI                                             │
│  - Results Table                                         │
│  - Takedown Template Generator                          │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP/JSON
                 │
┌────────────────▼────────────────────────────────────────┐
│                   Backend (FastAPI)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │ POST /hash-local                                 │   │
│  │  - Compute pHash from uploaded image             │   │
│  │  - Return hash + metadata                        │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ POST /search-proxy                               │   │
│  │  - Return MOCK candidate URLs                    │   │
│  │  - (Real APIs disabled by default)               │   │
│  └──────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ POST /compare                                    │   │
│  │  - Fetch thumbnails (in-memory only)             │   │
│  │  - Compute similarity scores                     │   │
│  │  - Return matches above threshold                │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User uploads image** → Frontend
2. **Image sent to backend** → `/hash-local` endpoint
3. **pHash computed in memory** → No persistence
4. **Hash returned to frontend** → Display to user
5. **User initiates search** → `/search-proxy` endpoint
6. **Mock candidates returned** → (Real search disabled)
7. **Thumbnails compared** → `/compare` endpoint
8. **Similarity scores computed** → Results displayed
9. **Takedown template generated** → For matches above threshold

**No images are stored at any step.**

---

## Demo Workflow

### Step 1: Upload Image

- Select a consenting test image (use demo images from `/backend/demo_data/consent_photos/`)
- Click "Compute Hash"
- View perceptual hash and metadata

### Step 2: Run Search (Demo Mode)

- Click "Run Safe Search (Demo)"
- Receives MOCK candidate URLs (real APIs disabled)
- View notice that results are simulated

### Step 3: View Results

- See table of candidate URLs with similarity scores
- Matches above 85% threshold highlighted
- Progress bars show similarity visually

### Step 4: Generate Takedown Template

- Click "Generate Takedown" for any match
- View pre-filled template with URL and similarity score
- Copy template to clipboard
- See warnings about not attaching images and reporting illegal content

### Step 5: Download Report

- Click "Download Report (Metadata Only)"
- JSON file contains only URLs and scores - no images

---

## Configuration

### Config File: `backend/app/config.example.yaml`

**Copy to `config.yaml` for customization (gitignored):**

```bash
cd backend/app
cp config.example.yaml config.yaml
```

### Key Configuration Options

```yaml
# SAFETY TOGGLES - MUST REMAIN FALSE FOR DEMO
allow_external_fetch: false  # Enable external thumbnail fetching
escalate_to_hotline: false   # Enable hotline escalation

# API KEYS (only use after legal review)
api_keys:
  tineye: "YOUR_KEY_HERE"
  bing_visual_search: "YOUR_KEY_HERE"

# RATE LIMITS
rate_limits:
  hash_local: 10  # requests per minute
  search_proxy: 5
  compare: 5

# SIMILARITY THRESHOLD
similarity_threshold: 0.85  # 85% similarity for matches
```

### ⚠️ Before Enabling External Features

See [SAFETY_AND_LEGAL.md - Checklist](docs/SAFETY_AND_LEGAL.md#checklist-before-enabling-real-features) for requirements before setting `allow_external_fetch=true`.

---

## Development

### Project Structure

```
consent-guardian/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── hash_utils.py        # Perceptual hashing functions
│   │   ├── config.example.yaml  # Configuration template
│   │   └── __init__.py
│   ├── demo_data/
│   │   └── consent_photos/      # Safe demo images
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── api.js               # API client
│   │   └── main.jsx             # Entry point
│   ├── package.json
│   └── vite.config.js
├── tests/
│   ├── test_hash.py             # Unit tests
│   └── requirements.txt
├── docs/
│   ├── SAFETY_AND_LEGAL.md      # Complete safety guidelines
│   └── presenter_script.md      # Demo presentation guide
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline
├── demo_run.py                  # CLI demo script
├── docker-compose.yml
├── Dockerfile
├── LICENSE
└── README.md
```

### Adding Features

**Before adding any feature that involves external data:**

1. Review [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md)
2. Add safety constraints to code
3. Add configuration gates
4. Update documentation
5. Add tests for safety constraints
6. Get legal review if applicable

### Code Style

- Python: Follow PEP 8
- JavaScript: ESLint configuration in frontend
- All external calls must have timeouts
- All file operations must be in-memory (BytesIO)
- No hardcoded API keys

---

## Testing

### Run Backend Tests

```bash
# Install test dependencies
pip install -r backend/requirements.txt
pip install -r tests/requirements.txt

# Run tests
cd tests
pytest test_hash.py -v

# Run with coverage
pytest test_hash.py --cov=backend/app --cov-report=html
```

### Run Demo Script

```bash
python demo_run.py
```

This runs a complete demo workflow using synthetic images and outputs results to stdout.

### Manual Testing Checklist

- [ ] Upload image and compute hash
- [ ] Hash is 16 hex characters
- [ ] Metadata shows correct format and size
- [ ] Search returns mock results with warning
- [ ] Comparison shows similarity scores
- [ ] Matches above threshold are highlighted
- [ ] Takedown template generates correctly
- [ ] Report downloads as JSON (no images)
- [ ] No files created in backend directory
- [ ] Safety warnings visible throughout UI

---

## Deployment

### ⚠️ Important: This POC is NOT for Production Deployment

This software is a **demonstration only**. Before any real-world deployment:

1. Complete legal review
2. Establish partnerships with API providers and hotlines
3. Conduct security audit and penetration testing
4. Complete privacy impact assessment
5. Implement proper authentication and authorization
6. Add monitoring and alerting
7. Establish incident response procedures
8. Train staff on handling sensitive reports

See [SAFETY_AND_LEGAL.md - Partner Integration Requirements](docs/SAFETY_AND_LEGAL.md#partner-integration-requirements).

### Local Demo Deployment Only

#### Using Docker Compose

```bash
docker-compose up -d
```

#### Manual Deployment

```bash
# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm run preview
```

---

## Legal and Ethical Considerations

### Must-Read Documents

1. **[SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md)** - Complete safety and legal guidelines
2. **[presenter_script.md](docs/presenter_script.md)** - How to present this POC safely

### Key Principles

1. **Consent First**: Only process images with explicit consent
2. **No Persistence**: Never store images
3. **No Scraping**: Do not scrape websites or violate ToS
4. **Report Illegal Content**: CSAM must be reported to authorities immediately
5. **Transparency**: Be clear about limitations and capabilities
6. **Privacy**: Protect user data and personal information
7. **Do No Harm**: Avoid re-victimizing people

### Legal Requirements

- Compliance with GDPR, CCPA, and applicable privacy laws
- Respect website terms of service
- Mandatory reporting laws (vary by jurisdiction)
- Copyright and intellectual property considerations
- Professional liability and insurance

---

## Resources and Support

### If You Encounter Illegal Content

**STOP and report immediately. DO NOT investigate or process.**

- **NCMEC CyberTipline** (US): https://www.cybertipline.org | 1-800-843-5678
- **INHOPE Network** (International): https://www.inhope.org
- **FBI Internet Crime Complaint Center**: https://www.ic3.gov
- **Local law enforcement**: Call your local emergency number

### Support for Victims

- **Revenge Porn Helpline** (UK, but has US resources): https://revengepornhelpline.org.uk
- **Cyber Civil Rights Initiative**: https://www.cybercivilrights.org
- **RAINN** (US): https://www.rainn.org | 1-800-656-4673
- **Crisis Text Line**: Text HOME to 741741

### Technical Resources

- **Perceptual Hashing**: http://www.phash.org/
- **imagehash Library**: https://github.com/JohannesBuchner/imagehash
- **PhotoDNA** (law enforcement only): https://www.microsoft.com/en-us/photodna

---

## Contributing

### How to Contribute

We welcome contributions that:

- Improve safety constraints
- Enhance documentation
- Add tests
- Fix bugs
- Improve error handling

### Contribution Guidelines

1. **Read [SAFETY_AND_LEGAL.md](docs/SAFETY_AND_LEGAL.md)** first
2. **Do NOT** add features that:
   - Remove safety constraints
   - Enable scraping
   - Store images
   - Bypass configuration gates
3. **All PRs must**:
   - Include tests
   - Update documentation
   - Pass CI checks
   - Maintain safety-first design

### Reporting Issues

- Use GitHub Issues for technical bugs only
- Do NOT share sensitive content in issues
- For safety/legal concerns, contact appropriate authorities first

---

## License

This project is licensed under the MIT License with additional safety disclaimers - see [LICENSE](LICENSE) file.

**Important**: The license includes explicit disclaimers about:
- Educational/demonstration purpose only
- No warranty or liability
- Prohibition on processing CSAM
- User responsibility for legal compliance

---

## Acknowledgments

This project is inspired by the important work of organizations fighting non-consensual image distribution:

- National Center for Missing & Exploited Children (NCMEC)
- INHOPE Network
- Cyber Civil Rights Initiative
- Revenge Porn Helpline
- All hotline operators and victim advocates

**Technology is only one piece of the solution. Professional support and legal frameworks are essential.**

---

## Contact

For questions about this project:
- **Technical questions**: Open a GitHub issue
- **Safety concerns**: Contact appropriate authorities first (see Resources above)
- **Partnership inquiries**: (Placeholder - not currently accepting)

---

**Remember: Safety First, Always.**

If you're uncertain about anything, err on the side of caution. This is a demonstration of responsible technology development, not a production tool.