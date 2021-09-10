function validar(){

    event.preventDefault();

    // Lectura del formulario
    var nombre, fecha, email, numero, nif, camiseta, dir, localidad;
    nif = document.getElementById("nif").value;
    nombre = document.getElementById("name").value;
    fecha = document.getElementById("date").value;
    email = document.getElementById("email").value;
    numero = document.getElementById("tlf").value;
    camiseta = document.getElementById("camiseta").value;
    dir = document.getElementById("dir").value;
    localidad = document.getElementById("localidad").value;


    // Expresiones regulares
    var patron_nif, patron_nombre, patron_fecha, patron_email, patron_numero;
    patron_nif = /^((\d{8}[A-Za-z])|([X-Zx-z]\d{7}[A-Za-z]))$/;
    patron_nombre = /^([A-Za-zÁÉÍÓÚñáéíóúÑ\-]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\-\']+[\s])+([A-Za-zÁÉÍÓÚñáéíóúÑ\-]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\-\'])+[\s]?([A-Za-zÁÉÍÓÚñáéíóúÑ\-]{0}?[A-Za-zÁÉÍÓÚñáéíóúÑ\-\'])?$/;
    patron_fecha = /^(((0?[1-9])|([1-2][0-9])|(3[0-1]))\/((0?[1-9])|1[0-2])\/((19[5-9][0-9])|(20((0[0-9])|(1[0-8])))))$/;
    patron_email = /^((\w[\w. %+-]*@(\w[\w-]*\.)+[a-zA-Z]{2,4}))$/;
    patron_numero = /^(\d{9}|(\d{3}(\s\d{2}){3})|(\d{3}(\s\d{3}){2}))$/;
    patron_localidad = /^[A-Za-zÁÉÍÓÚñáéíóúÑ]+$/

    // Comprobación ningun campo vacio
    if(nif === "" || nombre === "" || fecha === "" || email === "" || numero === "" || camiseta === "" || dir === "" || localidad === "" ){
        alert("Rellene todos los campos obligatorios.");
        return false;
    }

    var texto = "Los siguientes campos estan incorrectos: \n";
    var valido = true;

    // Comprobamos nombre
    if (! patron_nombre.test(nombre)){
        texto += "    - Nombre \n";
        valido = false;
    }

    // Comprobamos DNI
    if (! patron_nif.test(nif)){
      texto += "    - DNI \n";
      valido = false;
    }

    // Comprobamos fecha
    fechab = true
    if (! patron_fecha.test(fecha)){
        fechab = false;
    }else{
        leida = fecha.match(patron_fecha);
        var dia, mes, ano;
        dia = parseInt(leida[2]);
        mes = parseInt(leida[6]);
        ano = parseInt(leida[8]);

        if (dia > 31 && ( mes === 1 || mes === 3 || mes === 5 || mes === 7 || mes === 8 || mes === 10 || mes === 12)){
            fechab = false;
        }
        if (dia > 30 && (mes === 4 || mes === 6 || mes === 9 || mes === 11)){
            fechab = false;
        }
        if (mes === 2){
            if (dia > 28 && ano%4 !== 0){
                fechab = false;
            }
            if (dia > 29 && ano%4 === 0 && ano%100 !== 0){
                fechab = false;
            }
        }
    }
    if (!fechab){
      texto += "    - Fecha \n";
      valido = false;
    }

    // Comprobamos la localidad
    if (!patron_localidad.test(localidad)){
      texto += "    - Localidad"
      valido = false;
    }

    // Comprobamos telefono
    if (!patron_numero.test(numero)){
      texto += "    - Teléfono (Si su número de teléfono no es Español ponga seis 0 y en los comentarios ponga su número) \n";
      valido = false;
    }

    // Comprobamos email
    if (! patron_email.test(email)){
        texto += "    - Email \n";
        valido = false;
    }

    // Si todo ha ido bien no entrara
    if (!valido){
      alert(texto);
      return false;
    } else{

      var posicion;
      firebase.database().ref("ParticipantesIV/Inscritos").once("value").then(function(snapshot){
        posicion = snapshot.val();
        var dentro = true;
        if (snapshot.val() >= 60){
            dentro = false;
        }

        // Vemos en que torneos se ha registrado
        var torneos =  "";

        if(document.getElementById("torneo1").checked){
            torneos += "LOL ";
        }

        if(document.getElementById("torneo2").checked){
            torneos += "TFT ";
        }

        if(document.getElementById("torneo3").checked){
            torneos += "Rocket_League ";
        }

        if(document.getElementById("torneo4").checked){
            torneos += "CSGO ";
        }

        if(document.getElementById("torneo5").checked){
            torneos += "Fortnite ";
        }

        if(document.getElementById("torneo6").checked){
            torneos += "FIFA19 ";
        }

        if(document.getElementById("torneo7").checked){
            torneos += "DbD ";
        }
        if(document.getElementById("torneo8").checked){
            torneos += "Tekken ";
        }

        if(document.getElementById("torneo9").checked){
            torneos += "Prop_hunt ";
        }

        if(document.getElementById("torneo10").checked){
            torneos += "APEX ";
        }

        var nuevo;
        firebase.database().ref("ParticipantesIV").once('value').then( function(snapshot) {
          if (snapshot.hasChild(nif)) {
            nuevo = false;
          } else {
            posicion++;
            nuevo = true;
          }

          var nombre_camiseta = "no";
          if (document.getElementById("nombre_camiseta").checked){
            nombre_camiseta = "si";
          }

          // Enviamos a la base de datos
          if (nuevo) {
            // Creamos todos los datos nuevos
            var datos = {
              nombre: nombre,
              fecha_nacimiento: fecha,
              telefono: numero,
              email: email,
              dir: dir,
              localidad: localidad,
              nick: document.getElementById("nick").value,
              clan: document.getElementById("clan").value,
              talla_camiseta: camiseta,
              torneos: torneos,
              sugerencias: document.getElementById("message").value,
              numero_de_inscripcion: posicion,
              nombre_camiseta: nombre_camiseta,
              pagado: "no"
            };

            firebase.database().ref("ParticipantesIV/" + nif).set(datos).then(function(){
              firebase.database().ref("ParticipantesIV/Inscritos").set(posicion).then(function(){
                // Reseteamos
                document.getElementById("form").reset();
                // mostramos alerta
                if (dentro){
                  alert("La inscripción se ha hecho corrrectamente.");
                } else{
                  alert("La inscripción se ha hecho corrrectamente.\nEstas en lista de espera");
                }

              });
            });

          } else {
            // Actualizamos datos sin cambiar el numero de inscripción
            var datos = {
              nombre: nombre,
              fecha_nacimiento: fecha,
              telefono: numero,
              email: email,
              dir: dir,
              localidad: localidad,
              nick: document.getElementById("nick").value,
              clan: document.getElementById("clan").value,
              talla_camiseta: camiseta,
              torneos: torneos,
              nombre_camiseta: nombre_camiseta,
              sugerencias: document.getElementById("message").value,
              pagado: "no"
            };
            firebase.database().ref("ParticipantesIV/" + nif).update(datos).then(function(){
              // Reseteamos
              document.getElementById("form").reset();
              // mostramos alerta
              alert("Se han actualizado los datos de su inscripción.");
            });
          }
        });
      });



      return true;
    }

}
