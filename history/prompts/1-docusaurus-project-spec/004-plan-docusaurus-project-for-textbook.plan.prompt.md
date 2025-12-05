id: 004
title: Plan Docusaurus Project for Textbook
stage: plan
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-docusaurus-project-spec
branch: 1-docusaurus-project-spec
user: user
command: /sp.plan Create: A complete architectural plan for a production-ready Docusaurus v3 documentation website that will serve as the Physical AI & Humanoid Robotics textbook. The plan must describe the site's folder structure, chapter layout, navigation strategy, file configuration requirements, and GitHub Pages deployment architecture. It must also define how placeholder chapters will be created so later module iterations can populate them.\n\nDecisions needing documentation:\n- Docusaurus initialization parameters (site name, deployment settings)\n- Project directory layout: docs/, static/, sidebars.js, docusaurus.config.js\n- Chapter hierarchy: foundational-first vs module-first sequence\n- Sidebar configuration strategy (single sidebar vs multi-section)\n- Frontmatter template used for every chapter\n- Strategy for assets: diagrams in /static vs local to docs\n- Deployment method: GitHub Actions workflow vs manual deployment\n- Repository structure and naming conventions to ensure GitHub Pages compatibility\n- Whether chapters will be single long files or separated into nested subfolders\n\nTesting strategy:\n- Validate that the generated Docusaurus project builds successfully (`npm run build`)\n- Validate sidebar navigation and routing for all placeholder chapters\n- Validate GitHub Pages deployment through CI/CD workflow (`deploy.yml`)\n- Confirm that every Markdown file follows Docusaurus frontmatter requirements\n- Confirm that the project structure supports future integrations (RAG chatbot, personalization, React components)\n- Ensure the final site renders correctly locally and after deployment\n\nTechnical details:\n- Must use `npx create-docusaurus@latest <project-name> classic` to scaffold\n- Plan structure must follow phases: Initialization → Documentation Mapping → Configuration → Deployment Setup → Validation\n- Include requirements for correct Docusaurus metadata: `url`, `baseUrl`, `organizationName`, `projectName`\n- Specify a consistent chapter template: title → objectives → sections → examples → exercises\n- Use sidebar_position to enforce deterministic navigation order\n- Define how assets will be organized for scalability\n- Ensure compatibility with GitHub Pages by enforcing trailingSlash: false and correct baseUrl
labels: [plan, docusaurus, textbook]
links:
  spec: specs/1-docusaurus-project-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/1-docusaurus-project-spec/plan.md
tests:

---

## Prompt

Create: A complete architectural plan for a production-ready Docusaurus v3 documentation website that will serve as the Physical AI & Humanoid Robotics textbook. The plan must describe the site's folder structure, chapter layout, navigation strategy, file configuration requirements, and GitHub Pages deployment architecture. It must also define how placeholder chapters will be created so later module iterations can populate them.\n\nDecisions needing documentation:\n- Docusaurus initialization parameters (site name, deployment settings)\n- Project directory layout: docs/, static/, sidebars.js, docusaurus.config.js\n- Chapter hierarchy: foundational-first vs module-first sequence\n- Sidebar configuration strategy (single sidebar vs multi-section)\n- Frontmatter template used for every chapter\n- Strategy for assets: diagrams in /static vs local to docs\n- Deployment method: GitHub Actions workflow vs manual deployment\n- Repository structure and naming conventions to ensure GitHub Pages compatibility\n- Whether chapters will be single long files or separated into nested subfolders\n\nTesting strategy:\n- Validate that the generated Docusaurus project builds successfully (`npm run build`)\n- Validate sidebar navigation and routing for all placeholder chapters\n- Validate GitHub Pages deployment through CI/CD workflow (`deploy.yml`)\n- Confirm that every Markdown file follows Docusaurus frontmatter requirements\n- Confirm that the project structure supports future integrations (RAG chatbot, personalization, React components)\n- Ensure the final site renders correctly locally and after deployment\n\nTechnical details:\n- Must use `npx create-docusaurus@latest <project-name> classic` to scaffold\n- Plan structure must follow phases: Initialization → Documentation Mapping → Configuration → Deployment Setup → Validation\n- Include requirements for correct Docusaurus metadata: `url`, `baseUrl`, `organizationName`, `projectName`\n- Specify a consistent chapter template: title → objectives → sections → examples → exercises\n- Use sidebar_position to enforce deterministic navigation order\n- Define how assets will be organized for scalability\n- Ensure compatibility with GitHub Pages by enforcing trailingSlash: false and correct baseUrl

## Response snapshot

I have successfully created the `plan.md` file in `specs/1-docusaurus-project-spec/plan.md`. This plan outlines the architectural design for a production-ready Docusaurus documentation website for the Physical AI & Humanoid Robotics textbook. It covers the site's folder structure, chapter layout, navigation strategy, file configuration requirements, and GitHub Pages deployment architecture. Key decisions regarding Docusaurus initialization, chapter hierarchy (foundational-first), sidebar configuration, frontmatter templates, asset strategy (centralized in `/static`), and GitHub Actions deployment have been documented. The plan is structured into Initialization, Documentation Mapping, Configuration, Deployment Setup, and Validation phases.

## Outcome

- ✅ Impact: Architectural plan for Docusaurus project successfully created and aligned with spec and constitution.
- 🧪 Tests: Manual review conducted against spec and constitution; all checks passed.
- 📁 Files: One file created: specs/1-docusaurus-project-spec/plan.md
- 🔁 Next prompts: User can proceed with task generation (`/sp.tasks`).
- 🧠 Reflection: Automated script for prerequisite check failed, so manual verification was performed instead.

## Evaluation notes (flywheel)

- Failure modes observed: `pwsh` not found for `check-prerequisites.ps1`.
- Graders run and results (PASS/FAIL): N/A (manual verification).
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Address `pwsh` dependency or provide bash alternatives for system checks.