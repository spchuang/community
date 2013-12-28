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
         this.model.set({
            name     :this.$el.find('input[name="name"]').val(),
            summary  :this.$el.find('input[name="summary"]').val()
         });
      	this.trigger('create', this.model.toJSON());
      	//reset the form
      	this.render();
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
       tpl           = require('text!app/task/taskSidebarItemView.html');

   var taskSidebarView = Backbone.View.extend({
   
      template: Handlebars.compile(tpl),
      initialize: function(options){
         this.$el = options.el;
         this.tasks = options.collection;
         this.listenTo(this.tasks, 'add', this.render);
         this.listenTo(this.tasks, 'reset', this.render);
         this.listenTo(this.tasks, 'remove', this.removeOne);
         
      },
      events: {
         'click a'     : 'select',
      },
      
      render: function() {
         this.$el.empty();
         this.addAll();
         return this;
      },
      addOne: function( task ) {
         var $newItem = $(this.template(task.toJSON()));
         this.$el.prepend($newItem);
         $newItem.find('.created_time').timeago();
      },
      
      addAll: function() {
         //print reversively
         _.each(this.tasks.last(this.tasks.length).reverse(), this.addOne, this);
      },
      
      removeOne: function(task){
         var item = this.$el.find('[data-id='+task.id+']');
         item.fadeOut(300,function() {
             $(this).remove();
         });
      },
      select: function(e){
         e.preventDefault();
         var $target = $(e.currentTarget);
         //set selected item as active
         this.$el.find('a').removeClass('active');
         $target.addClass('active');
         this.trigger("select", $target.data('id'));
      }
   });
   return taskSidebarView;
});

define('mainView', function(require){
   var Backbone      = require('backbone'),
       Handlebars    = require('handlebars'),
       timeago       = require('timeago'),
       $             = require('jquery'),
       editable      = require('editable'),
       tpl           = require('text!app/task/taskMainItemView.html');

   $.fn.editable.defaults.mode = 'inline';
   var taskMainView = Backbone.View.extend({
   
      template: Handlebars.compile(tpl),
      initialize: function(options){
        this.$el = options.el;
        this.$el.on('focus', '[contenteditable]', function() {
            var $this = $(this);
            $this.data('before', $this.html());
            return $this;
         }).on('blur keyup paste input', '[contenteditable]', function() {
            var $this = $(this);
            if ($this.data('before') !== $this.html()) {
               $this.data('before', $this.html());
               $this.trigger('change');
            }
            return $this;
         });
        
      },
      events: {
         'click #delete_task' : 'delete'
      },
      renderEditable: function(fieldName){
         var that = this;
         this.$el.find('#'+fieldName).editable({
            pk:  this.model.get('id'),
            success     : function(response, newValue) {
               that.model.set(fieldName, newValue);
               that.model.save(fieldName, newValue);
               console.log(self.model);
            }
		
         });
      },
      
      render: function() {
         this.$el.html(this.template(this.model.toJSON()));
         this.$el.find('.timeago').timeago();
         this.renderEditable("description");
         
         
         return this;
      },
      delete: function(){
        
         this.trigger('delete', this.model.id);
      },
      show: function(){
         this.$el.fadeIn(300);
      },
      hide: function(){
         this.$el.fadeOut(300);
      }
      

   });
   return taskMainView;
});


define(function (require) {
   var $            = require('jquery'),
       _            = require('underscore'),
       Backbone     = require('backbone'),
       Handlebars   = require('handlebars'),
       tpl          = require('text!app/task/taskApp.html'),
       models       = require('app/task/taskModel'),
       taskModal    = require('newTaskModal'),
       taskSidebarVIew  = require('taskSidebar'),
       taskMainView     = require('mainView');
       
       
   var TaskView = Backbone.View.extend({
      el: $("#task"), 
      template: Handlebars.compile(tpl),
      initialize: function(options){
         _.bindAll.apply(_, [this].concat(_.functions(this)));
         this.render();
         this.tasks        = new models.TaskCollection({communityId: options.communityId}); 
         this.sidebarView  = new taskSidebarVIew({el: $("#task_sidebar"), collection: this.tasks});
         this.mainView     = new taskMainView({el: $("#task_main")});
         this.listen();
         this.tasks.fetch({reset: true});
      },
      events: {
         'click #add_button': 'openTaskModal' 
      },
     
      
      render: function() {
         this.$el.html(this.template());
         //create task modal
         this.taskModal = new taskModal();
         this.taskModal.render();
         return this;
      },
      renderMainView: function(task_id){
         this.mainView.show();
         this.mainView.model = this.tasks.get(task_id);
         this.mainView.render();
         //load main view with the selected task
      },
      openTaskModal: function(){
         this.taskModal.model = new models.Task();
         this.taskModal.open();
      },
      listen: function(){
         this.listenTo(this.taskModal, 'create', this.addTask);
         this.listenTo(this.sidebarView, 'select', this.renderMainView);
         this.listenTo(this.mainView, 'delete', this.deleteTask);
      },
    
      addTask: function(newTaskJSON){
         var that = this;
         this.tasks.create(
            newTaskJSON, 
            {
               wait: true,
               success : function(model){
                  that.tasks.add(model);
               }
            }
         );
      },
      deleteTask: function(id){
         var that = this;
         this.tasks.get(id).destroy({
            wait: true, 
            success: function(model, response){
               that.tasks.remove(model);
               that.mainView.hide();
               
            }
         });
      },
      
      
   });
   return TaskView; 
});