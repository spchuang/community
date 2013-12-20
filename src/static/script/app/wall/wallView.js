/*
   Let's put everything in the same file first...
   TODO:
      1. add comments
      2. create post return new post
      3. create comments return new comments
      4. comment list
*/

define('wallPostCommentItem', function(require){
   var Backbone      = require('backbone'),
       Handlebars    = require('handlebars'),
       tpl           = require('text!app/wall/wallPostCommentItem.html');

   var ItemView = Backbone.View.extend({
      tagName: "li",
      template: Handlebars.compile(tpl),
      events: {
         'click .like'     : 'likeEvt',
      },
      initialize: function() {
         this.listenTo(this.model, 'change', this.render);
      },
      
      render: function() {
         console.log(this.model.toJSON());
         var $oldel = this.$el
             $newel = $(this.template(this.model.toJSON()));
         this.setElement($newel);
         $oldel.replaceWith($newel);
         return this;
      },
      likeEvt: function(){
         console.log("like clicked");
      }
   });
   return ItemView;
});

//wall post item view (single post)
define('wallPostItem', function(require){
   var Backbone      = require('backbone'),
       Handlebars    = require('handlebars'),
       tpl           = require('text!app/wall/wallPostItem.html'),
       commentView   = require('wallPostCommentItem');

   var ItemView = Backbone.View.extend({
      tagName: "div",
      template: Handlebars.compile(tpl),
      events: {
         'click .like'     : 'likeEvt',
         'click .comment'  : 'commentEvt',
         'click #comment_post' : 'makeComment',
      },
      initialize: function() {
         this.comments = this.model.get('comments');
         this.listenTo(this.model, 'change', this.render);
         this.form = this.$("#comment_form");
      },
      
      render: function() {
         var $oldel = this.$el
             $newel = $(this.template(this.model.toJSON()));
         this.setElement($newel);
         $oldel.replaceWith($newel);
         
         this.comments.each(this.addComment, this);   

         return this;
      },
      addComment: function(comment){
         var view = new commentView({ model: comment });
        
         this.$el.find('.comments_list').append( view.render().el );
      },
      likeEvt: function(){
         console.log("like clicked");
      },
      commentEvt: function(){
         console.log("comment clicked");
      },
      makeComment: function(){
         
      }
   });
   return ItemView;
});


define(function (require) {
   var $           = require('jquery'),
       _           = require('underscore'),
       Backbone    = require('backbone'),
       Handlebars  = require('handlebars'),
       postView    = require('wallPostItem'),
       models      = require('app/wall/wallModel'),
       $body       = $('body');
   
      
   //main wall app logic   
   var WallView = Backbone.View.extend({
   
      el: $('#wall'),
      events:{
         'click #create_post' : 'createPost' 
      },
      initialize: function(){
         this.content = this.$("#wall_content");
         this.createForm  = this.$("#create_form");
   
         //create a collection of posts   
         this.posts =  new models.PostCollection();  
         
         this.posts.on('reset', this.addAll, this);
         //get list of wall posts
         this.posts.fetch({reset: true});
         
      },
      render: function() {
         
      },
      addOne: function( post ) {
         var view = new postView({ model: post });
         this.$el.append( view.render().el );
      },
      
      addAll: function() {
         this.posts.each(this.addOne, this);
      },
      createPost: function(){
         
         this.posts.create(
            {body: this.createForm.find('input').val()}, 
            {url: this.createForm.attr('action')}
         );
      }

   });
   return WallView;
      

});