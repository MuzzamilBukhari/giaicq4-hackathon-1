// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics Textbook',
  tagline: 'A comprehensive guide to embodied intelligence and humanoid systems.',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  // Update this to your actual Vercel domain when deployed
  url: 'https://giaicq4-hackathon-1-muzzamilbukharis-projects.vercel.app/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For Vercel deployment, use '/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'MuzzamilBukhari', // Usually your GitHub org/user name.
  projectName: 'giaicq4-hackathon-1', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/MuzzamilBukhari/giaicq4-hackathon-1/tree/main/',
        },
        blog: false, // Disable blog for this textbook
        theme: {
          customCss: './src/css/custom-theme.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      colorMode: {
        respectPrefersColorScheme: true,
      },
      navbar: {
        title: 'Physical AI & Humanoid Robotics',
        logo: {
          alt: 'Textbook Logo',
          src: 'img/logo.svg', // Assuming a logo will be placed here
        },
        items: [
          {
            to: 'docs/intro',
            position: 'left',
            label: 'Textbook',
          },
          {
            to: 'docs/setup-guides',
            position: 'left',
            label: 'Setup Guides',
          },
          {
            href: 'https://github.com/MuzzamilBukhari/giaicq4-hackathon-1',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Learning Modules',
            items: [
              {
                label: 'Introduction',
                to: '/docs/intro',
              },
              {
                label: 'Module 1: ROS 2 Fundamentals',
                to: '/docs/modules/module-1-ros2',
              },
              {
                label: 'Module 2: Digital Twin',
                to: '/docs/modules/module-2-digital-twin',
              },
              {
                label: 'Module 3: NVIDIA Isaac Sim',
                to: '/docs/modules/module-3-isaac-sim',
              },
              {
                label: 'Module 4: VLA & Humanoid',
                to: '/docs/modules/module-4-vla',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'Setup Guides',
                to: '/docs/setup-guides',
              },
              {
                label: 'Hardware Setup',
                to: 'docs/setup-guides/setup-guides-hardware-setup',
              },
              {
                label: 'Software Setup',
                to: 'docs/setup-guides/setup-guides-software-setup',
              },
              {
                label: 'Glossary',
                to: 'docs/references/glossary',
              },
            ],
          },
          {
            title: 'Community & Tools',
            items: [
              {
                label: 'ROS 2 Documentation',
                href: 'https://docs.ros.org/en/humble/',
              },
              {
                label: 'NVIDIA Isaac Sim',
                href: 'https://developer.nvidia.com/isaac-sim',
              },
              {
                label: 'GitHub Repository',
                href: 'https://github.com/MuzzamilBukhari/giaicq4-hackathon-1',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
