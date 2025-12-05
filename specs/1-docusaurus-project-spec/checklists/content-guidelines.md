# Content Guidelines for Textbook Writers

This document provides guidelines for writing and formatting content for the Physical AI & Humanoid Robotics Textbook built with Docusaurus. Following these guidelines ensures consistency, readability, and proper rendering of your content.

## Markdown Basics

All content should be written in Markdown (`.md`) format. Docusaurus supports [GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/).

### Headings

Use ATX headings (with `#`): `# H1`, `## H2`, `### H3`, etc. Always start with `## H2` for main sections within a chapter, as `H1` is typically reserved for the chapter title defined in frontmatter.

### Paragraphs

Separate paragraphs with a blank line.

### Emphasis

-   *Italic*: `*text*` or `_text_`
-   **Bold**: `**text**` or `__text__`
-   ***Bold Italic***: `***text***` or `___text___`

### Lists

-   **Unordered lists**: Use `-`, `*`, or `+`.
-   **Ordered lists**: Use `1.`, `2.`, `3.`, etc.

## Docusaurus Frontmatter

Each Markdown file representing a chapter or document **must** start with Docusaurus frontmatter (YAML block) at the very top. This configures metadata like the document ID, title, and sidebar position.

```markdown
---
id: your-document-id
title: "Your Document Title"
sidebar_position: X
---
```

-   `id`: A unique identifier for the document (e.g., `chapter-1-foundations-of-physical-ai`, `glossary`). This is used for linking.
-   `title`: The title displayed in the browser tab and at the top of the page.
-   `sidebar_position`: A number that determines the order of the document in the sidebar. Lower numbers appear higher up. For chapters, ensure sequential numbering (e.g., Chapter 1: `1`, Chapter 2: `2`).

## Internal Links

Link to other documents within the Docusaurus site using their `id` as part of the path:

```markdown
[Link Text](/docs/your-document-id)
```

For example, to link to Chapter 1:

```markdown
[Foundations of Physical AI](/docs/chapter-1-foundations-of-physical-ai)
```

To link to a specific heading within a document:

```markdown
[Section Title](/docs/your-document-id#section-slug)
```

(Docusaurus automatically generates slugs for headings. You can find them by inspecting the URL when navigating to a heading.)

## Code Blocks

Use fenced code blocks with language highlighting:

````markdown
```python
print("Hello, Physical AI!")
```
````

Replace `python` with the appropriate language (e.g., `javascript`, `cpp`, `bash`).

## Images

Place images in the `static/img/` directory. Reference them using absolute paths:

```markdown
![Alt text for image](/img/your-image-name.png)
```

For example:

```markdown
![Robotics Diagram](/img/robotics-diagram.png)
```

## Admonitions (Info/Warning/Danger Blocks)

Docusaurus supports admonitions for callouts:

```markdown
:::tip
This is a helpful tip!
:::

:::warning
Be careful with this!
:::

:::danger
Critical information.
:::
```

## Tables

Use standard Markdown table syntax:

```markdown
| Header 1 | Header 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```
