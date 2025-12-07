# Feature Specification: Restore Default Docusaurus Layout and Apply Color Theme

**Feature Branch**: `1-docusaurus-ui`
**Created**: 2025-12-07
**Status**: Draft
**Input**: User description: "Restore default Docusaurus layout, apply color theme via CSS variables, remove layout overrides, and deploy latest modules (2,3,4) + UI changes to GitHub

Target audience: Authors and readers of the Docusaurus textbook who need a modern, responsive UI that uses the project's color palette but preserves all default Docusaurus layout/responsive behavior.

Focus:
1. Revert any custom structural CSS that changes layout, padding, sidebar behavior, animations, breakpoints, or component structure.
2. Keep the site's color palette (White, Silver, Blue Gradient) but apply colors only through well-defined CSS variables (no layout/positioning changes).
3. Ensure mobile sidebar behaves using the Docusaurus default (slide-over or default mobile nav), and that spacing/padding/responsive rules are the Docusaurus defaults.
4. Deploy all latest content changes (Module 2, Module 3, Module 4) and the UI changes to GitHub; if Vercel is used, ensure Vercel deployment settings remain valid.

Success criteria:
- All structural custom CSS overrides that affect layout or responsive behavior are removed.
- A single CSS variables file (e.g., `src/css/theme-variables.css` or `src/css/custom-theme.css`) defines the color palette only:

:root {
--color-bg: #ffffff;
--color-surface: #f3f4f6; /* silver-ish /
--color-primary-0: #0ea5e9; / blue gradient start /
--color-primary-1: #2563eb; / blue gradient end */
--color-text: #0f172a;
--color-link: var(--color-primary-1);
}

and theme uses these variables (no layout CSS).
- No overrides exist that change Docusaurus default sidebar/padding/breakpoints/animations.
- Mobile sidebar operates exactly like an out-of-the-box Docusaurus site.
- Docusaurus builds (`npm run build`) and serves (`npm run serve`) successfully.
- Latest content for Modules 2, 3, 4 is included in the deployed site.
- Changes are pushed to GitHub in branch `fix/ui-restore-deploy` with a PR opened to `main`.
- GitHub Pages (or Vercel) deploys successfully; provide the deployment URL.

Constraints:
- Do not change component markup or Docusaurus core files beyond configuration and adding/removing site CSS.
- Do not add new layout JS or CSS that manipulates element positions or breakpoints.
- Keep all changes backward-compatible with existing content/sidebars.
- If the repo is monorepo/subfolder-based, operate relative to the Docusaurus project root (detect `package.json`).

Deliverables:
1. `src/css/custom-theme.css` (only CSS variables + non-layout color rules).
2. Removal or comment-out of any CSS files that override layout (list produced by the script).
3. `specs/ui/fix-report.md` summarizing removed files, changed files, and before/after screenshots (local).
4. Branch `fix/ui-restore-deploy` with commits and a PR to `main`.
5. A successful GitHub deployment (or Vercel confirmation) and the public URL.
6. Build logs saved to `specs/ui/build-logs.md`.

Not building:
- New UI components or complex visual redesigns other than color updates.
- Changes to accessibility beyond verifying the default Docusaurus accessibility baseline.

If"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Textbook Reader Experience (Priority: P1)

As a reader of the Physical AI & Humanoid Robotics textbook, I want to access the content through a responsive, well-designed interface that uses the project's color palette so that I can have a pleasant reading experience with consistent styling across all devices.

**Why this priority**: This is the primary user of the textbook who needs to access the content, and a good reading experience is critical to the project's success.

**Independent Test**: Can be fully tested by visiting the site on different devices and browsers, and delivers a consistent, readable interface with the correct color scheme.

**Acceptance Scenarios**:

1. **Given** I am accessing the textbook website, **When** I view it on desktop, tablet, or mobile, **Then** the layout should be responsive and use the default Docusaurus behavior without custom layout overrides.
2. **Given** I am viewing the textbook content, **When** I navigate through different sections, **Then** the sidebar should behave like a standard Docusaurus site with proper mobile navigation.

---

### User Story 2 - Content Author Experience (Priority: P2)

As an author contributing to the textbook, I want the site to maintain default Docusaurus styling behavior so that I can focus on content creation without worrying about layout inconsistencies.

**Why this priority**: Authors need a predictable environment to create content, and maintaining standard Docusaurus behavior ensures consistency.

**Independent Test**: Can be tested by reviewing the site's styling consistency and ensuring that the default Docusaurus components render correctly.

**Acceptance Scenarios**:

1. **Given** I am viewing a documentation page, **When** I look at the styling, **Then** the colors should match the specified palette (white background, silver surface, blue gradient accents).

---

### User Story 3 - Mobile Navigation (Priority: P3)

As a mobile user accessing the textbook, I want the sidebar to behave according to Docusaurus defaults so that I can navigate the content easily on small screens.

**Why this priority**: Mobile users need proper navigation functionality to access all content effectively.

**Independent Test**: Can be tested by opening the site on a mobile device or mobile emulator and verifying the sidebar behavior matches default Docusaurus patterns.

**Acceptance Scenarios**:

1. **Given** I am on a mobile device viewing the textbook, **When** I try to access the sidebar, **Then** it should behave like a standard Docusaurus mobile navigation.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST remove any custom CSS that overrides Docusaurus default layout, padding, sidebar behavior, animations, breakpoints, or component structure
- **FR-002**: System MUST apply the specified color palette using CSS variables: white background (#ffffff), silver surface (#f3f4f6), blue gradient (#0ea5e9 to #2563eb), dark text (#0f172a)
- **FR-003**: System MUST ensure mobile sidebar operates exactly like an out-of-the-box Docusaurus site
- **FR-004**: System MUST maintain backward compatibility with existing content and sidebars
- **FR-005**: System MUST build successfully using `npm run build` and serve using `npm run serve`
- **FR-006**: System MUST include the latest content for Modules 2, 3, and 4 in the deployed site
- **FR-007**: System MUST use CSS variables for theming without any layout/positioning CSS rules

### Key Entities *(include if feature involves data)*

- **Color Theme**: Represents the visual styling of the textbook site, including background, surface, primary colors, text, and link colors defined through CSS variables
- **Layout Configuration**: Represents the structural elements of the site including sidebar behavior, responsive breakpoints, and mobile navigation patterns

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All structural custom CSS overrides that affect layout or responsive behavior are removed from the site
- **SC-002**: A single CSS variables file defines the color palette with the specified colors (white, silver, blue gradient) without layout CSS
- **SC-003**: The Docusaurus build process completes successfully without errors (`npm run build`)
- **SC-004**: The site serves correctly in development mode (`npm run serve`)
- **SC-005**: Mobile sidebar operates exactly like an out-of-the-box Docusaurus site with proper responsive behavior
- **SC-006**: All content for Modules 2, 3, and 4 is accessible and properly formatted in the deployed site
- **SC-007**: GitHub deployment (or Vercel) completes successfully with a working public URL