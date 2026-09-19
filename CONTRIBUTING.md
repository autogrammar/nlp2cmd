# Contributing to NLP2CMD

## 📚 Related Documentation

- **[Installation Guide](INSTALLATION.md)** - Setup instructions
- **[User Guide](docs/guides/user-guide.md)** - Usage tutorial
- **[API Reference](docs/api/README.md)** - API documentation
- **[Examples](examples/)** - Code examples and use cases

Thank you for your interest in contributing to NLP2CMD! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We welcome contributors of all experience levels.

## Getting Started

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/wronai/nlp2cmd.git
cd nlp2cmd
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nlp2cmd --cov-report=html

# Run specific test file
pytest tests/unit/test_adapters.py

# Run tests matching pattern
pytest -k "test_sql"
```

### Code Style

We use the following tools for code quality:

- **Black** for formatting
- **Ruff** for linting
- **MyPy** for type checking

```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Type check
mypy src
```

## How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/wronai/nlp2cmd/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Relevant code snippets

### Suggesting Features

1. Check existing [Feature Requests](https://github.com/wronai/nlp2cmd/labels/enhancement)
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Proposed API (if applicable)

### Pull Requests

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/my-feature
```

3. Make your changes following our coding standards
4. Add tests for new functionality
5. Update documentation if needed
6. Run tests and linting:
```bash
pytest
black src tests
ruff check src tests
mypy src
```

7. Commit with a descriptive message:
```bash
git commit -m "feat: add Redis adapter support"
```

8. Push and create a Pull Request

### Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `style:` formatting, no code change
- `refactor:` code restructuring
- `test:` adding tests
- `chore:` maintenance tasks

Examples:
```
feat: add Terraform adapter
fix: handle null values in SQL generation
docs: update API reference for Docker adapter
test: add unit tests for feedback loop
```

## Adding a New DSL Adapter

1. Create a new file in `src/nlp2cmd/adapters/`:

```python
# src/nlp2cmd/adapters/mydsL.py
from nlp2cmd.adapters.base import BaseDSLAdapter, SafetyPolicy

class MyDSLSafetyPolicy(SafetyPolicy):
    # Define safety options
    pass

class MyDSLAdapter(BaseDSLAdapter):
    DSL_NAME = "mydsl"
    
    INTENTS = {
        "action1": {"patterns": [...], "required_entities": [...]},
    }
    
    def generate(self, plan: dict) -> str:
        # Implement command generation
        pass
    
    def validate_syntax(self, command: str) -> dict:
        # Implement syntax validation
        pass
```

2. Add to `__init__.py`:
```python
from nlp2cmd.adapters.mydsl import MyDSLAdapter, MyDSLSafetyPolicy
```

3. Add tests in `tests/unit/test_adapters.py`

4. Add documentation in `docs/api/README.md`

5. Add example in `examples/mydsl/`

## Adding a New File Schema

1. Add to `src/nlp2cmd/schemas/__init__.py`:

```python
self.schemas["myformat"] = FileFormatSchema(
    name="My Format",
    extensions=["*.myf"],
    mime_types=["application/x-myformat"],
    validator=self._validate_myformat,
    parser=self._parse_myformat,
    generator=self._generate_myformat,
    repair_rules=[...],
)
```

2. Implement validator, parser, and generator methods

3. Add tests

## Documentation

- Update docstrings for all public APIs
- Update user guide for new features
- Update API reference for new classes/methods
- Add examples for common use cases

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a release tag
4. CI will publish to PyPI

## Questions?

- Create a [Discussion](https://github.com/wronai/nlp2cmd/discussions)
- Ask in the issue tracker
- Contact maintainers

Thank you for contributing! 🎉


```dsl
DOCUMENT contributing
VERSION 1
MODE STRICT
```
