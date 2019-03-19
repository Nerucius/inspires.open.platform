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
    // Route Prerenderer
    prerenderSpa: {
      // renderRoutes: [ '/', '/about' ],
      renderRoutes: [],
      headless: true,
      registry: undefined,
      onlyProduction: true,
      useRenderEvent: true,
      postProcess: route => {
        // Defer scripts and tell Vue it's been server rendered to trigger hydration
        route.html = route.html
          .replace(/<script (.*?)>/g, '<script $1 defer>')
          .replace('id="app"', 'id="app" data-server-rendered="true"');
        return route;
      }
    }
  }
}