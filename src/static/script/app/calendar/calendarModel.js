define(function (require) {
   var Backbone  = require('backbone');

       
   var Event  = Backbone.Model.extend({
      initialize: function(){

      },
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
       
  
   var EventCollection = Backbone.Collection.extend({
      initialize: function(options){
         this.communityId = options.communityId;
      },
      model: Event,
      url: function(){
         return 'http://localhost:5000/api/calendar/list?c_id='+this.communityId;
      },
      parse: function(response) {
         return response.data;
      }
 
   });


   return {
      Event: Event,
      EventCollection: EventCollection,
   };

});