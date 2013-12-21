define(function (require) {
   var Backbone  = require('backbone');
       
   var PostComment = Backbone.Model.extend({
      parse: function(response, options){
         var item;
         if (options.collection){
            item = response;
         }else{
            item = response.data;
         }
         return item;
      }
   });
   
   var PostCommentCollection = Backbone.Collection.extend({
      model: PostComment,
      url: 'http://localhost:5000/api/wall/',
      parse: function(response) {
         return response.data;
      }
   });
       
   var Post  = Backbone.Model.extend({
      initialize:function(){
      
      },
      parse: function(response, options){
         var item;
         if (options.collection){
            item = response;
         }else{
            item = response.data;
         }
         item.comments = new PostCommentCollection(item.comments);
         return item;
      }
   });
       
  
   var PostCollection = Backbone.Collection.extend({
      initialize: function(options){
         this.communityId = options.communityId;
      },
      model: Post,
      url: function(){
         return 'http://localhost:5000/api/community/'+this.communityId+'/wall/posts';
      },
      parse: function(response) {
         return response.data;
      }
 
   });

    return {
        Post: Post,
        PostCollection: PostCollection
    };

});