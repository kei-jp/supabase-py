# TypeScript Configurations

This directory contains shared TypeScript configurations for different project types.

## Available Configurations

### Base Configuration (`tsconfig.json`)
Standard TypeScript configuration for Node.js projects.

**Usage:**
```json
{
  "extends": "@kei-jp/shared-config/typescript/tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### React Configuration (`tsconfig.react.json`)
Configuration optimized for React projects with modern bundlers (Vite, etc.).

**Usage:**
```json
{
  "extends": "@kei-jp/shared-config/typescript/tsconfig.react.json",
  "compilerOptions": {
    "baseUrl": "./src"
  }
}
```

## Key Features

- **Strict mode enabled** for better type safety
- **ES2020 target** for modern JavaScript features
- **Source maps and declarations** enabled
- **JSON imports** supported
- **Consistent casing** enforced
