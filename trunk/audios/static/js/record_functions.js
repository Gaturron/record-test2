var maxLevel = 0;

function setup() {
  $(view.tabs).tabs({ 
    fx:[ { width: 'toggle', opacity: 'toggle' }, 
         { opacity: 'toggle' }]  });

  $(view.dialogModal).dialog({
    modal: true,
  });

  Wami.setup("wami");

  $(view.runners).runner({
    milliseconds: false
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

  $(view.testContador).html("Tests: 0 de "+(minNumberExperiments));

  //log
  _writeLog("Start");

  $(view.dialogPopUp).css('visibility', 'hidden');
}

function record(name_test, id_test) {

  $(view.spinners).hide();

  //log
  _writeLog("Record");

  var me = this;

  //Wami.startRecording("http://localh0st:8000/audios/wamihandler2/?name_test="+name_test);
  var startfn = function() { 
    $(view.spinners).hide();

    console.debug("Grabando"); 

    checkSaturation = function() {
      if (Wami !== undefined) {
        var level = Wami.getRecordingLevel() * multipLevel;
        console.debug("El volumen es: "+ level);
        $(view.meters).width(level);
        
        setTimeout(checkSaturation, 5);

        if (level > maxLevel) {
          maxLevel = level;
        }
      }
    };
    
    checkSaturation();

    sleep1000Rec = function( part, id_test ) {
      if (part == 0) {
          setTimeout( function() { sleep1000Rec( 1, id_test ); }, 1000 );
      } else if( part == 1 ) {
        $(view.status).html('Estado: Grabando');

        $(view.record).each( function() { $(this).hide() });
        $(view.stop).each( function() { $(this).show() });
        $(view.stop).each( function() { $(this).prop("disabled", false) });
        $(view.play).each( function() { $(this).show() });
        $(view.play).each( function() { $(this).prop("disabled", true) });

        $(view.nextProduct).each( function() { $(this).prop("disabled", false) });

        $('.runner[word-id="'+id_test+'"]').runner({
          milliseconds: false
        });    
        $('.runner[word-id="'+id_test+'"]').runner("start");
      }
    }
    
    sleep1000Rec(0, id_test);
  };
  
  var finishedfn = function() { 
    console.debug("Fin grabacion"); 

    if (maxLevel > maxVolumenLevel) {
      $(view.status).html('Estado: Graba devuelta, mucha saturación');
      $(view.nextProduct).each( function() { $(this).prop("disabled", true) });
      maxLevel = 0;
    }

    if (maxLevel < minVolumenLevel) {
      $(view.status).html('Estado: Graba devuelta, volumen muy bajo');
      $(view.nextProduct).each( function() { $(this).prop("disabled", true) });
      maxLevel = 0;
    }
  };

  Wami.startRecording("http://elgatoloco.no-ip.org/audios/wamihandler2/?name_test="+name_test+"&id_test="+id_test,
    Wami.nameCallback(startfn),
    Wami.nameCallback(finishedfn)
  );
}

function play(name_test, id_test) {

  $(view.spinners).show();

  //log
  _writeLog("Play");

  //Wami.startPlaying("http://localh0st:8000/audios/wamihandler2/?name_test="+name_test);

  var startfn = function() { 

    $(view.spinners).hide();

    console.debug("Reproduciendo"); 

    checkSaturation = function() {
      if (Wami !== undefined) {
        var level = Wami.getPlayingLevel() * multipLevel;
        $(view.saturation).html("Nivel de grabación: "+level);
        $(view.meters).width(level);
        
        setTimeout(checkSaturation, 5);
      }
    };
    checkSaturation();

    $(view.status).html('Estado: Reproduciendo');

    $(view.play).each( function() { $(this).hide() });
    $(view.stop).each( function() { $(this).show() });
    $(view.stop).each( function() { $(this).prop("disabled", false) });
    $(view.record).each( function() { $(this).show()});
    $(view.record).each( function() { $(this).prop("disabled", true) });

    var runner = '.runner[word-id="'+id_test+'"]';
    $(runner).runner("reset");
    $(runner).runner({
      milliseconds: false
    });
    $(runner).runner("start");

  };

  var me = this;

  var finishedfn = function() { 
    console.debug("Fin Reproduccion"); 

    var runner = '.runner[word-id="'+id_test+'"]';
    me.stop(name_test, id_test);
  };

  Wami.startPlaying("http://elgatoloco.no-ip.org/audios/wamihandler2/?name_test="+name_test+"&id_test="+id_test,
    Wami.nameCallback(startfn), 
    Wami.nameCallback(finishedfn)
  );
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
      $(view.saturation).html("Nivel de grabación: ---");
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

      $( "#"+name_test ).html("OK");

      //chequeo el ruido ambiente
      if (minVolumenLevel > 20) {
        $(view.status).html('Estado: Graba devuelta: mucho ruido ambiente');
        $(view.nextProduct).each( function() { $(this).prop("disabled", true) });         
      }
    }
  }
  
  sleep1000Stop(0, id_test);
}

function next_product() {

  //log
  _writeLog("Finish");

  $(view.nextProduct).each( function() { $(this).prop('disabled', true) });

  var word_id = $(".wordexp:visible").attr("word-id");
  var name_test = "test-w"+word_id;
  check_test[name_test] = 1;
  var total_test = 1;
  var cant_test_ok = 0;
  $.each(check_test, function(index, value) { 
    total_test = total_test & value; 
    cant_test_ok = (value == 1) ? cant_test_ok + 1 : cant_test_ok;
  });

  $(view.testContador).html("Tests: "+(cant_test_ok % (minNumberExperiments + 1))+" de "+(minNumberExperiments));

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
          "Realizar cinco más": function() {
            $(this).dialog("close");
          },
          "Salir": function() {
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

function _writeLog(action) {
  //log
  var speakerId = $(view.speakerId).attr("speakerId");
  var word_id = $(".wordexp:visible").attr("word-id");
  $.post("/audios/writeLog/", {speakerId: speakerId, action: action, ItemId: word_id});
}