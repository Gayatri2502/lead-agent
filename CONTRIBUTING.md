# Contributing to AI Voice Receptionist

Thank you for your interest in contributing to the AI Voice Receptionist project!

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone your-fork-url`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Follow the setup in [GETTING_STARTED.md](GETTING_STARTED.md)

## Development Workflow

### Backend Development

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

### Code Style

**Python**:
- Follow PEP 8
- Use type hints
- Run: `black app/` and `flake8 app/`

**TypeScript/React**:
- Use ESLint: `npm run lint`
- Use Prettier: `npm run format`
- Follow component naming conventions

## Commit Messages

Format: `type(scope): description`

Examples:
- `feat(appointments): add bulk appointment creation`
- `fix(auth): resolve token refresh issue`
- `docs(api): update endpoint documentation`
- `refactor(database): optimize query performance`

Types: feat, fix, docs, refactor, test, chore, style

## Pull Requests

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass: `npm run test` and `pytest tests/`
4. Submit PR with clear description
5. Link related issues

## Reporting Bugs

Create an issue with:
- Description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, versions)
- Logs/error messages

## Feature Requests

Provide:
- Clear use case
- Expected behavior
- Potential implementation approach
- Why it's valuable

## Documentation

- Keep README.md up to date
- Document new API endpoints
- Add comments for complex logic
- Update relevant docs in `/docs`

## Version Control

- Rebase before submitting PR: `git rebase main`
- Keep commits atomic and logical
- Use meaningful branch names

## Questions?

- Check existing documentation in `/docs`
- Search existing issues
- Create a discussion or ask in a new issue

Thank you for contributing! 🎉
