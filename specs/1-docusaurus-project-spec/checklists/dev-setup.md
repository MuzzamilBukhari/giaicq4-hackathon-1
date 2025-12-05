# Developer Setup Guide

This guide outlines the steps to set up your local development environment for the Physical AI & Humanoid Robotics Textbook Docusaurus project.

## Prerequisites

Ensure you have the following installed:

-   **Node.js**: Version 18 or higher.
-   **npm** (Node Package Manager): Usually comes with Node.js.

## Project Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/MuzzamilBukhari/giaicq4-hackathon-1.git
    cd giaicq4-hackathon-1/docusaurus-project
    ```
2.  **Install dependencies**:
    Navigate to the `docusaurus-project` directory and install the required Node.js packages.
    ```bash
    npm install
    ```

## Running the Development Server

To start the local development server and view the textbook:

```bash
npm start
```

This will open the site in your browser at `http://localhost:3000`. The site will hot-reload as you make changes.

## Building the Project

To build the static production files for the project:

```bash
npm run build
```

The static files will be generated in the `build/` directory.

## Cleaning the Build Output

To remove the `build/` directory and other temporary files:

```bash
npm run clear
```
