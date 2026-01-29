# Prettier Configuration

This directory contains shared Prettier configurations for code formatting.

## Usage

In your project's `package.json`, add:

```json
{
  "prettier": "@kei-jp/shared-config/prettier/.prettierrc.json"
}
```

Or create a `.prettierrc.json` file:

```json
"@kei-jp/shared-config/prettier/.prettierrc.json"
```

Or extend it in `.prettierrc.json`:

```json
{
  "extends": "@kei-jp/shared-config/prettier/.prettierrc.json"
}
```

## Configuration Details

- **Semi-colons**: Enabled
- **Trailing Commas**: ES5 compatible
- **Single Quotes**: Enabled
- **Print Width**: 100 characters
- **Tab Width**: 2 spaces
- **Arrow Function Parens**: Avoid when possible
- **End of Line**: LF (Unix-style)
