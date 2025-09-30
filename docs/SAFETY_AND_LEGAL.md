# Safety and Legal Guidelines

## ⚠️ CRITICAL SAFETY NOTICE

**This is a PROOF-OF-CONCEPT DEMONSTRATION ONLY.**

This software is NOT intended for production use or for handling actual cases of non-consensual image distribution. It is designed solely for educational purposes and to demonstrate technical concepts.

---

## Legal Disclaimer

**READ THIS CAREFULLY BEFORE USING THIS SOFTWARE**

1. **NO WARRANTY**: This software is provided "AS IS" without warranty of any kind. The authors and contributors assume NO liability for any misuse or consequences arising from use of this software.

2. **NOT LEGAL ADVICE**: Nothing in this software or documentation constitutes legal advice. Consult qualified legal counsel for any legal matters.

3. **USER RESPONSIBILITY**: Users are solely responsible for ensuring their use complies with all applicable laws, regulations, and ethical standards.

4. **NO GUARANTEES**: This software makes no guarantees about accuracy, reliability, or fitness for any particular purpose.

---

## Prohibited Uses

### ❌ DO NOT USE THIS SOFTWARE FOR:

1. **Processing Suspected Child Sexual Abuse Material (CSAM)**
   - IMMEDIATELY report to authorities and hotlines
   - NCMEC CyberTipline: https://www.cybertipline.org
   - INHOPE Network: https://www.inhope.org
   - Local law enforcement

2. **Web Scraping or Mass Data Collection**
   - This tool does NOT scrape websites
   - It does NOT collect or store images
   - It does NOT perform mass searches

3. **Processing Images Without Consent**
   - ONLY use images where you have explicit written consent
   - Demo images must be synthetic/non-identifying

4. **Production or Commercial Use**
   - This is a POC/demo only
   - Not suitable for production environments
   - Requires extensive legal review before any real-world use

5. **Violating Privacy or Terms of Service**
   - Respect all website terms of service
   - Respect privacy laws (GDPR, CCPA, etc.)
   - Do not bypass access controls

---

## Required Safety Constraints

### ✅ This software MUST:

1. **Run Locally Only**
   - All processing happens on local machine
   - No cloud storage or external persistence
   - In-memory processing only

2. **No Image Persistence**
   - Images are never saved to disk
   - Processed in memory and immediately released
   - Thumbnails fetched in memory only

3. **Mock APIs by Default**
   - Reverse image search returns MOCK results
   - Real APIs disabled by default (`allow_external_fetch=false`)
   - Requires explicit configuration to enable

4. **Strict Fetch Limits**
   - Maximum 256 KB per thumbnail
   - Timeouts enforced (10 seconds default)
   - No redirects to other domains
   - User-agent identifies project

5. **Safe Logging Only**
   - Log URLs, timestamps, similarity scores
   - NEVER log IP addresses
   - NEVER log image bytes or personal data
   - NEVER log sensitive content

---

## Checklist Before Enabling Real Features

### Before enabling `allow_external_fetch=true`:

- [ ] Legal review completed by qualified counsel
- [ ] Partnership agreements signed with API providers
- [ ] API keys obtained through legitimate channels
- [ ] Rate limiting properly configured
- [ ] Terms of service compliance verified
- [ ] Privacy policy updated
- [ ] Data protection impact assessment (DPIA) completed
- [ ] Incident response plan in place
- [ ] Staff training completed
- [ ] Regular audits scheduled

### Before enabling `escalate_to_hotline=true`:

- [ ] Partnership with authorized hotline established
- [ ] Contact endpoints verified and tested
- [ ] Escalation procedures documented
- [ ] Staff training on handling sensitive reports
- [ ] Legal obligations understood (mandatory reporting, etc.)
- [ ] Secure communication channels established

---

## Demo and Presentation Guidelines

### ✅ Safe Demo Practices:

1. **Use Only Synthetic Images**
   - Use images from `/demo_data/consent_photos/`
   - These are safe, geometric patterns
   - No real people, no sensitive content

2. **Clearly Label as Demo**
   - Always state "This is a demonstration"
   - Emphasize mock results
   - Explain limitations

3. **Control the Environment**
   - Run on local machine only
   - Don't connect to real APIs during demo
   - Use prepared slides and scripts

4. **Audience Considerations**
   - Be sensitive to audience (some may be survivors)
   - Provide content warnings
   - Have resources ready (hotlines, support)

### ❌ DO NOT in Demos:

- Show real images of people
- Demonstrate with actual sensitive content
- Pretend this is production-ready
- Make unrealistic claims about capabilities

---

## Escalation Procedures

### If You Encounter Suspected CSAM:

1. **STOP IMMEDIATELY** - Do not view, download, or process
2. **DO NOT INVESTIGATE** - Leave it to professionals
3. **REPORT TO AUTHORITIES**:
   - NCMEC CyberTipline: https://www.cybertipline.org
   - FBI: https://www.fbi.gov/tips
   - Your local law enforcement
4. **DOCUMENT** (without saving images):
   - URL only
   - Timestamp
   - Any metadata (NO images)

### If You Encounter Non-Consensual Content:

1. **Document** (metadata only, no images)
2. **Contact appropriate resources**:
   - NCMEC (for minors)
   - INHOPE hotlines
   - Platform abuse teams
   - Law enforcement if illegal
3. **Support the victim** (if you are assisting someone)
4. **Do NOT share or distribute** the content further

---

## Contact Information for Hotlines

### United States:
- **NCMEC CyberTipline**: https://www.cybertipline.org | 1-800-843-5678
- **FBI IC3**: https://www.ic3.gov
- **Revenge Porn Helpline**: https://revengepornhelpline.org.uk (UK but has US resources)

### International:
- **INHOPE Network**: https://www.inhope.org (global hotline network)
- **IWF (UK)**: https://www.iwf.org.uk
- **Childline International**: https://www.childhelplineinternational.org

### Platform-Specific:
- Each platform has abuse reporting mechanisms
- Contact legal/safety teams directly for non-public content

---

## Technical Safeguards Implemented

### 1. No Persistence
- Images processed in `BytesIO` (memory only)
- No `open()` calls with write mode
- Immediate garbage collection

### 2. Size Limits
- Upload max: 10 MB
- Thumbnail fetch max: 256 KB
- Result limits: 20 candidates max

### 3. Timeouts
- API calls: 10 seconds default
- Fetch operations: strict timeout
- No infinite loops

### 4. Access Controls
- Config file required for external fetch
- Default: all external operations disabled
- Explicit opt-in required

### 5. Audit Trail
- All operations logged (safe metadata only)
- Timestamps on all actions
- No PII in logs

---

## Partner Integration Requirements

### Before Integrating Real APIs:

1. **Legal Documentation**:
   - Terms of Service review
   - Privacy Policy alignment
   - Data Processing Agreement (DPA)
   - Service Level Agreement (SLA)

2. **Technical Requirements**:
   - API key management (secure storage)
   - Rate limiting implementation
   - Error handling and retry logic
   - Monitoring and alerting

3. **Security Requirements**:
   - Encrypted communications (HTTPS/TLS)
   - Secure credential storage
   - Regular security audits
   - Penetration testing

4. **Operational Requirements**:
   - On-call rotation for incidents
   - Regular backups (metadata only)
   - Disaster recovery plan
   - Business continuity plan

---

## Code Review Checklist

Before deploying any changes:

- [ ] No image files saved to disk
- [ ] All external calls have timeouts
- [ ] Size limits enforced
- [ ] Error handling covers edge cases
- [ ] Logging contains no PII
- [ ] Config defaults are safe (disabled)
- [ ] Tests cover safety constraints
- [ ] Documentation updated
- [ ] Security review completed
- [ ] Legal review completed

---

## Educational Use Only

This project is intended to:

1. **Demonstrate Technical Concepts**:
   - Perceptual hashing algorithms
   - Image similarity comparison
   - API design patterns

2. **Raise Awareness**:
   - Non-consensual image distribution issues
   - Technical approaches to detection
   - Importance of legal/ethical considerations

3. **Foster Discussion**:
   - Ethical AI development
   - Privacy-preserving technologies
   - Victim support mechanisms

This project is NOT:
- A complete solution
- Production-ready software
- A substitute for professional services
- Legal or counseling advice

---

## Version History

- **v1.0.0** (2024): Initial POC release - Demo only, all external features disabled

---

## Contact for Questions

For questions about this project:
- Open a GitHub issue (for technical questions only)
- Do NOT share sensitive content in issues
- For safety/legal concerns, contact appropriate authorities first

---

**Remember: When in doubt, prioritize safety over functionality. If something seems wrong, STOP and seek guidance.**
