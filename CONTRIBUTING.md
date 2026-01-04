# Contributing to SYNAPSE

## How to Contribute

We welcome contributions! SYNAPSE is an open-source project and we appreciate any help.

## Reporting Bugs

1. Check existing issues on GitHub
2. Create new issue with descriptive title
3. Use the bug report template (if available)
4. Include:
   - Version: SYNAPSE version
   - OS: Operating system and version
   - Steps to reproduce: Detailed steps
   - Expected behavior: What should happen
   - Actual behavior: What actually happened
   - Logs: Relevant error logs

## Suggesting Enhancements

1. Check existing issues for "enhancement" label
2. Open new issue with "enhancement" label
3. Describe:
   - Use case: When and how you would use this feature
   - Benefits: Why this feature would be valuable
   - Implementation ideas (optional): If you have thoughts on how to implement

## Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Write tests for new functionality
5. Ensure all tests pass: `pytest`
6. Update CHANGELOG.md with your changes
7. Commit your changes with clear message
8. Push to your fork: `git push origin feature/my-feature`
9. Open a Pull Request on GitHub

## Development Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Docker (for container testing)
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/kayis-rahman/synapse.git
cd synapse

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
black synapse/
mypy synapse/
```

## Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints for all public functions
- Write docstrings for all public functions
- Maximum line length: 88 characters (black default)
- Use meaningful variable names

### Documentation

- Update README.md for user-facing changes
- Update CHANGELOG.md for version history
- Add docstrings to new functions

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring without functional changes
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks (build, CI, etc.)

Example:
```
feat: add support for custom chunk sizes

Fixes issue #123 where users couldn't adjust chunk size in configuration.

Adds new configuration option `custom_chunk_size` with validation.

Related: #120, #122
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run with coverage
pytest --cov=synapse --cov-report=term

# Run specific test
pytest -k "test_data_dir"
```

### Writing Tests

Place tests in the `tests/` directory with the following structure:

```
tests/
├── conftest.py           # Shared fixtures
├── test_config.py       # Configuration tests
├── test_memory_store.py  # Memory store tests
├── test_episodic_store.py # Episodic memory tests
└── test_semantic_store.py # Semantic memory tests
```

Example test:

```python
import pytest
from synapse.rag import MemoryStore

def test_store_memory_fact():
    """Test storing a symbolic memory fact"""
    store = MemoryStore(":memory:")
    
    fact = store.store_memory(
        MemoryFact(
            scope="test",
            category="test",
            key="test_key",
            value="test_value",
            confidence=1.0,
            source="test"
        )
    )
    
    assert fact.id is not None
    assert fact.value == "test_value"

def test_retrieve_memory_fact():
    """Test retrieving a symbolic memory fact"""
    store = MemoryStore(":memory:")
    
    # Store a fact first
    store.store_memory(
        MemoryFact(
            scope="test",
            category="test",
            key="test_key",
            value="test_value",
            confidence=1.0,
            source="test"
        )
    )
    
    # Retrieve it
    facts = store.query_memory(scope="test", key="test_key")
    
    assert len(facts) == 1
    assert facts[0].value == "test_value"
```

## Code Review

1. Be respectful and constructive
2. Point out issues with code, not people
3. Suggest improvements
4. Ask questions when something is unclear

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Questions?

Feel free to open an issue on GitHub for questions about:
- Architecture decisions
- Implementation approaches
- Feature requests
- Bug reports
