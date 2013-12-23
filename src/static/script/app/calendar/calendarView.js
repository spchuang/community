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
      className: 'modal',
      template: Handlebars.compile(tpl),
      
      events: {
      	'click .close'	  : 'close',
      	'click .cancel'  : 'close',
         'click .ok'		  : 'save',
         'click .edit'	  : 'save',
         'click .delete'  : 'destroy'
      },
      
      initialize: function(options) {
         this.$content = this.$el.find('.modal-body');
         //options parameter rewrites these default options
         this.options = _.extend({
         	title: null,
         	animate: true,
         	template: this.template
         }, options);
      },
      render: function() {
      	var $el = this.$el,
				 $content = this.$content;

         console.log(this.model.toJSON());
			//Loading the modal with options
      	$el.html(this.options.template(this.model.toJSON()));

      	if($content.$el){
      		content.render();
      		$el.find('.modal-body').html(content.$el);
      	}

      	if(this.options.animate)
      		$el.addClass('fade');

      	this.isRendered = true;
      	return this;
      },
      open: function() {
      	/*if(!this.isRendered)
      		this.render();*/

      	this.$el.modal('show');
      },
      save: function() {
      	var that = this,
      		$el = this.$el;

      	//Update event
      	if(this.options.exists){
      		this.collection.get(this.options.data.id).save(
      			{
       				name: $el.find('input[name="name"]').val(),
      				start: Date.create($el.find('input[name="start"]').val()).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'),
      				end: Date.create($el.find('input[name="end"]').val()).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'),
      				description: $el.find('input[name="description"]').val()     			
      			},

      			{
      				wait: true,
      				success: function(updatedEvent) {
      					console.log(updatedEvent);
      					that.collection.change(updatedEvent);
      					that.close();
      				}
      			}
      		);
      		//#todo for some reason the success callback is not getting fired
      		that.close();
      	}else{
      	//Create new event
      		this.collection.create(
      			{
      				name: $el.find('input[name="name"]').val(),
      				start: Date.create($el.find('input[name="start"]').val()).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'),
      				end: Date.create($el.find('input[name="end"]').val()).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'),
      				description: $el.find('input[name="description"]').val()
      			},
					{
						wait: true,
						success: function(newEvent) {
      					console.log(newEvent);
                  	that.collection.add(newEvent);
                  	that.close();
               	}
      			}
      		);
      	}
      },
      destroy: function() {
      	this.collection.get(this.options.data.id).destroy({wait: true, success: this.close()});
      },
      close: function(event) {
      	this.$el.modal('hide');
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
      },
      addOne: function(fcEvent) {
         this.$el.fullCalendar('renderEvent', fcEvent.toJSON());
      },
      addAll: function(){
         this.$el.fullCalendar('addEventSource', this.evts.toJSON());
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
      select: function(startDate, endDate) {
         console.log("SELECT");
         var calendarEvent = new eventView({
         	title: 'Add New Event',
         	data:
         	{
         		start: Date.create(startDate).full(), 
         		end: Date.create(endDate).full(), 
         	}
        	});
         calendarEvent.collection = this.evts;
         calendarEvent.model = new Event();
         calendarEvent.open();
      },
      destroy: function(fcEvent) {
      	this.$el.fullCalendar('removeEvents', fcEvent.id);
      },
      eventClick: function(fcEvent) {
         console.log("CLICK");
         //To stop event click from firing, remove this later on, to let user update and delete events
         if(this.evts.communityId == 'all')
         	return;

         //NEED to fix date errors, some reason if end date is not defined, the end date becomes current date.
         //Possibly due to fullcalendar default values need to check. Error on client side. 
         //alert(fcEvent.start);
         //alert(fcEvent.end);
         /*var calendarEvent = new eventView(
         	{title: 'Edit Current Event',
         		exists: true,
         		data:{
         			id: fcEvent.id,
         			name: fcEvent.title, 
         			start: Date.create(fcEvent.start).full(), 
         			end: Date.create(fcEvent.end).full(),
         			description: fcEvent.description,
         		},
        		});
         calendarEvent.collection = this.evts;
         calendarEvent.model = "d";
         calendarEvent.open();*/
         this.calendarEvent.open();
         this.calendarEvent.model = this.evts.get(fcEvent.id);
         this.calendarEvent.render();
      },
      eventDropOrResize: function(fcEvent) {
         console.log("DROP OR RESIZE");
         var calendarEvent = new eventView(
         	{title: 'Edit Current Event',
         		exists: true,
         		data:{
         			id: fcEvent.id,
         			name: fcEvent.title, 
         			start: Date.create(fcEvent.start).full(), 
         			end: Date.create(fcEvent.end).full(),
         			description: fcEvent.description,
         		},
        		});
         calendarEvent.collection = this.evts;
         calendar
         //calendarEvent.model = new Event();
         calendarEvent.render();
         calendarEvent.save();
      }
   });
   return CalendarView; 
});