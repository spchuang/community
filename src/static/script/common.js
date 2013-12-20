
requirejs.config({
    baseUrl: '/static/script/vendors/',
    paths: {
    
        app:         '../app',
        jquery:      'jquery/1.9.1/jquery.min',
        //jquery:      'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
        handlebars:  'handlebars-v1.1.2',
        //backbone:    'http://documentcloud.github.com/backbone/backbone-min.js',
        //underscore:  'http://documentcloud.github.com/underscore/underscore-min.js'
        backbone:    'backbone-1.1.0.min',
        underscore:  'underscore-1.5.2.min'    
   },
    shim: {
      underscore: {
         exports: '_'
      },
      backbone: {
         deps: ["underscore", "jquery"],
         exports: "Backbone"
      },
      handlebars: {
         exports: 'Handlebars'
      },
    },
    urlArgs: "bust=" + (new Date()).getTime(), //remove cache
    
});