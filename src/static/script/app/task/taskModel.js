define(function (require) {
   var Backbone  = require('backbone');
       
  
       
   var Task  = Backbone.Model.extend({
      
      parse: function(response, options){
         if (options.collection){
            return response;
         }else{
            return response.data;
         }

      },
      toggle: function() {
         //1=done, 0=not finished
         var newStatus = 0;
         if(this.get('status') == 0){
            newStatus = 1;
         }
         this.save({status: newStatus}, {wait:true});
         
         
      },
      validate: function (attrs) {
         
         if(attrs.name == ""){
            return "Task name can't be empty!";
         }
         return '';
      }

      /*
      validate: function(attributes, options) {
         console.log(attributes);
         console.log(options);
         if (typeof(options.error === 'function')) options.error();

      }*/
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
      },
      /*
      add: function(object, options) {
         if (_.isArray(object) || !object.get('errors')) {
           Backbone.Collection.prototype.add.call(this, object, options)
         }
         },
      */
 
   });

    return {
        Task: Task,
        TaskCollection: TaskCollection
    };

});