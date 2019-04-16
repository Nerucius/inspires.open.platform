module.exports = {
  pwa: {
    name: 'InSPIRES Platform'
  },

  // Allow npm run serve on local testing domain
  devServer: {
    compress: true,
    public: process.env.LOCAL_TESTING_DNS,
    port: 80
  },

  chainWebpack: config => {
    // disable hot reload
    // config.plugins.delete("hmr");
    // enable hashed filenames
    // config.plugin('html').tap(args => {
    //   args[0].hash = true
    //   return args
    // })
  },

  lintOnSave: undefined,
  publicPath: undefined,
  outputDir: undefined,
  assetsDir: undefined,
  runtimeCompiler: undefined,
  productionSourceMap: undefined,
  parallel: undefined,

  pluginOptions: {
    i18n: {
      locale: 'en',
      fallbackLocale: 'en',
      localeDir: 'locales',
      enableInSFC: false
    },
    // Prerender setup with `vue add prerender-spa`
    prerenderSpa: {
      registry: undefined,
      renderRoutes: [
        '/',
        '/login',
        '/about',
        '/projects',
        '/structures',
        '/projects/6-fix-my-food-system',
        '/projects/8-urban-garden',
        '/projects/10-green-care-services',
        '/projects/13-inspires-open-platform',
        '/projects/areas/10-technological-sciences',
        '/projects/areas/20-psychology',
        '/structures/1-isglobal',
        '/structures/2-unifi',
        '/structures/4-essrg',
        '/structures/5-ub',
      ],
      useRenderEvent: true,
      headless: true,
      onlyProduction: true,
      // TODO: Investigate why this is broken
      // postProcess: route => {
      //   // Defer scripts and tell Vue it's been server rendered to trigger hydration
      //   route.html = route.html
      //     .replace(/<script (.*?)>/g, '<script $1 defer>')
      //     .replace('id="app"', 'id="app" data-server-rendered="true"');
      //   return route;
      // }
    }
  }
}
