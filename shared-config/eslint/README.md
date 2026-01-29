# ESLint Configurations

This directory contains shared ESLint configurations for different project types.

## Available Configurations

### Base Configuration (`.eslintrc.json`)
Basic ESLint rules for JavaScript projects.

**Usage:**
```json
{
  "extends": ["@kei-jp/shared-config/eslint/.eslintrc.json"]
}
```

### TypeScript Configuration (`.eslintrc.typescript.json`)
Extended configuration for TypeScript projects.

**Usage:**
```json
{
  "extends": ["@kei-jp/shared-config/eslint/.eslintrc.typescript.json"]
}
```

### React Configuration (`.eslintrc.react.json`)
Configuration for React projects (works with both JavaScript and TypeScript).

**Usage:**
```json
{
  "extends": ["@kei-jp/shared-config/eslint/.eslintrc.react.json"]
}
```
