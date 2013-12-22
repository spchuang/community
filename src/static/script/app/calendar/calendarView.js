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
         //_(this).bindAll();
         this.$content = this.$el.find('.modal-body');
         //Options parameter rewrites these default options
         this.options = _.extend({
         	title: null,
         	animate: true,
         	template: this.template
         }, options);
      },
      render: function() {
      	var $el = this.$el,
				 $content = this.$content;

			//Loading the modal with options
      	$el.html(this.options.template(this.options));

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
      	if(!this.isRendered)
      		this.render();
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
      				url: this.options.action.update,
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
      				url: this.options.action,
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
      	this.collection.get(this.options.data.id).destroy({
      		url: this.options.action.delete,
      		wait: true,
      		success: this.close()
      	});
      },
      close: function(event) {
      	this.$el.modal('hide');
      }
      

   });
   
   return EventView;
});

//Main calendar logic
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
         
         //can't use this.events
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
            selectable: true,
            selectHelper: true,
            editable: true,
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
         var calendarEvent = new eventView(
         	{title: 'Add New Event',
         		action: 'http://localhost:5000/api/calendar/new_event?c_id='+this.evts.communityId,
         		data:{
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
         var calendarEvent = new eventView(
         	{title: 'Edit Current Event',
         		action: fcEvent.action,
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
         calendarEvent.model = new Event();
         calendarEvent.open();
      },
      eventDropOrResize: function(fcEvent) {
         console.log("DROP OR RESIZE");
         alert(fcEvent.start);
         this.evts.get(fcEvent.id).save(
         	{start: Date.create(fcEvent.start).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}'), 
         		end: Date.create(fcEvent.end).format('{yyyy}-{MM}-{dd} {hh}:{mm}:{ss}')
         	},

         	{
         		url: fcEvent.action.update,
         		sucess: function(){
         			alert("yes");
         		}
         	}

         );
      }
   });
   return CalendarView; 
});