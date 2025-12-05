id: 003
title: Specify Docusaurus Project for Textbook
stage: spec
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 1-docusaurus-project-spec
branch: 1-docusaurus-project-spec
user: user
command: /sp.specify Physical AI & Humanoid Robotics Textbook — Full Docusaurus Project Specification\n\nTarget audience: Beginner-to-intermediate students learning robotics, simulation, and embodied AI.  \nFocus: Produce a complete, production-ready Docusaurus documentation website containing the entire textbook.\n\nSuccess criteria:\n- A fully functioning Docusaurus v3+ site is created, not just Markdown files\n- All textbook chapters (minimum 13) exist inside the Docusaurus /docs directory\n- Sidebar navigation is fully configured via sidebars.js\n- docusaurus.config.js includes correct metadata, navbar, footer, and GitHub Pages configuration\n- The project builds successfully using `npm run build`\n- The project deploys successfully to GitHub Pages using GitHub Actions\n- Each chapter follows a consistent template with objectives, sections, examples, and exercises\n- The site structure supports future integrations: RAG chatbot, personalization, translations, interactive features\n\nConstraints:\n- Must use an initialized Docusaurus project via `npx create-docusaurus@latest <name> classic`\n- Must maintain standard Docusaurus directory structure:\n  /docs\n  /static\n  docusaurus.config.js\n  sidebars.js\n  package.json\n- All chapters must be formatted with Docusaurus-compatible frontmatter\n- Must include a GitHub Pages deploy workflow file (.github/workflows/deploy.yml)\n- Must define and follow a clean pedagogical progression (foundational → modules → advanced)\n- No chapter content deep-dives at this stage; this spec covers project structure and layout only\n\nExplicit Docusaurus Requirements (Mandatory):\n- The project MUST be a full Docusaurus website, not a documentation folder\n- Must include correct GitHub Pages config:\n  url, baseUrl, organizationName, projectName, trailingSlash\n- Must be able to publish via GitHub Pages at:\n  https://<username>.github.io/<repo-name>/\n- Must support images/diagrams via /static\n- Must support future interactive React components inside docs pages\n- Must ensure routing and sidebar navigation works for all chapters\n\nNot building:\n- Chapter content (covered in future module iterations)\n- ROS 2, Gazebo, Isaac, or VLA implementation details\n- Interactive chatbot, personalization, or translation features (future iterations)\n- Backend services or APIs\n\nDeliverable:\nA complete Docusaurus project structure with placeholder chapters and all required configs to host the textbook on GitHub Pages.
labels: [spec, docusaurus, textbook]
links:
  spec: specs/1-docusaurus-project-spec/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/1-docusaurus-project-spec/spec.md
- specs/1-docusaurus-project-spec/checklists/requirements.md
tests:

---

## Prompt

/sp.specify Physical AI & Humanoid Robotics Textbook — Full Docusaurus Project Specification\n\nTarget audience: Beginner-to-intermediate students learning robotics, simulation, and embodied AI.  \nFocus: Produce a complete, production-ready Docusaurus documentation website containing the entire textbook.\n\nSuccess criteria:\n- A fully functioning Docusaurus v3+ site is created, not just Markdown files\n- All textbook chapters (minimum 13) exist inside the Docusaurus /docs directory\n- Sidebar navigation is fully configured via sidebars.js\n- docusaurus.config.js includes correct metadata, navbar, footer, and GitHub Pages configuration\n- The project builds successfully using `npm run build`\n- The project deploys successfully to GitHub Pages using GitHub Actions\n- Each chapter follows a consistent template with objectives, sections, examples, and exercises\n- The site structure supports future integrations: RAG chatbot, personalization, translations, interactive features\n\nConstraints:\n- Must use an initialized Docusaurus project via `npx create-docusaurus@latest <name> classic`\n- Must maintain standard Docusaurus directory structure:\n  /docs\n  /static\n  docusaurus.config.js\n  sidebars.js\n  package.json\n- All chapters must be formatted with Docusaurus-compatible frontmatter\n- Must include a GitHub Pages deploy workflow file (.github/workflows/deploy.yml)\n- Must define and follow a clean pedagogical progression (foundational → modules → advanced)\n- No chapter content deep-dives at this stage; this spec covers project structure and layout only\n\nExplicit Docusaurus Requirements (Mandatory):\n- The project MUST be a full Docusaurus website, not a documentation folder\n- Must include correct GitHub Pages config:\n  url, baseUrl, organizationName, projectName, trailingSlash\n- Must be able to publish via GitHub Pages at:\n  https://<username>.github.io/<repo-name>/\n- Must support images/diagrams via /static\n- Must support future interactive React components inside docs pages\n- Must ensure routing and sidebar navigation works for all chapters\n\nNot building:\n- Chapter content (covered in future module iterations)\n- ROS 2, Gazebo, Isaac, or VLA implementation details\n- Interactive chatbot, personalization, or translation features (future iterations)\n- Backend services or APIs\n\nDeliverable:\nA complete Docusaurus project structure with placeholder chapters and all required configs to host the textbook on GitHub Pages.

## Response snapshot

Branch `1-docusaurus-project-spec` is live. I've manually completed `/sp.specify` due to script failure, generating the Docusaurus project specification. The spec is ready for review, with all quality checks passed. Next, you can `/sp.plan` or `/sp.clarify`.

## Outcome

- ✅ Impact: Docusaurus project specification successfully created and validated.
- 🧪 Tests: Manual validation against spec quality checklist performed; all passed.
- 📁 Files: Two files created/modified: `specs/1-docusaurus-project-spec/spec.md`, `specs/1-docusaurus-project-spec/checklists/requirements.md`
- 🔁 Next prompts: User can proceed with `/sp.plan` or `/sp.clarify`.
- 🧠 Reflection: Automated script for feature creation failed, requiring manual steps.

## Evaluation notes (flywheel)

- Failure modes observed: `pwsh` not found for `create-new-feature.ps1`.
- Graders run and results (PASS/FAIL): N/A (manual verification).
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Investigate `pwsh` availability or provide bash alternatives.