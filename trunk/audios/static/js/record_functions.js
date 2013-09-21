var attempts = 0;
var volumen = new Array();
var status = "Setup";

function setup() {
  $(view.tabs).tabs({ 
    fx:[ { width: 'toggle', opacity: 'toggle' }, 
         { opacity: 'toggle' }]  });

  $(view.dialogModal).dialog({
    modal: true,
    height:240,
    weight:100,
  });

  Wami.setup("wami");

  $(view.runners).runner({
    milliseconds: true
  });

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

  $(view.spinners).hide();

  //log
  attempts = attempts + 1;
  volumen = new Array();
  _writeLog("Record");

  var me = this;

  //Wami.startRecording("http://localh0st:8000/audios/wamihandler2/?name_test="+id_test);
  var startfn = function() { 
    $(view.spinners).hide();

    console.debug("Grabando"); 

    sleep1000Rec = function( part, id_test ) {
      if (part == 0) {
          setTimeout( function() { sleep1000Rec( 1, id_test ); }, 1000 );
      } else if( part == 1 ) {
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

        $(view.record).each( function() { $(this).hide() });
        $(view.stop).each( function() { $(this).show() });
        $(view.stop).each( function() { $(this).prop("disabled", false) });
        $(view.play).each( function() { $(this).show() });
        $(view.play).each( function() { $(this).prop("disabled", true) });

        $('.runner[word-id="'+id_test+'"]').runner({
          milliseconds: true
        });    
        $('.runner[word-id="'+id_test+'"]').runner("start");
      }
    }
    
    sleep1000Rec(0, id_test);
  };
  
  var finishedfn = function() { 
    console.debug("Fin grabacion"); 
    console.debug("El volumen fue: "+volumen);

    var res = checkFilters(volumen);
    console.debug('checkFilters: '+res);
    $(view.status).html('Estado: '+res);

    _writeLog("Record volume saved", volumen);
    _writeLog("Record status: "+res);

    checkSaturation = null;
    $(view.saturation).html("Nivel del micrófono:");

    $(view.stop).each( function() { $(this).hide() });
    $(view.record).each( function() { $(this).show() });
    $(view.record).each( function() { $(this).prop("disabled", false) });
    $(view.play).each( function() { $(this).show() });
    $(view.play).each( function() { $(this).prop("disabled", false) });

    $(view.record).show();

    var runner = '.runner[word-id="'+id_test+'"]';
    $(runner).runner('stop');
    $(runner).runner('reset');
    
    $(view.nextProduct).each( function() { $(this).prop("disabled", false) });

    $(view.spinners).hide();
  };

  Wami.startRecording("http://elgatoloco.no-ip.org/audios/wamihandler2/?name_test="+id_test+"&attempts="+attempts,
    Wami.nameCallback(startfn),
    Wami.nameCallback(finishedfn)
  );
}

function play(id_test) {

  $(view.spinners).show();

  //log
  _writeLog("Play");

  //Wami.startPlaying("http://localh0st:8000/audios/wamihandler2/?name_test="+id_test);

  var startfn = function() { 

    $(view.spinners).hide();

    console.debug("Reproduciendo"); 

    $(view.status).html('Estado: Reproduciendo');

    $(view.play).each( function() { $(this).hide() });
    $(view.stop).each( function() { $(this).show() });
    $(view.stop).each( function() { $(this).prop("disabled", false) });
    $(view.record).each( function() { $(this).show()});
    $(view.record).each( function() { $(this).prop("disabled", true) });
    $(view.nextProduct).each( function() { $(this).prop("disabled", true) });

    var runner = '.runner[word-id="'+id_test+'"]';
    $(runner).runner("reset");
    $(runner).runner({
      milliseconds: true
    });
    $(runner).runner("start");

  };

  var me = this;

  var finishedfn = function() { 

    console.debug("Fin Reproduccion"); 
    me.stop(id_test);

    checkSaturation = null;
    $(view.saturation).html("Nivel del micrófono:");
    $(view.status).html('Estado: Parado');

    $(view.stop).each( function() { $(this).hide() });
    $(view.record).each( function() { $(this).show() });
    $(view.record).each( function() { $(this).prop("disabled", false) });
    $(view.play).each( function() { $(this).show() });
    $(view.play).each( function() { $(this).prop("disabled", false) });

    $(view.record).show();

    var runner = '.runner[word-id="'+id_test+'"]';
    $(runner).runner('stop');
    $(runner).runner('reset');
    
    $(view.nextProduct).each( function() { $(this).prop("disabled", false) });

    $(view.spinners).hide();
  };

  Wami.startPlaying("http://elgatoloco.no-ip.org/audios/wamihandler2/?name_test="+id_test+"&attempts="+attempts,
    Wami.nameCallback(startfn), 
    Wami.nameCallback(finishedfn)
  );
}

function stop(id_test) {

  console.debug("Apretamos stop");

  var prevStatus = status;

  //log
  _writeLog("Stop");

  $(view.spinners).show();

  sleep1000Stop = function( part, id_test ) {
    if( part == 0 ) {
      setTimeout( function() { sleep1000Stop( 1, id_test ); }, 1000 );

    } else if( part == 1 ) {

      if( prevStatus === "Record"){

        Wami.stopRecording();

      } else if (prevStatus === "Play" ) {
        
        Wami.stopPlaying();
      
      }
    }
  }
  
  sleep1000Stop(0, id_test);
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