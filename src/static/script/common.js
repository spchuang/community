
requirejs.config({
    baseUrl: '/static/',
    paths: {
        app:         'script/app',
        jquery:      'vendors/jquery/1.9.1/jquery.min',
        handlebars:  'vendors/handlebars-v1.1.2',
        backbone:    'vendors/backbone-1.1.0.min.js',
        underscore:  'vendors/underscore-1.5.2.min.js'
    },
    shim: {
      underscore: {
         exports: '_'
      },
      backbone: {
         deps: ["underscore", "jquery"],
         exports: "Backbone"
      }
    },
    urlArgs: "bust=" + (new Date()).getTime() //remove cache
});