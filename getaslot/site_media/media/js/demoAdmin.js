$(document).ready(function() {


   var $calendar = $('#calendar');
   var id = 10;

   $calendar.weekCalendar({
	  
      timeslotsPerHour : 1,
	  timeFormat: "H:i",
	  use24Hour: true,
      allowCalEventOverlap : false,
      overlapEventsSeparate: false,
      firstDayOfWeek : 1,
	  timeslotHeight: 40,
      businessHours :{start: 8, end: 18, limitDisplay: true },
      daysToShow : 7,
	  
	  height : 
	  
	  function($calendar) {
         return 501;
      },
	  
      eventRender : function(calEvent, $event, schedule) {
		$event.css("backgroundColor", "#e05034");
			if (schedule == true)
				$event.css("backgroundColor", "#cccccc");
			else {
         if (calEvent.end.getTime() < new Date().getTime()) {
			$event.css("backgroundColor", "#e05034");
            $event.find(".wc-time").css({
               "backgroundColor" : "#999",
               "border" : "1px solid #888"
            });
         } 
}
      },
      draggable : function(calEvent, $event) {
         return calEvent.readOnly == false;
      },
      resizable : function(calEvent, $event) {
         return calEvent.readOnly != false;
      },
      eventNew : function(calEvent, $event) {
         var $dialogContent = $("#event_edit_container");
         resetForm($dialogContent);
         var startField = $dialogContent.find("select[name='start']").val(calEvent.start);
         var endField = $dialogContent.find("select[name='end']").val(calEvent.end);
         var nameField = $dialogContent.find("input[name='name']");
         var phoneField = $dialogContent.find("input[name='phone']");


         $dialogContent.dialog({
            modal: true,
            title: "Appointment",
            close: function() {
               $dialogContent.dialog("destroy");
               $dialogContent.hide();
               $('#calendar').weekCalendar("removeUnsavedEvents");
            },
            buttons: {
               save : function() {
                  calEvent.id = id;
                  id++;
                  calEvent.start = new Date(startField.val()*1000);
                  calEvent.end = new Date(endField.val()*1000);
                  calEvent.name = nameField.val();
                  calEvent.phone = phoneField.val();
					
					jQuery.ajax({
						type: "POST",
						url: "add_appointment/1/",
						data: $("#input_form_event").serialize(),
						timeout: (5 * 1000),
						async: true,
						success: function(data) {
							//alert(data);
							$calendar.weekCalendar("removeUnsavedEvents");
							if (data == "OK") {
								$calendar.weekCalendar("updateEvent", calEvent);
							}
						}
					});

                  $dialogContent.dialog("close");
               },
               cancel : function() {
                  $dialogContent.dialog("close");
               }
            }
         }).show();

         $dialogContent.find(".date_holder").text($calendar.weekCalendar("formatDate", calEvent.start));
         setupStartAndEndTimeFields(startField, endField, calEvent, $calendar.weekCalendar("getTimeslotTimes", calEvent.start));

      },
      eventDrop : function(calEvent, $event) {
      },
      eventResize : function(calEvent, $event) {
      },
      eventClick : function(calEvent, $event) {

         if (calEvent.readOnly) {
            return;
         }

         var $dialogContent = $("#event_edit_container");
         resetForm($dialogContent);
         var startField = $dialogContent.find("select[name='start']").val(calEvent.start);
         var endField = $dialogContent.find("select[name='end']").val(calEvent.end);
         var nameField = $dialogContent.find("input[name='name']").val(calEvent.name);
         var phoneField = $dialogContent.find("input[name='phone']");
         phoneField.val(calEvent.phone);

         $dialogContent.dialog({
            modal: true,
            title: "Edit - " + calEvent.name,
            close: function() {
               $dialogContent.dialog("destroy");
               $dialogContent.hide();
               $('#calendar').weekCalendar("removeUnsavedEvents");
            },
            buttons: {
               save : function() {

                  calEvent.start = new Date(startField.val());
                  calEvent.end = new Date(endField.val());
                  calEvent.name = nameField.val();
                  calEvent.phone = phoneField.val();

                  $calendar.weekCalendar("updateEvent", calEvent);
                  $dialogContent.dialog("close");
               },
               "delete" : function() {
                  $calendar.weekCalendar("removeEvent", calEvent.id);
                  $dialogContent.dialog("close");
               },
               cancel : function() {
                  $dialogContent.dialog("close");
               }
            }
         }).show();

         var startField = $dialogContent.find("select[name='start']").val(calEvent.start);
         var endField = $dialogContent.find("select[name='end']").val(calEvent.end);
         $dialogContent.find(".date_holder").text($calendar.weekCalendar("formatDate", calEvent.start));
         setupStartAndEndTimeFields(startField, endField, calEvent, $calendar.weekCalendar("getTimeslotTimes", calEvent.start));
         $(window).resize().resize(); //fixes a bug in modal overlay size ??

      },
      eventMouseover : function(calEvent, $event) {
      },
      eventMouseout : function(calEvent, $event) {
      },
      noEvents : function() {

      },
	data: "../appointments/?admin=1",
	schedule: ""

      
   });

   function resetForm($dialogContent) {
      $dialogContent.find("input").val("");
      $dialogContent.find("textarea").val("");
   }

   function getEventData() {
      var year = new Date().getFullYear();
      var month = new Date().getMonth();
      var day = new Date().getDate();

      return {
         events : [
            {
               "id":1,
               "start": new Date(year, month, day, 12),
               "end": new Date(year, month, day, 13, 00),
               "title":"Lunch with Mike"
            },
            {
               "id":6,
               "start": new Date(year, month, day, 10),
               "end": new Date(year, month, day, 11),
               "title":"I'm read-only",
               readOnly : true
            }

         ]
      };
   }


   /*
    * Sets up the start and end time fields in the calendar event
    * form for editing based on the calendar event being edited
    */
   function setupStartAndEndTimeFields($startTimeField, $endTimeField, calEvent, timeslotTimes) {

      for (var i = 0; i < timeslotTimes.length; i++) {
         var startTime = timeslotTimes[i].start;
         var endTime = timeslotTimes[i].end;
         var startSelected = "";
         if (startTime.getTime() === calEvent.start.getTime()) {
            startSelected = "selected=\"selected\"";
         }
         var endSelected = "";
         if (endTime.getTime() === calEvent.end.getTime()) {
            endSelected = "selected=\"selected\"";
         }
         $startTimeField.append("<option value=\"" + (startTime.getTime()/1000) + "\" " + startSelected + ">" + timeslotTimes[i].startFormatted + "</option>");
         $endTimeField.append("<option value=\"" + (endTime.getTime()/1000) + "\" " + endSelected + ">" + timeslotTimes[i].endFormatted + "</option>");

      }
      $endTimeOptions = $endTimeField.find("option");
      $startTimeField.trigger("change");
   }

   var $endTimeField = $("select[name='end']");
   var $endTimeOptions = $endTimeField.find("option");

   //reduces the end time options to be only after the start time options.
   // $("select[name='start']").change(function() {
   //       var startTime = $(this).find(":selected").val();
   //       var currentEndTime = $endTimeField.find("option:selected").val();
   //       $endTimeField.html(
   //             $endTimeOptions.filter(function() {
   //                return startTime < $(this).val();
   //             })
   //             );
   // 
   //       var endTimeSelected = false;
   //       $endTimeField.find("option").each(function() {
   //          if ($(this).val() === currentEndTime) {
   //             $(this).attr("selected", "selected");
   //             endTimeSelected = true;
   //             return false;
   //          }
   //       });
   // 
   //       if (!endTimeSelected) {
   //          //automatically select an end date 2 slots away.
   //          $endTimeField.find("option:eq(1)").attr("selected", "selected");
   //       }
   // 
   //    });
   /***/
   var getKeys = function(obj){
   var keys = [];
   for(var key in obj){
      keys= keys+ key+ ",";
	   }
	   return keys;
	}
	/*
	function toEvent(id,start,end,title)
		{
			this.id=0;
			this.start=null;
			this.end=null;
			this.title=null;
		}
        $.get( location+"appointments/",  function(data){ 
			var db = eval(data);
			var  i = 0;
			var forCorrectEvent = new Array();
			for (dbsingle in db)
           	{
				forCorrectEvent[i] = new toEvent(dbsingle.pl,dbsingle.fields.starttime,dbsingle.fields.endtime,dbsingle.fields.name);
			} 	
		});
		*/
		
		
		$('#btn1').mouseover(function(n) {
			$("#btn1_child").show();
		}).mouseout(function(n) {
			$("#btn1_child").hide();
		});
		
		
		$calendar.weekCalendar("nextWeek");	
});