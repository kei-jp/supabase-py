# shared-config

コーディング規則や共通actionsの管理リポジトリ

Repository for managing coding conventions and common GitHub Actions workflows.

## Overview

This repository provides shared configurations for:

- **ESLint**: Linting rules for JavaScript/TypeScript/React projects
- **Prettier**: Code formatting standards
- **TypeScript**: TypeScript compiler configurations
- **GitHub Actions**: Reusable CI/CD workflows

## Installation

```bash
npm install --save-dev @kei-jp/shared-config
```

## Usage

### ESLint

For a basic JavaScript project:

```json
// .eslintrc.json
{
  "extends": ["@kei-jp/shared-config/eslint/.eslintrc.json"]
}
```

For TypeScript projects:

```json
// .eslintrc.json
{
  "extends": ["@kei-jp/shared-config/eslint/.eslintrc.typescript.json"]
}
```

For React projects:

```json
// .eslintrc.json
{
  "extends": ["@kei-jp/shared-config/eslint/.eslintrc.react.json"]
}
```

### Prettier

In `package.json`:

```json
{
  "prettier": "@kei-jp/shared-config/prettier/.prettierrc.json"
}
```

Or in `.prettierrc.json`:

```json
"@kei-jp/shared-config/prettier/.prettierrc.json"
```

### TypeScript

For Node.js projects:

```json
// tsconfig.json
{
  "extends": "@kei-jp/shared-config/typescript/tsconfig.json"
}
```

For React projects:

```json
// tsconfig.json
{
  "extends": "@kei-jp/shared-config/typescript/tsconfig.react.json"
}
```

### GitHub Actions

The repository includes example GitHub Actions workflows in `.github/workflows/examples/`. To use them:

```bash
# Clone this repository
git clone https://github.com/kei-jp/shared-config.git

# Copy desired workflows to your project
cp shared-config/.github/workflows/examples/ci.example.yml .github/workflows/ci.yml
cp shared-config/.github/workflows/examples/release.example.yml .github/workflows/release.yml

# Customize for your project
```

Or download directly from GitHub by browsing to the workflow file and clicking "Raw".

## Directory Structure

```
shared-config/
├── eslint/               # ESLint configurations
│   ├── .eslintrc.json
│   ├── .eslintrc.typescript.json
│   ├── .eslintrc.react.json
│   └── README.md
├── prettier/             # Prettier configurations
│   ├── .prettierrc.json
│   └── README.md
├── typescript/           # TypeScript configurations
│   ├── tsconfig.json
│   ├── tsconfig.react.json
│   └── README.md
├── .github/
│   ├── README.md
│   └── workflows/        # Example GitHub Actions workflows
│       └── examples/
│           ├── ci.example.yml
│           ├── release.example.yml
│           └── dependabot-auto-merge.example.yml
├── .editorconfig         # Editor configuration
├── .gitignore
├── package.json
└── README.md
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT
