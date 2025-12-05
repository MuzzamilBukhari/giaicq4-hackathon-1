# Tasks: Physical AI & Humanoid Robotics Textbook — Full Docusaurus Project Specification

**Feature**: Initialize a production-ready Docusaurus website and create placeholder textbook chapters (Iteration 1: Book Structure Layout)
**Goal**: Produce a ready-to-build Docusaurus project with placeholder Markdown files for all chapters, working sidebar, and GitHub Pages deployment workflow. Tasks must be atomic, actionable, and produce files in the repository.

## Implementation Strategy

This implementation focuses on delivering a Minimum Viable Product (MVP) for the Docusaurus textbook structure. Tasks are organized into sequential phases, starting with foundational setup, progressing through user stories, and concluding with polish and finalization. Each user story is designed to be independently testable, with early validation steps to ensure core functionality.

## Dependencies

User Story completion order:
1.  Browse Textbook Chapters (P1)
2.  View Diagrams and Examples (P1)
3.  Deploy Textbook to GitHub Pages (P2)

Note: Foundational tasks must be completed before any User Story-specific tasks can be fully validated.

## Phases

### Phase 1: Setup

Goal: Initialize the core Docusaurus project structure.

- [x] T001 Initialize Docusaurus project using `npx create-docusaurus@latest humanoid-textbook classic` (Output: `docusaurus-project/`)

### Phase 2: Foundational

Goal: Establish the basic file structure and core configuration required for all user stories.

- [x] T002 [P] Create placeholder Markdown files for Intro, Chapters 1-13, Glossary, and Appendix in `docusaurus-project/docs/`. Each file to include Docusaurus frontmatter (`id`, `title`, `sidebar_position`), learning objectives placeholder, summary, and a TODO note for content author.
- [x] T003 Create `sidebars.js` with ordered sidebar entries matching `sidebar_position` fields, ensuring a single, deterministic sidebar that groups Intro → Chapters → Glossary → Appendix. (Output: `docusaurus-project/sidebars.js`)
- [x] T004 Configure `docusaurus.config.js` with metadata (`title`, `tagline`, `url`, `baseUrl`, `organizationName`, `projectName`, `trailingSlash: false`), navbar entries (Intro, Chapters dropdown, Glossary), and footer with repo link. (Output: `docusaurus-project/docusaurus.config.js`)
- [x] T005 Update `package.json` scripts to include `start`, `build`, `serve`, `deploy`. (Output: `docusaurus-project/package.json`)
- [x] T006 [P] Create static assets directory `docusaurus-project/static/img/` and add a placeholder `docusaurus-project/static/img/placeholder.png`.
- [x] T007 Create GitHub Actions deploy workflow file using Docusaurus recommended GitHub Pages action, ensuring it references `docusaurus-project` root. (Output: `.github/workflows/deploy.yml`)

### Phase 3: User Story 1 - Browse Textbook Chapters [P1]

Goal: Ensure students can navigate the Docusaurus site to browse all textbook chapters, guaranteeing a clear and intuitive learning flow.

- [ ] T008 [US1] Validate local serve (`npm run serve`) renders the sidebar and all placeholder chapter pages correctly via sidebar navigation.

### Phase 4: User Story 2 - View Diagrams and Examples [P1]

Goal: Ensure students can view embedded diagrams and code examples within each chapter, supporting visual and practical learning.

- [ ] T009 [US2] Validate that placeholder images (`docusaurus-project/static/img/placeholder.png`) and code blocks render correctly within chapter Markdown files locally.

### Phase 5: User Story 3 - Deploy Textbook to GitHub Pages [P2]

Goal: Enable the project administrator to successfully build and deploy the Docusaurus site to GitHub Pages using automated workflows.

- [ ] T010 [US3] Validate the `.github/workflows/deploy.yml` file for syntactic correctness and ensure GitHub Pages configuration in `docusaurus.config.js` is correct.

### Phase 6: Polish & Cross-Cutting Concerns

Goal: Perform overall project validation and prepare documentation for future content writers.

- [ ] T011 Local build and validation: Run `npm install` then `npm run build`. Validate that the build succeeds and the `build/` directory is produced. Record build logs and validation notes in `specs/1-docusaurus-project-spec/checklists/build-validate.md`.
- [ ] T012 Create `dev-setup.md`, `content-guidelines.md`, and `deploy.md` checklists/guides in `specs/1-docusaurus-project-spec/checklists/` to assist future writers.

### Phase 7: Finalization

Goal: Deliver the initial Docusaurus project skeleton to the repository via a Pull Request.

- [ ] T013 Commit all generated files, create a new branch `feature/docusaurus-skeleton`, push the branch, and open a Pull Request with a description referencing the spec and plan. Record the PR link in `specs/1-docusaurus-project-spec/contracts/pr-links.md`.
