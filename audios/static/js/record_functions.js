//var url = "fabula2.exp.dc.uba.ar"
var url = "elgatoloco.no-ip.org";
//var url = "localhost:8000"

var attempts = 0;
var volumen = new Array();
var status = "Setup";

function setup() {
  $(view.tabs).tabs({ 
    fx:[ { width: 'toggle', opacity: 'toggle' }, 
         { opacity: 'toggle' }]  });

  $(view.dialogModal).dialog({
    modal: true,
    height:740,
    weight:100,
  });

  Wami.setup("wami");

  runner.setupAll();

  $(view.nextProduct).click(function(){ 
    var tabs = $(view.tabs).tabs();
    var selected = tabs.tabs('option', 'selected');
    tabs.tabs('select', selected+1);
  });

  $(view.prevProduct).click(function() {
    var tabs = $(view.tabs).tabs();
    var selected = tabs.tabs('option', 'selected');
    tabs.tabs('select', selected-1);
  });

  $(view.testContador).html("Grabación: 1 de "+(minNumberExperiments));

  //log
  _writeLog("Start");

  $(view.dialogPopUp).css('visibility', 'hidden');
}

function record(id_test) {

  spinners.hide();

  //log
  attempts = attempts + 1;
  volumen = new Array();
  _writeLog("Record");

  var me = this;

  //Wami.startRecording("http://localh0st:8000/audios/wamihandler2/?name_test="+id_test);
  var startfn = function() { 
    spinners.hide();

    console.debug("Grabando"); 

    sleepAndExecute(0, function() {

      $(view.status).html('Estado: Grabando');

        checkSaturation = function() {
          if (Wami !== undefined) {
            var level = Wami.getRecordingLevel();
            console.debug("El volumen es: "+ level);
            $(view.meters).width(level);
            volumen = volumen.concat([level]);

            setTimeout(checkSaturation, 50);
          }
        };
        
        checkSaturation();

        buttons.showStopDisablePlay();
        runner.start(id_test);
    });
  };
  
  var finishedfn = function() { 
    console.debug("Fin grabacion: el volumen fue: "+volumen);

    var res = checkFilters(volumen);
    console.debug('checkFilters: '+res);
    $(view.status).html('Estado: '+res);

    _writeLog("Record volume saved", volumen);
    _writeLog("Record status: "+res);

    checkSaturation = null;
    $(view.saturation).html("Nivel del micrófono:");

    buttons.showRecordShowPlay();

    runner.stop(id_test);

    $(view.nextProduct).each( function() { $(this).prop("disabled", false) });

    spinners.hide();
  };

  Wami.startRecording("http://"+url+"/audios/wamihandler2/?name_test="+id_test+"&attempts="+attempts,
    Wami.nameCallback(startfn),
    Wami.nameCallback(finishedfn)
  );
}

function play(id_test) {

  spinners.show();

  //log
  _writeLog("Play");

  //Wami.startPlaying("http://localh0st:8000/audios/wamihandler2/?name_test="+id_test);

  var startfn = function() { 

    spinners.hide();

    console.debug("Reproduciendo"); 

    $(view.status).html('Estado: Reproduciendo');

    buttons.showStopDisableRecord();
    
    $(view.nextProduct).each( function() { $(this).prop("disabled", true) });

    runner.start(id_test);
  };

  var me = this;

  var finishedfn = function() { 

    console.debug("Fin Reproduccion"); 

    checkSaturation = null;
    $(view.saturation).html("Nivel del micrófono:");
    $(view.status).html('Estado: Parado');

    buttons.showRecordShowPlay();

    runner.stop(id_test);
    
    $(view.nextProduct).each( function() { $(this).prop("disabled", false) });

    spinners.hide();
  };

  Wami.startPlaying("http://"+url+"/audios/wamihandler2/?name_test="+id_test+"&attempts="+attempts,
    Wami.nameCallback(startfn), 
    Wami.nameCallback(finishedfn)
  );
}

function stop(id_test) {

  sleepAndExecute(0, function() {

    console.debug("Apretamos stop");
    
    buttons.disableAll();
    runner.stop(id_test);
    spinners.show();

    var prevStatus = status;

    //log
    _writeLog("Stop");

    if( prevStatus === "Record"){

      Wami.stopRecording();
      $(view.status).html("Estado: Enviando grabación al servidor");

    } else if (prevStatus === "Play" ) {
      
      Wami.stopPlaying();

      console.debug("Fin Reproduccion"); 

      checkSaturation = null;
      $(view.saturation).html("Nivel del micrófono:");
      $(view.status).html('Estado: Parado');

      buttons.showRecordShowPlay();

      runner.stop(id_test);
      
      $(view.nextProduct).each( function() { $(this).prop("disabled", false) });

      spinners.hide();
    }
  });
}

function next_product() {

  attempts = 0;

  //log
  _writeLog("Next");

  $(view.nextProduct).each( function() { $(this).prop('disabled', true) });

  var word_id = $(".wordexp:visible").attr("word-id");
  var name_test = "test-w"+word_id;
  check_test[name_test] = 1;
  var total_test = 1;
  var cant_test_ok = 1;
  $.each(check_test, function(index, value) { 
    total_test = total_test & value; 
    cant_test_ok = (value == 1) ? cant_test_ok + 1 : cant_test_ok;
  });

  $(view.testContador).html("Grabación: "+(cant_test_ok % (minNumberExperiments + 1))+" de "+(minNumberExperiments));

  if (total_test == 1) {
    $(view.confirm).prop('disabled', false);

    $(view.nextProduct).each( function() { $(this).prop("disabled", true) });
    $(view.exit).show();

  } else {    
    if((cant_test_ok % (minNumberExperiments + 1)) == 0){
      //pregunto por si quiere realizar mas grabaciones
      $(view.dialogConfirm).dialog({
        resizable: false,
        height:240,
        weight:100,
        modal: true,
        buttons: {
          "Sí, quiero hacer 5 más": function() {
            $(this).dialog("close");
          },
          "No, terminar": function() {
            document.location.href = '/audios/end/';
            $(this).dialog("close");
          }
        }
      });
      $(".ui-dialog-titlebar").hide();
      $(view.dialogConfirm).show();
    }
  }
}

function previous_product() {

}

/////////////////////////////////////////////////////////////////////////////////////
//Logging

function _writeLog(action, volumen) {

  status = action;

  var speakerId = $(view.speakerId).attr("speakerId");
  var word_id = $(".wordexp:visible").attr("word-id");

  if (volumen === undefined) {

    //log común
    $.post("/audios/writeLog/", {speakerId: speakerId, action: action, wordId: word_id, attempt: attempts});

  } else {
    
    //log guardando el sensado del volumen
    $.post("/audios/writeLogVolume/", {speakerId: speakerId, action: action, wordId: word_id, volumen: volumen.toString(), attempt: attempts});
  }
}

//Buttons
var buttons = {

  showStopDisablePlay: function() {
    $(view.record).each( function() { $(this).hide() });
    $(view.record).each( function() { $(this).prop("disabled", false) });
    $(view.stop).each( function() { $(this).show() });
    $(view.stop).each( function() { $(this).prop("disabled", false) });
    $(view.play).each( function() { $(this).show() });
    $(view.play).each( function() { $(this).prop("disabled", true) });
  },
  showRecordShowPlay: function() {
    $(view.record).each( function() { $(this).show() });
    $(view.record).each( function() { $(this).prop("disabled", false) });
    $(view.stop).each( function() { $(this).hide() });
    $(view.stop).each( function() { $(this).prop("disabled", false) });
    $(view.play).each( function() { $(this).show() });
    $(view.play).each( function() { $(this).prop("disabled", false) });  
  },
  showStopDisableRecord: function() {
    $(view.record).each( function() { $(this).show()});
    $(view.record).each( function() { $(this).prop("disabled", true) });
    $(view.stop).each( function() { $(this).show() });
    $(view.stop).each( function() { $(this).prop("disabled", false) });
    $(view.play).each( function() { $(this).hide() });
    $(view.play).each( function() { $(this).prop("disabled", false) });      
  },
  disableAll: function() {
    $(view.record).each( function() { $(this).prop("disabled", true) });
    $(view.stop).each( function() { $(this).prop("disabled", true) });
    $(view.play).each( function() { $(this).prop("disabled", true) });
  }
}

//Runners
var runner = {
  setupAll: function() {
      $(view.runners).runner({
        milliseconds: true
      });    
  },
  start: function(id_test) {
    var runner = '.runner[word-id="'+id_test+'"]';
    $(runner).runner('reset');
    $(runner).runner({
      milliseconds: true
    });    
    $(runner).runner("start");
  },
  stop: function(id_test) {
    var runner = '.runner[word-id="'+id_test+'"]';
    $(runner).runner('stop');
    $(runner).runner('reset');
  }
}

//Sleep 1000 ms (1 second) and execute
var sleepAndExecute = function(part, funct) {
  if (part == 0) {
    setTimeout( function() { sleepAndExecute(1, funct); }, 1000 );
  } else if( part == 1 ) {
    funct();
  }
}

//Spinners
var spinners = {
  hide: function() {
    $(".spinner").css('visibility', 'hidden');
  },
  show: function() {
    $(".spinner").css('visibility', 'visible');
  }
}

