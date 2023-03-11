// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
    title: 'File Validator',
    tagline: 'Python validation library to validate files using type, mime, extension, magic numbers and size',
    favicon: 'img/favicon.ico',
    plugins: [require.resolve('docusaurus-lunr-search')],
    // Set the production url of your site here
    url: 'https://file-validator.github.io',
    // Set the /<baseUrl>/ pathname under which your site is served
    // For GitHub pages deployment, it is often '/<projectName>/'
    baseUrl: '/',

    // GitHub pages deployment config.
    // If you aren't using GitHub pages, you don't need these.

    organizationName: 'file-validator', // Usually your GitHub org/user name.
    projectName: 'file-validator.github.io', // Usually your repo name.


    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',

    // Even if you don't use internalization, you can use this field to set useful
    // metadata like html lang. For example, if your site is Chinese, you may want
    // to replace "en" with "zh-Hans".
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
                    sidebarPath: require.resolve('./sidebars.js'),
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    editUrl:
                        'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
                },
                blog: {
                    showReadingTime: true,
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    editUrl:
                        'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
                },
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            }),
        ],
    ],

    themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
        ({
            // Replace with your project's social card
            image: 'img/docusaurus-social-card.jpg',
            navbar: {
                title: 'File Validator',
                logo: {
                    alt: 'My Site Logo',
                    src: 'img/file-validator.png',
                },
                items: [
                    {
                        type: 'doc',
                        docId: 'intro',
                        position: 'left',
                        label: 'Document',
                    },
                    {
                        href: 'https://github.com/file-validator/',
                        position: 'right',
                        className: 'header-github-link',
                    },
                    {
                        type: 'docsVersionDropdown',
                        position: 'right',
                        dropdownItemsAfter: [{to: '/versions', label: 'All versions'}],
                        dropdownActiveClassDisabled: true,
                    },
                ],
            },
            footer: {
                style: 'dark',
                links: [
                    {
                        title: 'Docs',
                        items: [
                            {
                                label: 'Documents',
                                to: '/docs/intro',
                            },
                        ],
                    },
                    {
                        title: 'Community',
                        items: [
                            {
                                label: 'Do you have a question? ask the community',
                                href: 'https://github.com/orgs/file-validator/discussions',
                            },
                            {
                                label: 'Do you see a bug? open an issue on GitHub',
                                href: 'https://github.com/file-validator/file-validator/issues',
                            },
                        ],
                    },
                    {
                        title: 'More',
                        items: [
                            {
                                label: 'GitHub',
                                href: 'https://github.com/file-validator/file-validator/',
                            },
                        ],
                    },
                ],
                copyright: `Copyright © ${new Date().getFullYear()} File Validator`,
            },
            prism: {
                theme: lightCodeTheme,
                darkTheme: darkCodeTheme,
            },
        }),
};

module.exports = config;
