
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
        sugar: 		 'sugar.min',
        bootstrap:    'bootstrap/3.0.2/bootstrap.min',
        editable:     'bootstrap3-editable-1.5.1/bootstrap3-editable/js/bootstrap-editable'

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
      },
      editable:{
         deps: ["bootstrap", "jquery"]
      }
      
      
    },
    urlArgs: "bust=" + (new Date()).getTime(), //remove cache
    
});

//include csrf token to Backone in global scope
define(['backbone', 'jquery', 'underscore'], function(Backbone, $, _){
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
   
   //override backbone save to handle server validation errors
   var oldSave = Backbone.Model.prototype.save;
   Backbone.Model.prototype.save = function(){
      var returnedValue = oldSave.apply(this, arguments),
      deferred = new $.Deferred();
      //console.log(deferred);
      
      if(_.isBoolean(returnedValue)){
         this.validate(this.attributes);
         deferred.reject(this.validationError || 'error');
         return deferred.promise();
      }
      
      
      
      return returnedValue;
   }

});


