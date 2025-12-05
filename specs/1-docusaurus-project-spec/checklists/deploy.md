# Deployment Guide for GitHub Pages

This guide outlines the process for deploying the Physical AI & Humanoid Robotics Textbook Docusaurus project to GitHub Pages using GitHub Actions.

## Overview

The deployment is automated via a GitHub Actions workflow defined in `.github/workflows/deploy.yml`. This workflow is triggered on every `push` to the `main` branch.

## Deployment Workflow (`.github/workflows/deploy.yml`)

The `deploy.yml` file contains the following key steps:

1.  **Checkout Code**: Clones the repository.
2.  **Setup Node.js**: Sets up Node.js (version 18.x) and caches `yarn` dependencies.
3.  **Install dependencies**: Installs the project's dependencies using `yarn install --frozen-lockfile` within the `docusaurus-project` directory.
4.  **Build Docusaurus website**: Builds the static Docusaurus site using `yarn build` within the `docusaurus-project` directory.
5.  **Deploy to GitHub Pages**: Uses `peaceiris/actions-gh-pages@v3` action to deploy the `docusaurus-project/build` directory to the `gh-pages` branch of your repository. This action automatically handles the GitHub Pages configuration.

## GitHub Pages Configuration

Ensure that your `docusaurus.config.js` file is correctly configured for GitHub Pages deployment:

-   `url`: Should be set to `https://<YOUR_GITHUB_USERNAME>.github.io` (e.g., `https://MuzzamilBukhari.github.io`).
-   `baseUrl`: Should be set to `/<YOUR_REPOSITORY_NAME>/` (e.g., `/giaicq4-hackathon-1/`). This is critical if your repository is not named after your GitHub username.
-   `organizationName`: Your GitHub username or organization name.
-   `projectName`: Your GitHub repository name.
-   `trailingSlash`: Set to `false` for consistent URLs.

### Example `docusaurus.config.js` excerpt:

```javascript
  url: 'https://MuzzamilBukhari.github.io',
  baseUrl: '/giaicq4-hackathon-1/',
  organizationName: 'MuzzamilBukhari',
  projectName: 'giaicq4-hackathon-1',
  trailingSlash: false,
```

## Manual Deployment Steps (if needed)

While automated deployment is preferred, you can manually build and deploy if necessary:

1.  **Build the project**:
    ```bash
    cd docusaurus-project
    npm run build
    ```
2.  **Deploy manually**:
    If you need to manually push to the `gh-pages` branch, you can use tools like `gh-pages` npm package or manual git commands. However, the GitHub Actions workflow is the recommended approach.

## Troubleshooting

-   **Deployment Failure**: Check the GitHub Actions workflow runs in your repository for detailed logs.
-   **Broken Links**: Ensure `baseUrl` in `docusaurus.config.js` is correct. Verify internal links in your Markdown files use the correct `/docs/your-document-id` format.
-   **GitHub Token**: The `GITHUB_TOKEN` secret is automatically provided by GitHub Actions; you typically do not need to configure it manually unless using a personal access token for more advanced scenarios.
