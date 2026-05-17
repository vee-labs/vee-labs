import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'Vee Labs',
  description: 'Building apps that matter — mobile, security, and open-source experiments.',
  lastUpdated: true,
  head: [
    ['meta', { name: 'theme-color', content: '#3c3c44' }],
    ['meta', { name: 'og:type', content: 'website' }],
    ['meta', { name: 'og:locale', content: 'en' }],
    ['meta', { name: 'og:site_name', content: 'Vee Labs' }],
  ],
  themeConfig: {
    siteTitle: 'Vee Labs',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Projects', link: '/projects/' },
      { text: 'Guide', link: '/guide/' },
      { text: 'GitHub', link: 'https://github.com/vee-labs' },
    ],
    sidebar: {
      '/projects/': [
        {
          text: 'Projects',
          items: [
            { text: 'Overview', link: '/projects/' },
            { text: 'BreachGuard', link: '/projects/breachguard' },
            { text: 'ACServiceApp', link: '/projects/acservice' },
          ],
        },
      ],
      '/guide/': [
        {
          text: 'Guide',
          items: [
            { text: 'Getting Started', link: '/guide/' },
            { text: 'API Reference', link: '/guide/api' },
            { text: 'Examples', link: '/guide/examples' },
            { text: 'Contributing', link: '/guide/contributing' },
          ],
        },
      ],
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/vee-labs' },
    ],
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 Vee Labs',
    },
    search: {
      provider: 'local',
    },
  },
})
