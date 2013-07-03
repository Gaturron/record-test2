var time_rec = 0;
var recording = 0;

function setup() {
  $( "#tabs").tabs({ 
    fx:[ { width: 'toggle', opacity: 'toggle' }, 
         { opacity: 'toggle' }]  });

  Wami.setup("wami");

  $('.runner').runner({
    milliseconds: false
  });

  $('#next-product').click(function(){ 
    var tabs = $('#tabs').tabs();
    var selected = tabs.tabs('option', 'selected');
    tabs.tabs('select', selected+1);
  });

  $('#previous-product').click(function() {
    var tabs = $('#tabs').tabs();
    var selected = tabs.tabs('option', 'selected');
    tabs.tabs('select', selected-1);
  });

  $('#test-contador').html("Tests: 0 de "+(minNumberExperiments-1));

  //log
  _writeLog("Start");
}

function record(name_test, id_test) {

  //log
  _writeLog("Record");

  recording = 1;

  //Wami.startRecording("http://localh0st:8000/audios/wamihandler2/?name_test="+name_test);
  var startfn = function() { console.debug("Grabando") };
  var finishedfn = function() { console.debug("Fin grabacion") };
  Wami.startRecording("http://elgatoloco.no-ip.org/audios/wamihandler2/?name_test="+name_test+"&id_test="+id_test,
    startfn(),
    finishedfn()
  );

  checkSaturation = function() {
    if (Wami !== undefined) {
      var level = Wami.getRecordingLevel();
      $("#saturation").html("Nivel de grabación: "+level);
      $("#meter").width(level);
      
      setTimeout(checkSaturation, 5);

      if (level > 50) {
        $(".status").html('Estado: Graba devuelta: mucha saturación');
        $("#next-product").each( function() { $(this).prop("disabled", true) });
      }

      if (minVolumenLevel > level) {
        minVolumenLevel = level;
      }
    }
  };
  
  checkSaturation();

  sleep1000Rec = function( part, id_test ) {
    if (part == 0) {
        setTimeout( function() { sleep1000Rec( 1, id_test ); }, 1000 );
    } else if( part == 1 ) {
      $(".status").html('Estado: Grabando');

      $(".record").each( function() { $(this).hide() });
      $(".stop").each( function() { $(this).show() });
      $(".stop").each( function() { $(this).prop("disabled", false) });
      $(".play").each( function() { $(this).show() });
      $(".play").each( function() { $(this).prop("disabled", true) });

      $("#next-product").each( function() { $(this).prop("disabled", false) });

      $('.runner[word-id="'+id_test+'"]').runner({
        milliseconds: false
      });    
      $('.runner[word-id="'+id_test+'"]').runner("start");
    }
  }
  
  sleep1000Rec(0, id_test);
}

function play(name_test, id_test) {

  //log
  _writeLog("Play");

  //Wami.startPlaying("http://localh0st:8000/audios/wamihandler2/?name_test="+name_test);

  var startfn = function() { console.debug("Reproduciendo") };
  var finishedfn = function() { console.debug("Fin Reproduccion") };
  Wami.startPlaying("http://elgatoloco.no-ip.org/audios/wamihandler2/?name_test="+name_test+"&id_test="+id_test,
    startfn(), 
    finishedfn()
  );

  checkSaturation = function() {
    if (Wami !== undefined) {
      var level = Wami.getPlayingLevel();
      console.debug("Nivel de grabación: "+level);
      $("#saturation").html("Nivel de grabación: "+level);
      $("#meter").width(level);
      
      setTimeout(checkSaturation, 5);
    }
  };
  checkSaturation();

  $(".status").html('Estado: Reproduciendo');

  $(".play").each( function() { $(this).hide() });
  $(".stop").each( function() { $(this).show() });
  $(".stop").each( function() { $(this).prop("disabled", false) });
  $(".record").each( function() { $(this).show()});
  $(".record").each( function() { $(this).prop("disabled", true) });

  var me = this;

  var runner = '.runner[word-id="'+id_test+'"]';
  $(runner).runner("reset");
  $(runner).runner({
    stopAt: time_rec * 1000,
    milliseconds: false
  }).on("runnerFinish", function(eventObject, info){
    me.stop(name_test, id_test);
    //$(runner).runner("reset");
  });
  $(runner).runner("start");
}

function stop(name_test, id_test) {

  //log
  _writeLog("Stop");

  var me = this;
  sleep1000Stop = function( part, id_test ) {
    if( part == 0 ) {
      setTimeout( function() { sleep1000Stop( 1, id_test ); }, 1000 );

    } else if( part == 1 ) {

      Wami.stopRecording();
      Wami.stopPlaying();
      
      checkSaturation = null;
      $("#saturation").html("Nivel de grabación: ---");
      $(".status").html('Estado: Parado');

      $(".stop").each( function() { $(this).hide() });
      $(".record").each( function() { $(this).show() });
      $(".record").each( function() { $(this).prop("disabled", false) });
      $(".play").each( function() { $(this).show() });
      $(".play").each( function() { $(this).prop("disabled", false) });

      $(".record").show();

      var runner = '.runner[word-id="'+id_test+'"]';
      $(runner).runner('stop');
      if (me.recording !== 0) { 
        me.time_rec = $(runner).runner('lap');
      }      
      me.recording = 0;
      $(runner).runner('reset');
      
      $("#next-product").each( function() { $(this).prop("disabled", false) });

      $( "#"+name_test ).html("OK");

      //chequeo el ruido ambiente
      if (minVolumenLevel > 20) {
        $(".status").html('Estado: Graba devuelta: mucho ruido ambiente');
        $("#next-product").each( function() { $(this).prop("disabled", true) });         
      }
    }
  }
  
  sleep1000Stop(0, id_test);
}

function next_product() {

  //log
  _writeLog("Finish");

  $('#next-product').each( function() { $(this).prop('disabled', true) });

  var word_id = $(".wordexp:visible").attr("word-id");
  var name_test = "test-w"+word_id;

  check_test[name_test] = 1;
  var total_test = 1;
  var cant_test_ok = 0;
  $.each(check_test, function(index, value) { 
    total_test = total_test & value; 
    cant_test_ok = (value == 1) ? cant_test_ok + 1 : cant_test_ok;
  });

  $( "#test-contador").html("Tests: "+(cant_test_ok % minNumberExperiments)+" de "+(minNumberExperiments-1));

  if (total_test == 1) {
    $("#confirm").prop('disabled', false);

    $("#next-product").each( function() { $(this).prop("disabled", true) });
    $("#exit").show();

  } else {    
    if(cant_test_ok % minNumberExperiments == 0){
      //pregunto por si quiere realizar mas grabaciones
      $("#dialog-confirm").dialog({
        resizable: false,
        height:240,
        weight:100,
        modal: true,
        buttons: {
          "Realizar cinco más": function() {
            $(this).dialog("close");
          },
          "Salir": function() {
            document.location.href = '/audios/end/';
            $(this).dialog("close");
          }
        }
      });
      $("#dialog-confirm").show();
    }
  }
}

function previous_product() {

}

/////////////////////////////////////////////////////////////////////////////////////
//Logging

function _writeLog(action) {
  //log
  var speakerId = $("#speaker_id").attr("speakerId");
  var word_id = $(".wordexp:visible").attr("word-id");
  $.post("/audios/writeLog/", {speakerId: speakerId, action: action, ItemId: word_id});
}