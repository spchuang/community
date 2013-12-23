//Each event in calendar
define('calendarEventItem', function(require){
   var Backbone      = require('backbone'),
       _             = require('underscore'),
       jquery        = require('jquery'),
       Handlebars    = require('handlebars'),
       bootstrap     = require('bootstrap'),
       sugar			= require('sugar'),
       tpl           = require('text!app/calendar/eventModal.html');
       
   var EventView = Backbone.View.extend({
      className: 'modal fade',
      template: Handlebars.compile(tpl),
      
      events: {
      	'click .close'	  : 'close',
      	'click .cancel'  : 'close',
      	'hidden.bs.modal': 'teardown',
         'click .ok'		  : 'save',
         'click .edit'	  : 'save',
         'click .delete'  : 'destroy'
      },
      
      initialize: function() {
         this.$content = this.$el.find('.modal-body');
      },
      render: function() {
         console.log(this.model);
         var data = {
            name: this.model.get('title'), 
            start: Date.create(this.model.get('start')).full(), 
            end: Date.create(this.model.get('end')).full(),
            description: this.model.get('description'),
            show_delete: this.show_delete
         }
      	this.$el.html(this.template(data));

      	return this;
      },
      
      save: function() {
      	var that = this,
      		$el = this.$el;

         this.model.set({ 
               name: $el.find('input[name="name"]').val(),
               start: Date.create($el.find('input[name="start"]').val()).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'),
               end: Date.create($el.find('input[name="end"]').val()).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'),
               description: $el.find('input[name="description"]').val()
            });

      	//Create new event
      	if(this.model.isNew()){       
            var result = this.collection.create(this.model, 
               {
                  wait: true,
                  success: function(newEvent) {
                     console.log(newEvent);
                     //Add isn't getting auto fired on create, something to do with wait, but need request to add to calendar
                     that.collection.add(newEvent);
                     that.close();
                  }
               });
      	}else{
      	//Update event
      		this.model.save({}, 
               {
                  wait: true,
      				success: function(updatedEvent) {
      					console.log(updatedEvent);
      					that.close();
      				}
      			}
      		);
      		//#todo for some reason the success callback is not getting fired
      		that.close();
      	}
      },
      destroy: function() {
      	this.model.destroy({wait: true, success: this.close()});
      },
      open: function() {
      	this.$el.modal('show');
      },
      close: function(event) {
      	this.$el.modal('hide');

      },
      teardown: function(event){
      	this.show_delete = false
      }

   });
   
   return EventView;
});

define(function (require) {
   var $            = require('jquery'),
       _            = require('underscore'),
       Backbone     = require('backbone'),
       fullcalendar = require('fullcalendar'),
       sugar		  = require('sugar'),
       eventView    = require('calendarEventItem'),
       models       = require('app/calendar/calendarModel');
       
   var CalendarView = Backbone.View.extend({
      el: $("#calendar"), 
      initialize: function(options){
         _.bindAll.apply(_, [this].concat(_.functions(this)));
         
         this.evts =  new models.EventCollection({communityId: options.communityId});  
         this.listenTo(this.evts, 'reset', this.addAll);
         this.listenTo(this.evts, 'add', this.addOne);
         this.listenTo(this.evts, 'change', this.change);
         this.listenTo(this.evts, 'destroy', this.destroy);
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
            selectable: (this.evts.communityId == 'all') ? false : true,
            selectHelper: (this.evts.communityId == 'all') ? false : true,
            editable: (this.evts.communityId == 'all') ? false : true,
            allDayDefault: false,
            select: this.select,
            eventClick: this.eventClick,
            eventDrop: this.eventDropOrResize,
            eventResize: this.eventDropOrResize
         });
         
         this.calendarEvent = new eventView();
         this.calendarEvent.collection = this.evts;
      },
      addAll: function(){
         this.$el.fullCalendar('addEventSource', this.evts.toJSON());
      },
      addOne: function(event) { 
         this.$el.fullCalendar('renderEvent', event.toJSON());
      },
      change: function(event) {
         var fcEvent = this.$el.fullCalendar('clientEvents', event.get('id'))[0];
         fcEvent.title = event.get('title');
         fcEvent.start = event.get('start');
         fcEvent.end = event.get('end');
         fcEvent.description = event.get('description');
         fcEvent.color = event.get('color');
         this.$el.fullCalendar('updateEvent', fcEvent);
      },     
      destroy: function(fcEvent) {
      	this.$el.fullCalendar('removeEvents', fcEvent.id);
      }, 
      select: function(startDate, endDate) {
         console.log("SELECT");
         this.calendarEvent.model = new models.Event({title: "", start: startDate, end: endDate, description: ""});
         this.calendarEvent.render();
         this.calendarEvent.open();
      },
      eventClick: function(fcEvent) {
         console.log("CLICK");
         
         //To stop event click from firing, remove this later on, to let user update and delete events
         if(this.evts.communityId == 'all')
         	return;

         this.calendarEvent.model = this.evts.get(fcEvent.id);
         this.calendarEvent.show_delete = true;
         this.calendarEvent.render();
         this.calendarEvent.open();
      },
      eventDropOrResize: function(fcEvent) {
         console.log("DROP OR RESIZE");
         this.calendarEvent.model = this.evts.get(fcEvent.id);
         this.calendarEvent.model.set({start: fcEvent.start, end: fcEvent.end});
         this.calendarEvent.render();
         this.calendarEvent.save();
      }
   });
   return CalendarView; 
});