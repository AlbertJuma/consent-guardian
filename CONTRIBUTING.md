# Contributing to Consent Guardian

Thank you for your interest in contributing to the Consent Guardian proof-of-concept! This document provides guidelines for contributing safely and responsibly.

## ⚠️ CRITICAL: Read This First

Before contributing, you **MUST** read:

1. **[SAFETY_AND_LEGAL.md](SAFETY_AND_LEGAL.md)** - Complete safety guidelines
2. **[README.md](../README.md)** - Project overview and goals
3. This **CONTRIBUTING.md** file in full

## Code of Conduct

### Our Commitment

This project deals with sensitive topics. We are committed to:

- **Safety First**: Never compromising on safety or legal constraints
- **Respect**: Treating all contributors with respect and dignity
- **Responsibility**: Using technology ethically and legally
- **Transparency**: Being clear about limitations and risks

### Unacceptable Contributions

We will **NOT** accept contributions that:

- Remove or weaken safety constraints
- Enable web scraping or mass data collection
- Store images or sensitive data
- Bypass configuration gates for external APIs
- Add features for processing suspected illegal content
- Remove legal disclaimers or warnings
- Add real API keys or credentials
- Violate privacy, security, or ethical standards

## What We're Looking For

### Welcome Contributions

✅ **Bug Fixes**
- Fix errors that don't compromise safety
- Improve error handling
- Fix documentation typos

✅ **Safety Improvements**
- Strengthen safety constraints
- Add additional checks
- Improve logging (metadata only)
- Better error messages

✅ **Documentation**
- Clarify existing documentation
- Add examples (safe only)
- Improve installation instructions
- Translate documentation (maintaining all warnings)

✅ **Testing**
- Add unit tests
- Improve test coverage
- Add integration tests (safe data only)

✅ **Code Quality**
- Refactoring that maintains safety
- Performance improvements
- Code cleanup
- Type hints

## How to Contribute

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/consent-guardian.git
cd consent-guardian
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 3. Make Your Changes

- Follow the coding standards below
- Write or update tests
- Update documentation
- Run safety verification

### 4. Test Your Changes

```bash
# Run unit tests
cd tests
pytest test_hash.py -v

# Run safety verification
python verify_safety.py

# Test demo script
python demo_run.py

# All must pass before submitting
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"

# Use descriptive commit messages:
# Good: "Add timeout parameter to fetch_and_hash_thumbnail"
# Good: "Fix: Correct similarity calculation edge case"
# Bad: "update stuff"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Pull Request Guidelines

### PR Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass (including safety verification)
- [ ] Documentation is updated
- [ ] No sensitive data or API keys committed
- [ ] Safety constraints are maintained or strengthened
- [ ] PR description clearly explains changes
- [ ] No breaking changes (or clearly documented)

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature (safe/documentation only)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Test improvement

## Safety Impact
- [ ] No impact on safety constraints
- [ ] Strengthens safety constraints
- [ ] Requires safety review (explain why)

## Testing
- [ ] Unit tests pass
- [ ] Safety verification passes
- [ ] Demo script runs successfully
- [ ] Manual testing completed

## Checklist
- [ ] Read SAFETY_AND_LEGAL.md
- [ ] No hardcoded credentials
- [ ] No removal of safety features
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Coding Standards

### Python Code Style

- Follow **PEP 8**
- Use **type hints** where helpful
- Write **docstrings** for functions
- Keep functions focused and small
- Use meaningful variable names

```python
# Good
def compute_phash(image_bytes: bytes) -> Tuple[str, dict]:
    """
    Compute perceptual hash from image bytes.
    
    Args:
        image_bytes: Raw image data
        
    Returns:
        Tuple of (hash_string, metadata_dict)
    """
    # Implementation
    pass

# Bad
def do_stuff(x):
    pass
```

### JavaScript/React Code Style

- Follow **ESLint** configuration
- Use **functional components** with hooks
- Keep components focused
- Use meaningful prop names

```javascript
// Good
function ImageUploader({ onHashComputed, disabled }) {
  // Implementation
}

// Bad
function Comp({ fn, d }) {
  // Implementation
}
```

### Safety-Critical Code

For code that handles images, network requests, or sensitive operations:

```python
# ALWAYS include safety comments
def fetch_thumbnail(url: str) -> bytes:
    """
    SAFETY: Does NOT save to disk, processes in memory only.
    """
    # Implementation with BytesIO, timeouts, size limits
```

## Documentation Standards

### Code Comments

- Explain **why**, not what
- Document safety constraints
- Note TODOs for future work
- Reference requirements/issues

```python
# Good: Explains why
# Use BytesIO to avoid disk persistence (safety requirement)
image_stream = io.BytesIO(image_bytes)

# Bad: Obvious
# Create a BytesIO object
image_stream = io.BytesIO(image_bytes)
```

### Documentation Files

- Use **Markdown**
- Include **table of contents** for long docs
- Use **clear headings**
- Add **examples** where helpful
- Maintain **consistent formatting**

## Testing Requirements

### Unit Tests

All code changes should include tests:

```python
def test_new_feature():
    """Test description."""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = new_function(input_data)
    
    # Assert
    assert result == expected_output
```

### Test Coverage

- Aim for high test coverage
- Test edge cases
- Test error conditions
- Use safe test data only

### Safety Tests

For safety-critical code, include verification tests:

```python
def test_no_file_persistence():
    """Verify no files are created during processing."""
    # Test implementation
    pass
```

## Review Process

### What to Expect

1. **Automated Checks**: CI will run tests and linting
2. **Safety Review**: Maintainers verify safety constraints
3. **Code Review**: Review for quality and correctness
4. **Discussion**: May request changes or clarification
5. **Approval**: Merged when all requirements met

### Timeline

- Initial response: Within 1 week
- Full review: Within 2 weeks
- Complex changes may take longer

## Reporting Issues

### Bug Reports

Include:

- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Python/Node versions)
- Screenshots if applicable

**DO NOT** include:
- Sensitive data
- Real images
- API keys
- Personal information

### Feature Requests

Before requesting features:

1. Check if it aligns with project goals
2. Consider safety implications
3. Review existing issues

Template:
```markdown
## Feature Description
Brief description

## Safety Considerations
How does this maintain or improve safety?

## Use Case
Why is this needed for the demo/POC?

## Implementation Ideas
Optional technical approach
```

## Security Vulnerabilities

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email project maintainers privately
3. Allow time for fix before disclosure
4. We will credit you (if desired) after fix

## Questions?

- Check [README.md](../README.md)
- Check [SAFETY_AND_LEGAL.md](SAFETY_AND_LEGAL.md)
- Check existing issues
- Open a new issue for questions

## Recognition

Contributors will be:
- Listed in project acknowledgments
- Credited in relevant commits
- Thanked in release notes

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License with safety disclaimers).

---

## Final Reminders

✅ **Safety First**: Never compromise on safety  
✅ **Read Documentation**: Understand the project before contributing  
✅ **Test Thoroughly**: All tests must pass  
✅ **Be Respectful**: This project deals with sensitive topics  
✅ **Ask Questions**: When in doubt, ask

Thank you for helping make this project safer and better! 🙏
