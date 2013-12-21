define(function (require) {
   var $         = require('jquery'),
       Backbone  = require('backbone');
       
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
   
   var PostComment = Backbone.Model.extend({

   });
   
   var PostCommentCollection = Backbone.Collection.extend({
      model: PostComment,
      url: 'http://localhost:5000/api/wall/'
   });
       
   var Post  = Backbone.Model.extend({
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
      
         model: Post,
         
         url: "http://localhost:5000/api/wall/posts?c_id=1",
         parse: function(response) {
            return response.data;
         }
    
      });

    return {
        Post: Post,
        PostCollection: PostCollection
    };

});