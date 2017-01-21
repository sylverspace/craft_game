

$(document).ready(function(){

var water = 0;
var fish = 0;
var perles = 0;

var wood = 0;
var rarePlants = 0;
var epicWood = 0;

var rock = 0;
var iron = 0;
var gold = 0;

var woodplanks = 0;
var houses = 0;
var workers = 0;
var totalWorkers = 3;

var waterWork = 0; 
var woodWork = 0;
var rockWork = 0;

var waterRate = 50000 ; //3000 - waterWork * 100; //milliseconds 
var woodRate = 50000; 
var rockRate = 50000; 


//INIT Showing Starting ressources
refreshRessources();

//Water collecting Interval
function startCollectWater(){
	collectWater = setInterval(function(){
		water += 1;
		refreshRessources();
	}, waterRate);
}
function stopCollectWater(){
	clearInterval(collectWater);
}
startCollectWater();//Init at 50000 default

//Wood collecting Interval
function startCollectWood(){
	collectWood = setInterval(function(){
		wood += 1;
		refreshRessources();
	}, woodRate);
}
function stopCollectWood(){
	clearInterval(collectWood);
}
startCollectWood();//Init at 50000 default

//Rock collecting Interval
function startCollectRock(){
	collectRock = setInterval(function(){
		rock += 1;
		refreshRessources();
	}, rockRate);
}
function stopCollectRock(){
	clearInterval(collectRock);
}
startCollectRock();//Init at 50000 default





//Craft Woodplanks costs 2 water, 4 wood
$("#craftWoodplanks").click(function(){
	if(water < 2 || wood < 4){//if not enough ressources

		$("#craftWoodplanks").attr("disabled","disabled");
		console.log("Unsufisent fund!");
		
		$(this).parent().children(".requirements").animate({
			color: "red",
			fontSize: "1.2em"
		},200);
		$(this).parent().children(".requirements").animate({
			color: "black",
			fontSize: "1.0em"
		},200);
		$("#craftWoodplanks").removeAttr("disabled");
	}else{
	water -= 2;
	wood -= 4;
	$("#craftWoodplanks").attr("disabled","disabled");
	refreshRessources();
	startWoodplanksProgress(20); // 2 sec
	}
});
//Woodplanks progressbar
function startWoodplanksProgress(tick){
	
	var width = 0;
	var progressBar = $('#woodplanksProgressbar');
	progressBar.width(width);

	$( "#woodplanksProgressbar" ).progressbar({
	      value: width
	    });

	var interval = setInterval(function() {

	    width += 1;

	    progressBar.css('width', width + '%');

	    if (width >= 100) {
	    	woodplanks += 1;
	    	refreshRessources();
	    	width = 0;
	    	progressBar.css('width', width + '%');
	    	document.getElementById('audioChime1').play();
	    	$("#craftWoodplanks").removeAttr("disabled");
	        clearInterval(interval);
	        
	    }
	}, tick);
}



//Craft Houses
$("#craftHouseButton").click(function(){
	if(woodplanks < 4){
		console.log("Unsufisent fund!");
	}else{
	woodplanks -= 4;
	$("#craftHouseButton").attr("disabled","disabled");
	refreshRessources();
	startHouseProgress(50); //5sec
	}
});
//House progressbar
function startHouseProgress(tick){
	
	var width = 0;
	var progressBar = $('#houseProgressbar');
	progressBar.width(width);

	$( "#houseProgressbar" ).progressbar({
	      value: width
	    });

	var interval = setInterval(function() {

	    width += 1;

	    progressBar.css('width', width + '%');

	    if (width >= 100) {
	    	houses += 1;
	    	refreshRessources();
	    	width = 0;
	    	progressBar.css('width', width + '%');
	    	document.getElementById('audioChime1').play();
	    	$("#craftHouseButton").removeAttr("disabled");
	        clearInterval(interval);
	        checkObjective();
	        
	    }
	}, tick);
}



//Craft Workers
$("#craftWorkers").click(function(){
	if(water < 10 || wood < 6){
		console.log("Unsufisent fund!");
	}else if(workers >= totalWorkers){
		console.log("To many workers.");
	}else{
	water -= 10;
	wood -= 6;
	$("#craftWorkers").attr("disabled","disabled");
	refreshRessources();
	startWorkerProgress(80); //80sec
	}
});
//Worker progressbar
function startWorkerProgress(tick){
	
	var width = 0;
	var progressBar = $('#workerProgressbar');
	progressBar.width(width);

	$( "#workerProgressbar" ).progressbar({
	      value: width
	    });

	var interval = setInterval(function() {

	    width += 1;

	    progressBar.css('width', width + '%');

	    if (width >= 100) {
	    	workers += 1;
	    	refreshRessources();
	    	width = 0;
	    	progressBar.css('width', width + '%');
	    	document.getElementById('audioChime1').play();
	    	$("#craftWorkers").removeAttr("disabled");
	        clearInterval(interval);
	        
	    }
	}, tick);
}

//Function to update ressources in status bar
function refreshRessources(){
	$("#water").html(water);
	$("#wood").html(wood);
	$("#rock").html(rock);
	$("#woodplanks").html(woodplanks);
	$("#houses").html(houses);
	$("#workers").html(workers);
	$("#totalWorkers").html(totalWorkers);
}


//WIDGETS_____________________________________________________________________________

//Set timer countdown in seconds with callback
//Hide hours
$('#countdown-1').timeTo({
    seconds: 1200,
    displayHours: false
}, function(){
    alert('Countdown finished');
});

$('#reset-1').click(function() {
    $('#countdown-1').timeTo('reset');
});


//Spinners ____________________________________________
// use $(this).val() to get last. Use ui.value to get next


//Spinner water
$( "#spinnerWater" ).spinner({
  spin: function( event, ui ) {
    if ( ui.value > totalWorkers ) {
      	return false;
    } else if ( ui.value < 0 ) {
      	$( this ).spinner( "value", 0 );
      	return false;
    }

    //ADDING a worker to water
	if ($(this).val() < ui.value){
	    if(workers == totalWorkers){
			return false; //No more workers? Return false
		}
    	workers += 1;
    }else{
    	workers -= 1;
    }
    console.log(ui.value);
    waterWork = ui.value;
    waterRate = 3000 - waterWork * 500; //milliseconds 
    if(ui.value == 0){
    	waterRate = 50000;
    }
    stopCollectWater();
    startCollectWater();
    refreshRessources();

	}
	
});

//Spinner wood
$( "#spinnerWood" ).spinner({
  spin: function( event, ui ) {
    if ( ui.value > totalWorkers ) {
      	return false;
    } else if ( ui.value < 0 ) {
      	$( this ).spinner( "value", 0 );
      	return false;
    }

    //ADDING a worker to wood
	if ($(this).val() < ui.value){
    	if(workers == totalWorkers){
			return false;//No more workers? Return false
		}
    	workers += 1;
    }else{
    	workers -= 1;
    }

    woodWork = ui.value;
    woodRate = 3000 - woodWork * 500; //milliseconds 
    if(ui.value == 0){
    	woodRate = 50000;
    }
    stopCollectWood();
    startCollectWood();
    refreshRessources();

  }
	
});

//Spinner rock
$( "#spinnerRock" ).spinner({
  spin: function( event, ui ) {
    if ( ui.value > totalWorkers ) {
      	return false;
    } else if ( ui.value < 0 ) {
      	$( this ).spinner( "value", 0 );
      	return false;
    }

    //ADDING a worker to rock
	if ($(this).val() < ui.value){
    	if(workers == totalWorkers){
			return false;//No more workers? Return false
		}
    	workers += 1;
    }else{
    	workers -= 1;
    }

    rockWork = ui.value;
    rockRate = 3000 - rockWork * 500; //milliseconds 
    if(ui.value == 0){
    	rockRate = 50000;
    }
    stopCollectRock();
    startCollectRock();
    refreshRessources();
  }
	
});

function checkObjective(){
	if(houses >= 2 && water >= 20){
		$( "#dialog-message" ).dialog({
  			modal: true,
  			buttons: {
    			"Back to Lobby": function() {
      			$( this ).dialog( "close" );
      			//redirect to lobby
    			}
  			}
		});
	}
}

//Objectives_________________________________________________________________

//run checkObjective after building something
function checkObjective(){     
	if(houses >= 2 && water >= 20){
		$( "#dialog-message" ).dialog({
  			modal: true,
  			buttons: {
    			"Back to Lobby": function() {
      			$( this ).dialog( "close" );
      			//redirect to lobby {{ url_for('lobby') }} NOT WORKING YET
    			}
  			}
		});
	}
}




});

