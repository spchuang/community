//Each event in calendar
define('newTaskModal', function(require){
   var Backbone      = require('backbone'),
       _             = require('underscore'),
       jquery        = require('jquery'),
       Handlebars    = require('handlebars'),
       bootstrap     = require('bootstrap'),
       sugar			= require('sugar'),
       tpl           = require('text!app/task/taskModal.html');
       
   var newTaskModalView = Backbone.View.extend({
      className: 'modal fade',
      template: Handlebars.compile(tpl),
      
      events: {
      	'click .close'	  : 'close',
      	'click .cancel'  : 'close',
      	'hidden.bs.modal': 'teardown',
         'click .ok'		  : 'save',
      },
      
      initialize: function(options) {
         this.$content = this.$el.find('.modal-body');
      },
      render: function() {
      
      	this.$el.html(this.template());
      	return this;
      },
      
      save: function() {
      	this.trigger('create');
      	this.close();
      },

      open: function() {
      	this.$el.modal('show');
      },
      close: function(event) {
      	this.$el.modal('hide');

      },
      teardown: function(event){

      }
      

   });
   
   return newTaskModalView;
});

define('taskSidebar', function(require){
   var Backbone      = require('backbone'),
       Handlebars    = require('handlebars'),
       timeago       = require('timeago'),
       tpl           = require('text!app/task/sidebarTaskItem.html');

   var ItemView = Backbone.View.extend({
      el: $("#task_sidebar"),
      template: Handlebars.compile(tpl),
      events: {
         'click li'     : 'select',
      },
      
      render: function() {
         this.$el.html(this.template(this.model.toJSON()));
         //apply time ago
         this.$el.find(".comment_time").timeago();
         return this;
      },
      select: function(event){
         event.stopPropagation();
         console.log("SELECT");
      }
   });
   return ItemView;
});



define(function (require) {
   var $            = require('jquery'),
       _            = require('underscore'),
       Backbone     = require('backbone'),
       Handlebars   = require('handlebars'),
       tpl          = require('text!app/task/taskApp.html'),
       taskModal    = require('newTaskModal');
       
   
       
   var TaskView = Backbone.View.extend({
      el: $("#task"), 
      template: Handlebars.compile(tpl),
      initialize: function(options){
         _.bindAll.apply(_, [this].concat(_.functions(this)));
         this.taskModal = new taskModal();
         this.listenTo(this.taskModal, 'create', this.addTask);
         this.render();
         
      },
      events: {
         'click #add_button': 'openTaskModal' 
      },
      
      render: function() {
         this.$el.html(this.template());
         this.taskModal.render();
         return this;
      },
      openTaskModal: function(){
         this.taskModal.open();
      },
      addTask: function(){
         console.log("COOL");
      }
      
   });
   return TaskView; 
});