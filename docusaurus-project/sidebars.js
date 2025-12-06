// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Setup Guides',
      items: [
        'setup-guides/setup-guides-index',
        'setup-guides/setup-guides-hardware-setup',
        'setup-guides/setup-guides-software-setup',
        'setup-guides/setup-guides-cloud-bridge',
      ],
    },
    {
      type: 'category',
      label: 'Modules',
      items: [
        {
          type: 'category',
          label: 'Module 1: ROS 2 (Weeks 3-5)',
          items: [
            'modules/module-1-ros2/module-1-ros2-index',
            {
              type: 'category',
              label: 'Chapter 1: Foundations & Nodes',
              items: [
                'modules/module-1-ros2/chapter-1/module-1-ros2-chapter-1-overview',
                'modules/module-1-ros2/chapter-1/module-1-ros2-chapter-1-topics',
                'modules/module-1-ros2/chapter-1/module-1-ros2-chapter-1-labs',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 2: Services & Actions',
              items: [
                'modules/module-1-ros2/chapter-2/module-1-ros2-chapter-2-overview',
                'modules/module-1-ros2/chapter-2/module-1-ros2-chapter-2-examples',
                'modules/module-1-ros2/chapter-2/module-1-ros2-chapter-2-labs',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Module 2: Digital Twin (Weeks 6-7)',
          items: [
            'modules/module-2-digital-twin/module-2-digital-twin-index',
          ],
        },
        {
          type: 'category',
          label: 'Module 3: NVIDIA Isaac (Weeks 8-10)',
          items: [
            'modules/module-3-isaac/module-3-isaac-index',
          ],
        },
        {
          type: 'category',
          label: 'Module 4: VLA & Humanoids (Weeks 11-13)',
          items: [
            'modules/module-4-vla/module-4-vla-index',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'References',
      items: [
        'references/glossary',
      ],
    },
  ],
};

export default sidebars;

