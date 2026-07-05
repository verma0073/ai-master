# 🤝 Contributing to AI Master

First of all, thank you for your interest in contributing to AI Master!

AI Master is a long-term project focused on learning, building, and documenting production-grade AI Engineering practices.

Whether you're fixing a typo, improving documentation, adding a project, or contributing code, your help is appreciated.

---

# Project Philosophy

AI Master follows a documentation-first engineering approach.

Core principles include:

- Documentation before implementation
- Learn by building
- Production-grade engineering
- Small, focused Git commits
- Clean and maintainable code
- Continuous learning and improvement

---

# Getting Started

## 1. Fork the Repository

Create your own copy of the repository.

## 2. Clone Your Fork

```bash
git clone <your-fork-url>
```

## 3. Create a Branch

```bash
git checkout -b feature/my-feature
```

Use descriptive branch names.

Examples:

- feature/add-rag-project
- feature/langgraph-agent
- docs/update-roadmap
- fix/readme-links

---

# Development Guidelines

Before submitting changes, ensure that:

- Documentation is updated.
- Code is tested.
- Files follow the repository formatting rules.
- No secrets or credentials are committed.
- Meaningful commit messages are used.

---

# Coding Standards

## Python

- Follow PEP 8.
- Use type hints where appropriate.
- Keep functions small and focused.
- Write descriptive variable names.
- Prefer readability over cleverness.

---

## Documentation

Documentation should be:

- Clear
- Concise
- Technically accurate
- Beginner-friendly where appropriate

Every significant project should include:

- README
- Architecture overview
- Setup instructions
- Usage examples
- Future improvements

---

# Git Workflow

Recommended workflow:

```bash
git checkout -b feature/my-feature

git add .

git commit -m "feat: add semantic search project"

git push origin feature/my-feature
```

Then open a Pull Request.

---

# Commit Message Convention

Follow Conventional Commits where possible.

Examples:

```text
feat: add FastAPI chatbot
fix: resolve Docker build issue
docs: update architecture guide
refactor: improve prompt utilities
test: add API integration tests
chore: update dependencies
```

---

# Pull Request Guidelines

Before submitting a Pull Request:

- Ensure the project builds successfully.
- Verify documentation is updated.
- Keep changes focused on a single feature or fix.
- Describe the purpose of the change.
- Reference related issues where applicable.

---

# Reporting Issues

When opening an issue, please include:

- Description
- Expected behavior
- Actual behavior
- Steps to reproduce
- Environment details
- Relevant screenshots or logs

---

# Security

Do not commit:

- API keys
- Passwords
- Secrets
- Access tokens
- Certificates
- Sensitive datasets

Use environment variables for all secrets.

---

# AI Engineering Standards

Projects should aim to include:

- Documentation
- Architecture diagrams
- Docker support
- Tests
- Example usage
- Clear project structure

---

# Code of Conduct

Be respectful and constructive.

Provide helpful feedback.

Encourage learning and collaboration.

---

# Questions

If you have suggestions for improving AI Master, feel free to open an issue or submit a Pull Request.

Thank you for contributing!
---

# Engineering Checklist

Before marking any feature as complete, verify the following:

- [ ] Documentation updated
- [ ] Architecture reviewed
- [ ] Code follows project standards
- [ ] Environment variables documented
- [ ] Docker support added (if applicable)
- [ ] Tests added or updated
- [ ] README updated
- [ ] Interview notes captured
- [ ] Changes committed with a meaningful message
- [ ] Changes pushed to GitHub
