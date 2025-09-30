# Presenter Script: Consent Guardian POC Demo

## Overview
This document provides guidance for presenting the Consent Guardian proof-of-concept in a safe, responsible manner.

---

## Pre-Presentation Checklist

- [ ] Review SAFETY_AND_LEGAL.md thoroughly
- [ ] Test demo environment (backend and frontend running)
- [ ] Prepare synthetic demo images only
- [ ] Check that all external APIs are DISABLED (`allow_external_fetch=false`)
- [ ] Prepare content warning for audience
- [ ] Have hotline resources ready to share
- [ ] Practice timing (aim for 10-15 minutes)

---

## Content Warning (Required)

**Say this at the beginning:**

> "Before we begin, I want to provide a content warning. This presentation discusses technology related to non-consensual image distribution, which is a serious issue affecting many people. While we will NOT show any actual sensitive content—only abstract geometric patterns—this topic may be difficult for some. If you need to step away at any time, please feel free to do so. I also have resources for support hotlines available if needed."

---

## Presentation Outline (10-15 minutes)

### 1. Introduction (2 minutes)

**Slide 1: Title**
- Consent Guardian: A Proof-of-Concept for Non-Consensual Image Detection
- Subtitle: Demo Only - Educational Purposes

**Say:**
> "Today I'm presenting a proof-of-concept that demonstrates how perceptual hashing and reverse image search APIs could potentially help people find non-consensual images. This is a DEMO ONLY—not production software. It's designed to explore the technical feasibility while maintaining strict ethical and legal safeguards."

**Slide 2: The Problem**
- Non-consensual image distribution is a serious issue
- Victims often struggle to find and report images
- Technical tools can assist, but must be built safely

**Say:**
> "Non-consensual image distribution affects thousands of people. Victims face significant challenges in locating unauthorized images online. While technology can help, any solution must prioritize safety, consent, and legal compliance."

### 2. Key Safety Principles (3 minutes)

**Slide 3: Safety First**
- ✅ Local-first processing (no cloud storage)
- ✅ No image persistence (memory only)
- ✅ Mock APIs by default
- ✅ Explicit consent required
- ❌ NO scraping
- ❌ NO production use without legal review

**Say:**
> "This POC is built on safety-first principles. All image processing happens locally in memory—nothing is saved to disk. By default, it uses mock search results, not real APIs. Any real-world use would require extensive legal review and partnerships with authorized organizations."

**Slide 4: What This Is NOT**
- NOT a complete solution
- NOT for handling suspected illegal content (CSAM)
- NOT for production use
- NOT a substitute for legal/counseling services

**Say:**
> "It's critical to understand what this is NOT. This is not production-ready. If anyone encounters suspected child sexual abuse material, they must immediately report it to NCMEC, law enforcement, or INHOPE hotlines—NOT process it with tools like this."

### 3. Technical Demo (5 minutes)

**Slide 5: How It Works**
1. User uploads consenting photo
2. System computes perceptual hash (pHash)
3. [Simulated] Reverse image search
4. Compare thumbnails using pHash
5. Generate takedown template for matches

**Say:**
> "Let me walk through the technical workflow. I'll be using only synthetic geometric images—no real photos."

**LIVE DEMO:**

1. **Open the frontend** (http://localhost:3000)
   - Point out the safety warnings
   - Show "DEMO ONLY" notices

2. **Upload a demo image**
   - Use `/demo_data/consent_photos/demo_image_1.jpg`
   - Say: "I'm uploading a safe, synthetic test image—just colored stripes."

3. **Compute hash**
   - Click "Compute Hash"
   - Show the perceptual hash result
   - Say: "The system computes a 64-bit perceptual hash. This hash is like a fingerprint of the image's visual content."

4. **Run search**
   - Click "Run Safe Search (Demo)"
   - Point out the "MOCK results" notice
   - Say: "In this demo, we're using mock search results. Real integration would require legal partnerships with reverse image search providers."

5. **View comparison results**
   - Show the similarity scores
   - Highlight matches vs. non-matches
   - Say: "The system compares perceptual hashes to determine similarity. Matches above 85% similarity are flagged."

6. **Generate takedown template**
   - Click on a match
   - Show the prefilled template
   - Point out the safety warnings
   - Say: "For potential matches, we provide a takedown request template. Notice the warnings—don't attach images, and contact authorities for illegal content."

7. **Download report**
   - Click "Download Report"
   - Open the JSON file
   - Say: "Reports contain only metadata—URLs and similarity scores. No images are included."

### 4. Technical Architecture (2 minutes)

**Slide 6: System Architecture**
- Frontend: React + Tailwind (user interface)
- Backend: FastAPI (Python) with strict safety controls
- Hashing: imagehash library (pHash algorithm)
- Storage: NONE (in-memory only)

**Say:**
> "The architecture is straightforward. A React frontend communicates with a Python FastAPI backend. Images are processed entirely in memory using the imagehash library. There's no database, no cloud storage—just local processing."

**Slide 7: Code Safeguards**
- Size limits (10MB uploads, 256KB thumbnails)
- Strict timeouts (10 seconds)
- No file writes (BytesIO only)
- Config-gated external calls
- Safe logging (metadata only, no PII)

**Say:**
> "We've implemented multiple safeguards in code: size limits, timeouts, no file persistence, and configuration gates that disable external calls by default."

### 5. Path to Real Implementation (2 minutes)

**Slide 8: What Would Be Required**
Before this could be used in the real world:
1. Legal review and approval
2. Partnerships with:
   - Reverse image search providers (TinEye, Google, Bing)
   - Hotlines (NCMEC, INHOPE)
   - Platform safety teams
3. Extensive testing and validation
4. Privacy impact assessment
5. Security audit
6. Professional counseling support integrated

**Say:**
> "To move from POC to real-world use would require extensive work: legal review, formal partnerships, security audits, and integration with professional support services. This is a long process—and rightly so, given the sensitive nature."

**Slide 9: TODO Items**
Show actual code TODOs:
```python
# TODO: Integrate real reverse image API after legal review
# TODO: Add partnership with authorized hotlines
# TODO: Implement rate limiting for production
# TODO: Add PhotoDNA/ProjectVIC integration (law enforcement only)
```

**Say:**
> "We've marked all integration points with TODO comments. Each represents a place where partnerships and legal agreements would be needed."

### 6. Ethical Considerations (2 minutes)

**Slide 10: Ethics First**
- Consent is paramount
- Privacy must be protected
- Avoid harm to victims
- Don't enable abuse
- Transparency about limitations

**Say:**
> "Ethics must guide every decision. We must always have explicit consent, protect privacy, avoid re-victimizing people, and be transparent about what the technology can and cannot do."

**Slide 11: Resources**
Share support resources:
- NCMEC CyberTipline: cybertipline.org
- INHOPE: inhope.org
- Revenge Porn Helpline: revengepornhelpline.org.uk
- Local law enforcement

**Say:**
> "If anyone is affected by non-consensual image distribution, these resources can help. Technology is only one piece—professional support is critical."

### 7. Q&A (2-3 minutes)

**Slide 12: Questions**

**Anticipated questions:**

Q: "Could someone misuse this?"
A: "Any technology can be misused, which is why we've built in safeguards: no scraping, no persistence, disabled external calls, and extensive documentation about what NOT to do. Real deployment would require professional oversight."

Q: "Why not integrate real APIs now?"
A: "Legal and ethical requirements first. We need partnerships, terms of service agreements, and legal review before connecting to real services."

Q: "What about accuracy?"
A: "Perceptual hashing is good but not perfect. False positives and false negatives occur. This would need extensive validation and professional review before real-world use."

Q: "What about privacy?"
A: "All processing is local. Nothing is sent to external servers except in the (disabled) search function, which would require consent and privacy review before enabling."

---

## Closing Statement

**Say:**
> "Thank you for your attention. Remember, this is a proof-of-concept to demonstrate technical feasibility with safety-first design. Real-world implementation would require extensive legal review, partnerships, and professional oversight. If you have questions, I'm happy to discuss further. And again, resources are available if anyone needs support."

---

## After the Presentation

- Share the GitHub repository link
- Point people to SAFETY_AND_LEGAL.md
- Provide hotline resources
- Be available for follow-up questions
- Do NOT provide copies of the software to anyone without ensuring they understand the safety constraints

---

## Red Flags to Watch For

If someone asks about:
- Removing safety constraints → Redirect to legal/ethical requirements
- Using for production → Emphasize "POC only" and legal review needed
- Processing real images → Stress consent requirements
- "Testing" on public sites → Clarify no scraping policy

**If someone seems to want to misuse this:**
- Politely but firmly decline to assist
- Reiterate safety and legal constraints
- Document the concern
- Report if necessary

---

## Sample Slide Deck Outline

1. Title slide
2. Content warning
3. The problem
4. Safety principles
5. What this is NOT
6. How it works (diagram)
7. Demo (live or recorded)
8. Technical architecture
9. Code safeguards
10. Path to real implementation
11. TODOs and partnerships needed
12. Ethical considerations
13. Resources and support
14. Questions

---

## Technical Setup for Demo

### Before presenting:

```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd frontend
npm run dev

# Verify both running
# Backend: http://localhost:8000
# Frontend: http://localhost:3000

# Check that allow_external_fetch=false in config
```

### Demo data prepared:
- `/backend/demo_data/consent_photos/demo_image_1.jpg`
- `/backend/demo_data/consent_photos/demo_image_2.jpg`

### Fallback plan:
If live demo fails, have:
- Screenshots of each step
- Pre-recorded video
- Slide-based walkthrough

---

## Remember

**Safety and ethics first, always.**

If you're uncertain about anything, err on the side of caution. The goal is to demonstrate responsible technology development, not to create a fully functional tool.
