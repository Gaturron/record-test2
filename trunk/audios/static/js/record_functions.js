
function setup() {
  $( "#tabs").tabs({ 
    fx:[ { width: 'toggle', opacity: 'toggle' }, 
         { opacity: 'toggle' }]  });

  Wami.setup("wami");

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

  $('#test-contador').html("Tests: 0 de "+(Object.keys(check_test).length));
}

function record(name_test, id_test) {
  //Wami.startRecording("http://localh0st:8000/audios/wamihandler2/?name_test="+name_test);

  var startfn = function() { console.debug("Grabando") };
  var finishedfn = function() { console.debug("Fin grabacion") };
  Wami.startRecording("http://localhost:8000/audios/wamihandler2/?name_test="+name_test+"&id_test="+id_test,
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
        $("#status").html('Estado: Graba devuelta: mucha saturación');
        $("#next-product").each( function() { $(this).prop("disabled", true) });
      }

      if (minVolumenLevel > level) {
        minVolumenLevel = level;
      }
    }
  };
  
  checkSaturation();

  sleep1000Rec = function( part ) {
    if( part == 0 ) {
        setTimeout( function() { sleep1000Rec( 1 ); }, 1000 );
    } else if( part == 1 ) {
      $("#status").html('Estado: Grabando');

      $(".record").each( function() { $(this).hide() });
      $(".stop").each( function() { $(this).show() });
      $(".stop").each( function() { $(this).prop("disabled", false) });
      $(".play").each( function() { $(this).show() });
      $(".play").each( function() { $(this).prop("disabled", true) });

      $("#next-product").each( function() { $(this).prop("disabled", false) });
    }
  }
  
  sleep1000Rec(0);
}

function play(name_test, id_test) {
  //Wami.startPlaying("http://localh0st:8000/audios/wamihandler2/?name_test="+name_test);

  var startfn = function() { console.debug("Reproduciendo") };
  var finishedfn = function() { console.debug("Fin Reproduccion") };
  Wami.startPlaying("http://localhost:8000/audios/wamihandler2/?name_test="+name_test+"&id_test="+id_test,
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

  $("#status").html('Estado: Reproduciendo');

  $(".play").each( function() { $(this).hide() });
  $(".stop").each( function() { $(this).show() });
  $(".stop").each( function() { $(this).prop("disabled", false) });
  $(".record").each( function() { $(this).show()});
  $(".record").each( function() { $(this).prop("disabled", true) });
}

function stop(name_test) {

  sleep1000Stop = function( part ) {
    if( part == 0 ) {
      setTimeout( function() { sleep1000Stop( 1 ); }, 1000 );

    } else if( part == 1 ) {

      Wami.stopRecording();
      Wami.stopPlaying();
      
      checkSaturation = null;
      $("#saturation").html("Nivel de grabación: ---");

      check_test[name_test] = 1;

      $("#status").html('Estado: Parado');

      $(".stop").each( function() { $(this).hide() });
      $(".record").each( function() { $(this).show() });
      $(".record").each( function() { $(this).prop("disabled", false) });
      $(".play").each( function() { $(this).show() });
      $(".play").each( function() { $(this).prop("disabled", false) });

      $(".record").show();

      $( "#"+name_test ).html("OK");

      var total_test = 1;
      var cant_test_ok = 0;
      $.each(check_test, function(index, value) { 
        total_test = total_test & value; 
        cant_test_ok = (value == 1) ? cant_test_ok + 1 : cant_test_ok;
      });

      $( "#test-contador").html("Tests: "+cant_test_ok+" de "+(Object.keys(check_test).length));

      if(total_test == 1){
        $("#confirm").prop('disabled', false);

        $("#next-product").each( function() { $(this).prop("disabled", true) });
        $("#exit").show();
      }

      //chequeo el ruido ambiente
      if (minVolumenLevel > 20) {
        $("#status").html('Estado: Graba devuelta: mucho ruido ambiente');
        $("#next-product").each( function() { $(this).prop("disabled", true) });         
      }
    }
  }
  
  sleep1000Stop(0);
}
