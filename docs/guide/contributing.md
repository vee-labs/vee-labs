# Contributing to Vee Labs

Thank you for your interest in contributing to Vee Labs! We welcome contributions from everyone.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** and commit them
5. **Push to your fork** and submit a pull request

## Development Setup

\`\`\`bash
# Clone the repository
git clone https://github.com/vee-labs/vee-labs.git
cd vee-labs

# Install dependencies
npm install

# Create a feature branch
git checkout -b feature/your-feature-name

# Run tests
npm test

# Run linter
npm run lint
\`\`\`

## Code Guidelines

- **Code Style**: Follow ESLint configuration
- **Testing**: Write tests for new features
- **Commits**: Use clear, descriptive commit messages
- **Documentation**: Update docs for API changes

### Commit Message Format

\`\`\`
<type>(<scope>): <subject>

<body>

<footer>
\`\`\`

Types: \`feat\`, \`fix\`, \`docs\`, \`style\`, \`refactor\`, \`test\`, \`chore\`

## Pull Request Process

1. Update README.md with any new features
2. Update documentation in the \`docs/\` directory
3. Add tests for new functionality
4. Ensure all tests pass: \`npm test\`
5. Ensure linting passes: \`npm run lint\`
6. Submit your PR with a clear description

## Testing

\`\`\`bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
\`\`\`

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Questions?

Feel free to:
- Open an issue for bugs and feature requests
- Start a discussion for general questions
- Check existing issues and discussions first

## License

By contributing to Vee Labs, you agree that your contributions will be licensed under the MIT License.