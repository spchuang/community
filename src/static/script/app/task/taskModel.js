define(function (require) {
   var Backbone  = require('backbone');
       
  
       
   var Task  = Backbone.Model.extend({
   });
       
  
   var TaskCollection = Backbone.Collection.extend({
      initialize: function(options){
         this.communityId = options.communityId;
      },
      model: Task,
      url: function(){
         return 'http://localhost:5000/api/community/'+this.communityId+'/tasks';
      },
      parse: function(response) {
         return response.data;
      }
 
   });

    return {
        Task: Task,
        TaskCollection: TaskCollection
    };

});