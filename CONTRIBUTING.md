# Contributing to Suno Music Player

Thank you for your interest in contributing! This document provides guidelines and instructions.

## Code of Conduct

- Be respectful and inclusive
- Constructive feedback only
- No harassment or discrimination

## Getting Started

### 1. Fork & Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/yourusername/suno-music-player.git
cd suno-music-player
git remote add upstream https://github.com/original-owner/suno-music-player.git
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Development Dependencies

```bash
pip install -r requirements.txt
pip install pylint black pytest
```

## Development Workflow

### Making Changes

1. **Create a branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make changes:**
   - Write clean, readable code
   - Add comments for complex logic
   - Follow PEP 8 style guide

3. **Test locally:**
```bash
python main.py
```

4. **Lint your code:**
```bash
pylint *.py
black *.py
```

### Committing

Use clear, descriptive commit messages:

```bash
git add .
git commit -m "Add: feature description"
# or
git commit -m "Fix: bug description"
git commit -m "Refactor: code improvement"
```

### Pushing & Pull Request

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub with:
- Clear title
- Description of changes
- Why this change is needed
- Any related issues (#123)

## Code Style

### Python

```python
# Follow PEP 8
# Good
def get_user_data(user_id: int) -> Dict:
    """Fetch user data from API."""
    
# Bad
def getUserData(userId):
    # fetch user data from API

# Use type hints
def download_file(url: str, path: Path) -> bool:
    ...

# Docstrings
def authenticate(token: str) -> bool:
    """
    Authenticate with Suno API.
    
    Args:
        token: JWT authentication token
        
    Returns:
        True if authentication successful, False otherwise
    """
```

### Comments

- Use `#` for short inline comments
- Use docstrings for functions/classes
- Explain *why*, not *what*

```python
# Good
# Wait for user to complete login (API requires this)
time.sleep(5)

# Bad
# Sleep for 5 seconds
time.sleep(5)
```

## Feature Development

### Before Starting

1. **Check existing issues** - Avoid duplicates
2. **Start a discussion** - For large features
3. **Assign yourself** - Comment "I'll work on this"

### Feature Ideas

Popular suggestions:
- [ ] Playlist management
- [ ] Search/filter functionality  
- [ ] Batch downloads
- [ ] Keyboard shortcuts
- [ ] Dark mode theme
- [ ] Equalizer
- [ ] Shuffle/repeat modes
- [ ] Better progress indication

### Implementation Tips

- Keep changes focused and small
- One feature per PR
- Update README if needed
- Add comments for non-obvious code

## Bug Reports

### Reporting Issues

Include:

```markdown
**Description**
[What's the problem?]

**Steps to Reproduce**
1. ...
2. ...
3. ...

**Expected Behavior**
[What should happen?]

**Actual Behavior**
[What actually happened?]

**Environment**
- OS: Windows/macOS/Linux
- Python: 3.9/3.10/3.11
- App Version: 1.0.0

**Error Message**
[Paste any error messages/stack traces]

**Screenshots**
[If applicable]
```

## Testing

When adding features:

```python
# Test the feature works
python main.py

# Test error handling
# (e.g., try invalid token, no internet, etc.)

# Test UI responsiveness
# (app shouldn't freeze)
```

## Documentation

If you change:
- API usage → Update `api.py` docstrings
- Authentication flow → Update auth section in README
- UI elements → Update screenshots if major change
- Command line usage → Update README

## Pull Request Review

Expect feedback on:
- Code style & readability
- Performance implications
- Error handling
- Documentation
- Testing

It's normal to need revisions - all code goes through review!

## Merge Process

Your PR will be merged when:
- ✓ Code reviewed & approved
- ✓ All tests pass
- ✓ No conflicts with main branch
- ✓ Documentation updated

## Questions?

- **GitHub Issues** - For bugs/features
- **Discussions** - For questions
- **Email** - your.email@example.com

## Recognition

Contributors are recognized in:
- README.md acknowledgments
- Release notes
- GitHub contributors graph

---

**Thank you for helping make Suno Music Player better!** 🎵
