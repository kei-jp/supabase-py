# GitHub Actions Workflows

This directory contains example GitHub Actions workflows for common CI/CD tasks.

## Available Example Workflows

All example workflows are located in the `workflows/examples/` directory.

### CI Workflow (`examples/ci.example.yml`)
Continuous Integration workflow that runs linting, testing, and building.

**Features:**
- ESLint code linting
- Prettier formatting check
- Unit tests with coverage reporting
- Build verification
- Artifact upload

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### Release Workflow (`examples/release.example.yml`)
Automated release workflow for creating GitHub releases and publishing to NPM.

**Features:**
- Automatic changelog generation
- GitHub Release creation
- NPM package publishing
- Semantic versioning support

**Triggers:**
- Push tags matching `v*.*.*` (e.g., v1.0.0)

### Dependabot Auto-Merge (`examples/dependabot-auto-merge.example.yml`)
Automatically approves and merges Dependabot PRs for patch and minor updates.

**Features:**
- Auto-approval of Dependabot PRs
- Auto-merge for patch and minor version updates
- Requires status checks to pass

**Triggers:**
- Pull requests from Dependabot

## Usage in Your Project

To use these workflows in your project:

1. **Copy the example workflow files** from this repository directly (not from npm):

```bash
# Clone or download this repository
git clone https://github.com/kei-jp/shared-config.git

# Copy workflows to your project
cp shared-config/.github/workflows/examples/ci.example.yml .github/workflows/ci.yml
cp shared-config/.github/workflows/examples/release.example.yml .github/workflows/release.yml
cp shared-config/.github/workflows/examples/dependabot-auto-merge.example.yml .github/workflows/dependabot.yml
```

2. **Or download directly from GitHub**:
   - Browse to the workflow file you want on GitHub
   - Click "Raw" button
   - Save the file to your project's `.github/workflows/` directory

3. **Rename them** by removing the `.example` suffix
4. **Customize them** to match your project's needs

### Customization Tips

- Adjust the npm scripts referenced in the workflows to match your project
- Modify branch names if you use different naming conventions
- Add or remove jobs based on your project's requirements
- Configure required secrets for release workflows

## Required Secrets

For the Release workflow to publish to NPM, add these secrets to your repository:

- `NPM_TOKEN`: Your NPM authentication token

## Permissions

Some workflows require specific permissions:

- **Release workflow**: `contents: write`
- **Dependabot auto-merge**: `contents: write`, `pull-requests: write`
