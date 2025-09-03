# Contributing to CLI Bookmark Manager

Thank you for your interest in contributing to CLI Bookmark Manager! This document provides guidelines and instructions for contributors.

## 🤝 How to Contribute

### Reporting Bugs

- Use the [GitHub Issues](https://github.com/ersinkoc/bookmark-manager/issues) page to report bugs
- Use the bug report template and provide as much detail as possible
- Include steps to reproduce the issue
- Mention your operating system and Python version

### Suggesting Features

- Use the [GitHub Issues](https://github.com/ersinkoc/bookmark-manager/issues) page to suggest features
- Use the feature request template
- Explain the use case and how the feature would help users

### Submitting Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/ersinkoc/bookmark-manager.git
   cd bookmark-manager
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make Your Changes**
   - Follow the coding standards below
   - Add tests for new functionality
   - Update documentation if needed

4. **Commit Your Changes**
   ```bash
   git commit -m "Add some amazing feature"
   ```

5. **Push to the Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Use the pull request template
   - Link to any related issues
   - Describe your changes clearly

## 📋 Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use type hints where appropriate
- Write docstrings for all public functions and classes

### Required Tools

Install development dependencies:
```bash
pip install black flake8 mypy pytest pytest-cov
```

### Code Formatting

Format your code with Black:
```bash
black bookmark_manager/
```

### Linting

Check for issues with Flake8:
```bash
flake8 bookmark_manager/
```

### Type Checking

Check types with MyPy:
```bash
mypy bookmark_manager/
```

### Testing

Run tests with pytest:
```bash
pytest bookmark_manager/test_bookmark_manager.py -v
```

Run tests with coverage:
```bash
pytest --cov=bookmark_manager bookmark_manager/test_bookmark_manager.py
```

## 🧪 Testing Guidelines

### Writing Tests

- Write unit tests for all new features
- Test both success and error cases
- Use descriptive test names
- Mock external dependencies (HTTP requests, file I/O)

### Test Coverage

- Aim for at least 80% test coverage
- All critical paths must be tested
- Add tests for bug fixes

### Running Tests

Before submitting a pull request, ensure all tests pass:
```bash
pytest bookmark_manager/test_bookmark_manager.py
python bookmark_manager/test_windows.py  # Windows compatibility tests
```

## 📝 Documentation

### Updating Documentation

- Update README.md for user-facing changes
- Update docstrings for API changes
- Add comments for complex logic
- Update CHANGELOG.md for significant changes

### Examples

- Provide clear examples in the README
- Include usage examples for new features
- Update command reference if needed

## 🔀 Git Workflow

### Commit Messages

Use the following format for commit messages:
```
type(scope): description

# Example:
feat(search): add regex search support
fix(windows): handle long file paths
docs(readme): update installation instructions
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

### Branch Naming

Use descriptive branch names:
- `feature/feature-name`
- `bugfix/issue-description`
- `docs/documentation-update`
- `test/add-tests-for-feature`

## 🏷️ Issue Templates

### Bug Report Template

```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
A clear and concise description of what you expected to happen.

## Actual Behavior
A clear and concise description of what actually happened.

## Environment
- OS: [e.g. Windows 10, Ubuntu 20.04]
- Python Version: [e.g. 3.9.0]
- Bookmark Manager Version: [e.g. 1.0.0]

## Additional Context
Add any other context about the problem here.
```

### Feature Request Template

```markdown
## Feature Description
A clear and concise description of the feature you'd like to see.

## Use Case
Describe the use case for this feature. How would it help users?

## Proposed Solution
If you have ideas on how to implement this feature, please describe them.

## Alternatives
Describe any alternative solutions or features you've considered.

## Additional Context
Add any other context or screenshots about the feature request here.
```

## 🎯 Release Process

### Versioning

This project follows [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` format
- Increment MAJOR for incompatible changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version is updated in `__init__.py`
- [ ] Create a Git tag
- [ ] Create a GitHub release
- [ ] Update PyPI package

## 📞 Getting Help

If you need help with contributing:

1. Check the [documentation](README.md)
2. Search existing [issues](https://github.com/ersinkoc/bookmark-manager/issues)
3. Join [GitHub Discussions](https://github.com/ersinkoc/bookmark-manager/discussions)
4. Create a new issue with the "question" label

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub repository contributors list

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to CLI Bookmark Manager! 🎉