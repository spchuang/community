/*
   the idea here is to separate the logic of model and presentation (view). I'll read
   
   Should we have a one page app?
*/

define(function (require) {
   "use strict";
   var $           = require('jquery'),
       _           = require('underscore'),
       Backbone    = require('backbone'),
       handlebars  = require('handlebars'),
       //wallPostTemplate = require('text!templates/wall/post.html'),
       //WallPostModels  = require('app/models/wallPosts'),
       $body       = $('body');
      
   //posts views
   
   var WallPostsView = Backbone.View.extend({
      el: $('#wall_content'),
      render: function(){
         /*var data = {};
         var compiledTemplate = Handlebars.compile(wallPostTemplate);
         this.$el.append( compiledTemplate(data));*/
      }
   });
   
   
   require(['app/models/wallPost'], function (models) {
      var wall = new models.WallPostCollection();
      wall.fetch({
         success: function (data) {
            console.log(data.models[0].attributes);
         }
      });

    
   });
   console.log("TEST");
});