/*
   Let's put everything in the same file first...
   TODO:

      3. create comments return new comments
      4. comment list
*/

define('wallPostCommentItem', function(require){
   var Backbone      = require('backbone'),
       Handlebars    = require('handlebars'),
       timeago       = require('timeago'),
       tpl           = require('text!app/wall/wallPostCommentItem.html');

   var ItemView = Backbone.View.extend({
      tagName: "li",
      template: Handlebars.compile(tpl),
      events: {
         'click .like'     : 'likeEvt',
      },
      
      render: function() {
         this.$el.html(this.template(this.model.toJSON()));
         //apply time ago
         this.$el.find(".comment_time").timeago();
         return this;
      },
      likeEvt: function(event){
         event.stopPropagation();
         console.log("like clicked");
      }
   });
   return ItemView;
});

//wall post item view (single post)
define('wallPostItem', function(require){
   var Backbone      = require('backbone'),
       Handlebars    = require('handlebars'),
       timeago       = require('timeago'),
       tpl           = require('text!app/wall/wallPostItem.html'),
       commentView   = require('wallPostCommentItem');

   var ItemView = Backbone.View.extend({
      tagName: "div",
      template: Handlebars.compile(tpl),
      events: {
         'click .like'     : 'likeEvt',
         'click .comment'  : 'commentEvt',
         'click #comment_post' : 'commentPost',
      },
      initialize: function() {
         this.comments = this.model.get('comments');
         this.listenTo(this.comments, 'add', this.addComment);
      },
      
      render: function() {
         var $oldel = this.$el
             $newel = $(this.template(this.model.toJSON()));
         this.setElement($newel);
         $oldel.replaceWith($newel);
         
         this.commentForm = this.$("#comment_form");
         this.comments.each(this.addComment, this);   
         
         //apply time ago
         this.$el.find(".post_time").timeago();

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
      commentPost: function(){
         var that = this;
         this.comments.create(
            {body: this.commentForm.find('input').val()}, 
            {
               url: this.commentForm.attr('action'),
               wait: true,
               success : function(newComment){
             
                  that.comments.add(newComment);
               }
            }
         );
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
         this.$content     = this.$("#wall_content");
         this.createForm   = this.$("#create_form");
   
         //create a collection of posts   
         this.posts =  new models.PostCollection();  
         
         this.listenTo(this.posts, 'reset', this.render);
         this.listenTo(this.posts, 'add', this.addOne);
         //get list of wall posts
         this.posts.fetch({reset: true});
         
      },
      render: function() {
         this.addAll();
         return this;
      },
      addOne: function( post ) {
         var view = new postView({ model: post });
         this.$content.prepend( view.render().el );
      },
      
      addAll: function() {
         //print reversely
         _.each(this.posts.last(this.posts.length).reverse(), this.addOne, this);
      },
      createPost: function(){
         var that = this
         this.posts.create(
            {body: this.createForm.find('input[name="body"]').val()}, 
            {
               url: this.createForm.attr('action'), 
               wait: true,
               success : function(newPost){
                  that.posts.add(newPost);
               }
            }
         );

      }

   });
   return WallView;
});