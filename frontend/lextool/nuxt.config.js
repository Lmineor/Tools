
export default {
  mode: 'universal',
  /*
  ** Headers of the page
  */
  head: {
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  /*
  ** Customize the progress-bar color
  */
  loading: { 
    color: '#00adb5',
    height: '4px'
  },
  /*
  ** Global CSS
  */
  css: [
    'normalize.css',
    '~styles/main.scss',
    'eva-icons/style/eva-icons.css'
  ],
  
  styleResources: {
    scss: ['styles/variables.scss']
  },
  /*
  ** Plugins to load before mounting the App
  */
  plugins: [
    {
      src: './components/UI/index.js',
    },
    {
      src: '~/plugins/vue-good-table.js'
    },
    {
      src: './plugins/vue-lazyload.js',
      ssr: false
    },
    {
      src: './plugins/vuejs-noty.js',
      ssr: false
    },
    {
      src: './plugins/modal.js',
      ssr: false
    },
  ],
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
      // Doc: https://axios.nuxtjs.org/usage
      '@nuxtjs/axios',
      '@nuxtjs/pwa',
      '@nuxtjs/style-resources',
      // [
      //     '@nuxtjs/google-analytics',
      //     {
      //         id: ''
      //     }
      // ],
      [
          'vue-sweetalert2/nuxt',
          {
              confirmButtonColor: '#249ffd',
              animation: false,
              customClass: {
                  popup: 'sweetalert2'
              }
          }
      ]
  ],
  /*
  ** Build configuration
  */
 build: {
  /*
   ** You can extend webpack config here
   */
  postcss: {
      plugins: {
          'postcss-pxtorem': {
              rootValue: 16,
              propList: ['*'],
              selectorBlackList: ['html']
          },
          autoprefixer: {}
      }
    }
  },
  manifest: {
    description: '收集实用的小工具',
    display: 'standalone',
    name: 'MikuTools',
    short_name: 'MikuTools',
    start_url: '/',
    background_color: '#ffffff',
    theme_color: '#ffffff',
    scope: '/',
    lang: 'zh-cn'
  },
    // workbox: {
    //     runtimeCaching: [
    //         {
    //             urlPattern: 'https://mikutools.cdn.hazymoon.vip/.*'
    //         }
    //     ],
    //     offlinePage: '/offline.html',
    //     offlineAssets: ['/offline.html']
    // },
    router: {
      prefetchLinks: false,
      middleware: ['getCurrentTool', 'baidupush']
    }
};