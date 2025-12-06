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
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapters',
      link: {
        type: 'doc',
        id: 'chapters-overview',
      },
      items: [
        'chapter-1-foundations-of-physical-ai',
        'chapter-2-ros2-fundamentals',
        'chapter-3-gazebo-simulation',
        'chapter-4-unity-visualization',
        'chapter-5-nvidia-isaac-sim',
        'chapter-6-perception-and-slam',
        'chapter-7-humanoid-kinematics',
        'chapter-8-humanoid-dynamics',
        'chapter-9-locomotion-control',
        'chapter-10-manipulation-systems',
        'chapter-11-human-robot-interaction',
        'chapter-12-conversational-robotics',
        'chapter-13-vla-driven-robotics',
      ],
    },
    {
      type: 'category',
      label: 'Modules',
      items: [
        {
          type: 'category',
          label: 'Module 1 — ROS 2 Fundamentals',
          link: {
            type: 'doc',
            id: 'module-1-ros2/module-1-ros2-introduction',
          },
          items: [
            'module-1-ros2/module-1-ros2-nodes-topics',
            'module-1-ros2/module-1-ros2-services-actions',
            'module-1-ros2/module-1-ros2-rclpy-patterns',
            'module-1-ros2/module-1-ros2-urdf-robot-description',
            'module-1-ros2/module-1-ros2-launch-files-params',
            'module-1-ros2/module-1-ros2-agent-ros-bridge',
            'module-1-ros2/module-1-ros2-capstone',
          ],
        },
        // Module 2..4 will be added as they are implemented
      ],
    },
    'glossary',
    'appendix',
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
