//Each event in calendar
define('calendarEventItem', function(require){
   var Backbone      = require('backbone'),
       jquery        = require('jquery'),
       jquery_ui     = require('jquery_ui'),
       fullcalendar  = require('fullcalendar')

   var EventView = Backbone.View.extend({
      el: $('#eventDialog'),
      initialize: function() {
         _.bindAll.apply(_, [this].concat(_.functions(this)))
      },
      render: function() {
        this.$el.dialog({
                modal: true,
                title: (this.model.isNew() ? 'New' : 'Edit') + ' Event',
                buttons: {'Ok': this.save, 'Cancel': this.close},
                open: this.open
            });
 
            return this;
        },
        open: function() {
            this.$('#title').val(this.model.get('title'));
            this.$('#color').val(this.model.get('color'));
        },
        save: function() {
            this.model.set({'title': this.$('#title').val(), 'color': this.$('#color').val()});
            if (this.model.isNew()){
                this.collection.create(this.model, {success: this.close});
            }else{
                this.model.save({}, {success: this.close});
            }
        },
        close: function() {
           this.$el.dialog('close');
        }
   });
   return EventView;
});

//Main calendar logic
define(function (require) {
   var $            = require('jquery'),
       _            = require('underscore'),
       Backbone     = require('backbone'),
       jquery_ui    = require('jquery_ui'),
       fullcalendar = require('fullcalendar'),
       eventView    = require('calendarEventItem'),
       models       = require('app/calendar/calendarModel'),
       $body        = $('body');
   
   var CalendarView = Backbone.View.extend({
        initialize: function(options){
            _.bindAll.apply(_, [this].concat(_.functions(this)))
            this.events =  new models.EventCollection({communityId: options.communityId}); 
            this.events.bind('reset', this.addAll);
            this.events.bind('add', this.addOne);
            this.events.bind('change', this.change);
            this.events.fetch();
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
        },
        addAll: function(){
            this.$el.fullCalendar('addEventSource', this.collection.toJSON());
        },
        select: function(startDate, endDate) {
            var eventView = new EventView();
            eventView.collection = this.collection;
            eventView.model = new Event({start: startDate, end: endDate});
            eventView.render();
            
        },
        addOne: function(event) {
            this.$el.fullCalendar('renderEvent', event.toJSON());
        },
        change: function(event) {
            var fcEvent = this.$el.fullCalendar('clientEvents', event.get('id'))[0];
            fcEvent.title = event.get('title');
            fcEvent.color = event.get('color');
            this.$el.fullCalendar('updateEvent', fcEvent);
        }, 
        eventClick: function(fcEvent) {
            this.eventView.model = this.collection.get(fcEvent.id);
            this.eventView.render();
        },
        eventDropOrResize: function(fcEvent) {
            this.collection.get(fcEvent.id).save({start: fcEvent.start, end: fcEvent.end});
            alert(JSON.stringify(fcEvent));
        }
   });
   return CalendarView; 
});