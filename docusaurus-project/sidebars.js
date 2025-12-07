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
            'modules/module-2-digital-twin/index',
            {
              type: 'category',
              label: 'Chapter 1: Gazebo Fundamentals',
              items: [
                'modules/module-2-digital-twin/chapter-1-gazebo-fundamentals/index',
                'modules/module-2-digital-twin/chapter-1-gazebo-fundamentals/lab',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 2: Unity for Robotics',
              items: [
                'modules/module-2-digital-twin/chapter-2-unity-for-robotics/index',
                'modules/module-2-digital-twin/chapter-2-unity-for-robotics/lab',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 3: Sim-to-Real Transfer',
              items: [
                'modules/module-2-digital-twin/chapter-3-sim-to-real-transfer/index',
                'modules/module-2-digital-twin/chapter-3-sim-to-real-transfer/lab',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Module 3: NVIDIA Isaac Sim (Weeks 8-10)',
          items: [
            'modules/module-3-isaac-sim/index',
            {
              type: 'category',
              label: 'Chapter 1: Isaac Sim Setup',
              items: [
                'modules/module-3-isaac-sim/chapter-1-isaac-sim-setup/index',
                'modules/module-3-isaac-sim/chapter-1-isaac-sim-setup/lab',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 2: Perception Pipeline',
              items: [
                'modules/module-3-isaac-sim/chapter-2-perception-pipeline/index',
                'modules/module-3-isaac-sim/chapter-2-perception-pipeline/lab',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 3: AI Training Integration',
              items: [
                'modules/module-3-isaac-sim/chapter-3-ai-training-integration/index',
                'modules/module-3-isaac-sim/chapter-3-ai-training-integration/lab',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Module 4: VLA & Humanoids (Weeks 11-13)',
          items: [
            'modules/module-4-vla/index',
            {
              type: 'category',
              label: 'Chapter 1: VLA Fundamentals',
              items: [
                'modules/module-4-vla/chapter-1-vla-fundamentals/index',
                'modules/module-4-vla/chapter-1-vla-fundamentals/chapter-1-vla-fundamentals-lab',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 2: Humanoid Kinematics',
              items: [
                'modules/module-4-vla/chapter-2-humanoid-kinematics/chapter-2-humanoid-kinematics-index',
                'modules/module-4-vla/chapter-2-humanoid-kinematics/chapter-2-humanoid-kinematics-lab',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 3: Bipedal Locomotion',
              items: [
                'modules/module-4-vla/chapter-3-bipedal-locomotion/chapter-3-bipedal-locomotion-index',
                'modules/module-4-vla/chapter-3-bipedal-locomotion/chapter-3-bipedal-locomotion-lab',
              ],
            },
            {
              type: 'category',
              label: 'Chapter 4: Integration & Deployment',
              items: [
                'modules/module-4-vla/chapter-4-integration-deployment/chapter-4-integration-deployment-index',
                'modules/module-4-vla/chapter-4-integration-deployment/chapter-4-integration-deployment-lab',
              ],
            },
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

