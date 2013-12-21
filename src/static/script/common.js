
requirejs.config({
    baseUrl: '/static/script/vendors/',
    paths: {
    
        app:          '../app',
        jquery:       'jquery/1.9.1/jquery.min',
        //jquery:      'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
        handlebars:   'handlebars-v1.1.2',
        //backbone:    'http://documentcloud.github.com/backbone/backbone-min.js',
        //underscore:  'http://documentcloud.github.com/underscore/underscore-min.js'
        backbone:     'backbone-1.1.0.min',
        underscore:   'underscore-1.5.2.min',
        timeago:      'jquery.timeago',
        jquery_ui:    'jquery-ui.custom.min',
        fullcalendar: 'fullcalendar/1.6.4/fullcalendar',
        bootstrap:    'bootstrap/3.0.2/bootstrap.min'

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
      fullcalendar: {
         deps: ["jquery", "jquery_ui"],
         exports: 'fullcalendar'
      },
      jquery_ui: {
         deps: ['jquery'],
      },
      bootstrap: {
         deps: ["jquery"]
      }
      
    },
    urlArgs: "bust=" + (new Date()).getTime(), //remove cache
    
});

//include csrf token to Backone in global scope
define(['backbone'], function(Backbone){
   var csrftoken = $('meta[name=csrf-token]').attr('content');
   var oldSync = Backbone.sync;
   Backbone.sync = function(method, model, options){
      options.beforeSend =  function(xhr, settings) {
         if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
         }
       }
      return oldSync(method, model, options);
   };
});