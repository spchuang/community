//Each event in calendar
define('calendarEventItem', function(require){
   var Backbone      = require('backbone'),
       _             = require('underscore'),
       jquery        = require('jquery'),
       Handlebars    = require('handlebars'),
       bootstrap     = require('bootstrap'),
       tpl           = require('text!app/calendar/eventModal.html');
       
   var EventView = Backbone.View.extend({
      id: 'base-modal',
      className: 'modal fade hide',
      template: Handlebars.compile(tpl),
      
      events: {
         'hidden.bs.modal': 'hidden'
      },
      
      initialize: function() {
         //_(this).bindAll();
         this.render();
      },
      render: function() {
         this.$el.html(this.template());
         this.$el.modal({show:true}); // dont show modal on instantiation
         
         return this;
      },
      
      show: function() {
         this.$el.modal('show');
      },
      
      hidden: function() {
         this.$el.data('modal', null);
         this.remove();
      },
      

   });
   
   return EventView;
});

//Main calendar logic
define(function (require) {
   var $            = require('jquery'),
       _            = require('underscore'),
       Backbone     = require('backbone'),
       fullcalendar = require('fullcalendar'),
       eventView    = require('calendarEventItem'),
       models       = require('app/calendar/calendarModel');
       
   var CalendarView = Backbone.View.extend({
      el: $("#calendar"), 
      initialize: function(options){
         _.bindAll.apply(_, [this].concat(_.functions(this)));
         
         //can't use this.events
         this.evts =  new models.EventCollection({communityId: options.communityId});  
         this.listenTo(this.evts, 'reset', this.addAll);
         this.listenTo(this.evts, 'add', this.addOne);
         this.listenTo(this.evts, 'change', this.change);
         this.evts.fetch({reset: true});
         
         this.render();
      },
        
      render: function() {
         this.$el.fullCalendar({
            header: {
               left: 'prev,next today',
               center: 'title',
               right: 'month,agendaWeek,agendaDay',
               ignoreTimezone: false
            },
            selectable: true,
            selectHelper: true,
            editable: true,
            allDayDefault: false,
            select: this.select,
            eventClick: this.eventClick,
            eventDrop: this.eventDropOrResize,
            eventResize: this.eventDropOrResize
         });
         
         this.eventView = new eventView();
      },
      addOne: function(event) {
         this.$el.fullCalendar('renderEvent', event.toJSON());
      },
      addAll: function(){
         this.$el.fullCalendar('addEventSource', this.evts.toJSON());
      },
      change: function(event) {
         var fcEvent = this.$el.fullCalendar('clientEvents', event.get('id'))[0];
         fcEvent.title = event.get('title');
         fcEvent.color = event.get('color');
         this.$el.fullCalendar('updateEvent', fcEvent);
      }, 
      
      select: function(startDate, endDate) {
         console.log("SELECT");
         var eventView = new EventView();
         eventView.collection = this.collection;
         eventView.model = new Event({start: startDate, end: endDate});
       
      
      },
      
      eventClick: function(fcEvent) {
         console.log("CLICK");
         this.eventView.model = this.evts.get(fcEvent.id);
         this.eventView.show();
      },
      eventDropOrResize: function(fcEvent) {
         console.log("DROP OR RESIZE");
         this.collection.get(fcEvent.id).save({start: fcEvent.start, end: fcEvent.end});
         alert(JSON.stringify(fcEvent));
      }
   });
   return CalendarView; 
});