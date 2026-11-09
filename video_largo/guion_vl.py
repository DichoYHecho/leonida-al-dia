"""Guion completo del vídeo largo de «Leónida al Día»: hook, 20 curiosidades y cierre.

Cada bloque: id, num (número de curiosidad o None), titulo (rótulo arriba a la izquierda), overlay (rótulo grande
del hook), texto (lo que se dice y se subtitula), voz (opcional: cómo se escribe para la voz si hace falta una
grafía especial), planos (trozos de trozos.csv y trozos_vl.csv, en orden) y original (trozo con su sonido original).
"""

BLOQUES = [
    {"id": "hook", "num": None, "titulo": "", "overlay": "TIRAR LA BASURA|= MEJOR REPUTACIÓN",
     "texto": ("Rockstar ha tardado trece años en hacer GTA 6. Trece. Y entre todo lo que han metido, hay un "
               "detalle que me tiene obsesionado: en este juego puedes mejorar tu reputación criminal... tirando la "
               "basura al contenedor. Sí. Has oído bien. Pero eso es lo de menos. En este vídeo te cuento 20 "
               "curiosidades de GTA 6 que casi nadie conoce: los nuevos coches, la policía que te recuerda la cara, "
               "el perro más importante de la historia de los videojuegos... y, al final, las tres cosas que Rockstar "
               "todavía no se ha atrevido a contar. Empezamos."),
     "planos": ["Lanz_Paseo", "Lanz_Descapotable", "T1_Autopista", "Mirada_Skyline_Azotea", "Lanz_Playa", "T1_Neones",
                "Mirada_Autopista_1", "Lanz_Balcon", "T2_Jason_Conduce", "Mirada_Descapotable_1", "Lanz_Moto_Salto",
                "Mirada_Calles_2", "T1_Coches_Noche", "VL_Perro_Caricia", "VL_Poli_2", "VL_Disco_2"]},
    {"id": "c01", "num": 1, "titulo": "EL HERMANO MAYOR", "overlay": "",
     "texto": ("Curiosidad número uno. Para entender GTA 6 hay que mirar a su hermano mayor. GTA 5 hizo más de 800 "
               "millones de dólares en su primer día. En un día. Y mil millones en solo tres, algo que ninguna "
               "película ni ningún juego había conseguido tan rápido: Avatar, por ejemplo, tardó 17 días. Hoy GTA 5 "
               "ha vendido más de 230 millones de copias. Y GTA 6 tiene que superar eso. Ni presión ni nada."),
     "planos": ["Mirada_Vista_Aerea", "T1_Playa_Aerea", "Lanz_Cartel_Keys", "Mirada_Atardecer", "T1_Noche_Aerea",
                "Mirada_Puerto", "T1_Letras_Vice", "VL_Joyeria", "Mirada_Autopista_2", "T1_Neones"]},
    {"id": "c02", "num": 2, "titulo": "TRECE AÑOS", "overlay": "",
     "texto": ("Número dos: trece años de espera. GTA 5 salió en septiembre de 2013. GTA 6 sale en noviembre de "
               "2026. Hay gente que ha nacido, ha empezado el colegio y se ha sacado el carné de conducir mientras "
               "esperábamos. Por el camino se retrasó dos veces: iba a salir en 2025, luego el 26 de mayo de 2026, y "
               "al final: el 19 de noviembre. El 26 de mayo, por cierto, Rockstar no dijo ni mu, y los fans se "
               "cabrearon bastante. Esta vez, el jefe de Take-Two ha descartado otro retraso."),
     "planos": ["T2_Mar_Atardecer", "Lanz_Marina", "Mirada_Playa", "T2_Cayos_Aereo", "Mirada_Paracaidas",
                "T2_Gimnasio_Playa", "T1_Puente_Cayos", "Mirada_Moto_Calle", "T2_Casa_Pilotes", "Mirada_Skyline_Noche"]},
    {"id": "c03", "num": 3, "titulo": "EL TRÁILER QUE SE COLÓ", "overlay": "",
     "texto": ("Número tres: el tráiler que se coló. Rockstar tenía previsto publicar el primer tráiler el 5 de "
               "diciembre de 2023. Pero se filtró en redes, y la compañía lo subió trece horas antes, con un "
               "mensaje: nuestro tráiler se ha filtrado, mira el de verdad en YouTube. Resultado: unos 90 millones "
               "de visualizaciones en 24 horas, récord Guinness del vídeo no musical más visto en un día, y se llevó "
               "por delante a MrBeast. Noventa segundos de vídeo y un récord que MrBeast parecía tener blindado."),
     "voz": ("Número tres: el tráiler que se coló. Rockstar tenía previsto publicar el primer tráiler el 5 de "
             "diciembre de 2023. Pero se filtró en redes, y la compañía lo subió trece horas antes, con un "
             "mensaje: nuestro tráiler se ha filtrado, mira el de verdad en YouTube. Resultado: unos 90 millones "
             "de visualizaciones en 24 horas, récord Guinness del vídeo no musical más visto en un día, y se llevó "
             "por delante a Míster Bist. Noventa segundos de vídeo y un récord que Míster Bist parecía tener "
             "blindado."),
     "planos": ["T1_Autopista", "T1_Playa_Aerea", "T1_Humedal", "T1_Lancha_Rapida", "T1_Coches_Noche", "T1_Camioneta",
                "T1_Noche_Aerea", "T1_Neones", "T1_Puente_Cayos", "T1_Letras_Vice"]},
    {"id": "c04", "num": 4, "titulo": "475 MILLONES", "overlay": "",
     "texto": ("Número cuatro: el récord de los récords. El segundo tráiler, en mayo de 2025, se llevó 475 millones "
               "de visualizaciones en 24 horas, sumando todas las plataformas, según Rockstar. El de Deadpool y "
               "Lobezno, que era el campeón, tuvo 365 millones. Y Guinness ya lo recoge en su edición Gamer 2027. "
               "Para que te hagas una idea: más visualizaciones en un día que habitantes tiene la Unión Europea."),
     "planos": ["T2_Cayos_Aereo", "T2_Casa_Pilotes", "T2_Brian", "T2_Jason_Tejado", "T2_Casa_Aerea",
                "T2_Jason_Conduce", "T2_Autopista", "T2_Gimnasio_Playa", "T2_Muelle_Atardecer", "T2_Mar_Atardecer"]},
    {"id": "c05", "num": 5, "titulo": "CUANDO NETFLIX SE CAYÓ", "overlay": "",
     "texto": ("Número cinco: cuando Netflix se cayó. El 27 de agosto Rockstar estrenó una mirada extendida de "
               "GTA 6, unos 26 minutos de juego, primero en Netflix. Fue la primera vez que Netflix estrenaba algo "
               "así. Entró tanta gente a la vez que el servicio falló un rato. En cuatro días: 31,1 millones de "
               "visualizaciones, número uno en 87 de los 93 países que mide Netflix. Y el tráiler de lanzamiento, "
               "del 15 de octubre, ya iba por 51 millones a los cuatro días."),
     "planos": ["Mirada_Jason_Calle", "Mirada_Jason_Patio", "Mirada_Terraza", "Mirada_Azotea", "Mirada_Jason_y_Lucia",
                "Mirada_Logo", "Lanz_Descapotable", "Lanz_Paseo", "Lanz_Balcon", "Mirada_Vista_Aerea"]},
    {"id": "c06", "num": 6, "titulo": "EL MAPA", "overlay": "",
     "texto": ("Número seis: el tamaño. Rockstar le dijo al New York Times que el mapa de GTA 6 es tres veces más "
               "grande que el de Red Dead Redemption 2. Y como el de GTA 5 era algo mayor que el de Red Dead, las "
               "cuentas salen: entre dos y tres veces el último GTA. Leonida es básicamente la Florida de Rockstar: "
               "ciudad, cayos, pantanos y hasta un parque nacional. Y según un informe de Edge, no hace falta "
               "avanzar mucho en la historia para empezar a explorarlo."),
     "planos": ["Mirada_Vista_Aerea", "T1_Humedal", "Mirada_Hidrodeslizador", "Mirada_Buceo", "T2_Cayos_Aereo",
                "Mirada_Motocross", "Lanz_Cartel_Keys", "Mirada_Skyline_Noche", "T1_Puente_Cayos", "Mirada_Atardecer"]},
    {"id": "c07", "num": 7, "titulo": "LO QUE HAY DENTRO", "overlay": "",
     "texto": ("Número siete: lo que hay dentro. Rockstar presume más de la densidad que del tamaño. Los edificios "
               "por dentro tienen mucho más detalle que en Los Santos, y hay más tráfico y más gente por la calle. "
               "En una escena, Jason y Lucía cruzan una discoteca tan llena que parece el metro a las ocho de la "
               "mañana. Es un detalle pequeño, sí. Pero es Rockstar: los detalles pequeños son su religión."),
     "planos": ["VL_Azotea_1", "VL_Azotea_2", "VL_Azotea_3", "VL_Disco_1", "VL_Disco_2", "VL_Disco_3", "VL_Disco_4",
                "Mirada_Calles_1", "Mirada_Camiones", "Mirada_Calles_2"]},
    {"id": "c08", "num": 8, "titulo": "LA GENTE", "overlay": "",
     "texto": ("Número ocho: la gente. En la mirada extendida mantienes un botón y eliges qué decirle a cada "
               "persona, como en Red Dead 2. Y, según un informe de la revista Edge, esto no lo ha confirmado "
               "Rockstar, hay unas 600.000 animaciones para que cada peatón reaccione de forma distinta. Hasta mirar "
               "fijamente a alguien demasiado rato puede acabar mal. Así que ya sabes: en Vice City, no mires a "
               "nadie."),
     "planos": ["VL_Mural", "Mirada_Playa", "VL_Azotea_2", "Mirada_Kayak", "Mirada_Jason_Calle", "VL_Atraco_2",
                "T2_Gimnasio_Playa", "VL_Joyeria", "VL_Disco_0"]},
    {"id": "c09", "num": 9, "titulo": "LA VOZ DE LA RADIO", "overlay": "",
     "texto": ("Número nueve: el locutor más famoso de Vice City. Bad Bunny va a estar dentro del juego como "
               "locutor de radio. Rockstar lo anunció el 8 de octubre: presenta Cocoteo FM, la emisora de música "
               "latina, junto a RaiNao. Dentro del juego se llaman El Martillo y La Gata. Sí: el cabeza de cartel de "
               "la Super Bowl de este año va a ser la voz que te hable por la radio mientras robas un coche. Y no "
               "solo en el coche: por primera vez en la saga habrá pódcast a la carta, y podrás escuchar radio y "
               "pódcast también a pie, con auriculares conectados al móvil de Jason y Lucía. Que el Conejo Malo te "
               "hable por la radio mientras huyes de la policía... eso es otro nivel."),
     "planos": ["T1_Coches_Noche", "Mirada_Skyline_Noche", "VL_Negro_1", "VL_Negro_2", "VL_Interior_1",
                "T2_Jason_Conduce", "Lanz_Descapotable", "VL_Interior_2", "T1_Neones"]},
    {"id": "c10", "num": 10, "titulo": "EL PRIMER COCHE", "overlay": "",
     "texto": ("Número diez: el primer coche. En la mirada extendida, el primero en el que se suben Jason y Lucía "
               "es un descapotable alemán de los ochenta. Parece la versión de Rockstar de un BMW Serie 3 clásico, "
               "aunque eso es suposición de la prensa: Rockstar nunca pone marcas reales. También se ve el Dinka "
               "Blista, un clásico de la saga. Y por dentro los coches tienen tanto detalle que podrías pasar la "
               "ITV."),
     "planos": ["Mirada_Descapotable_1", "Mirada_Descapotable_2", "VL_Descap_3", "Mirada_Autopista_2",
                "Mirada_Coche_Clasico", "Mirada_Calles_2", "Mirada_Furgoneta", "VL_Descap_Cayos"]},
    {"id": "c11", "num": 11, "titulo": "CÓMO SE ROBA UN COCHE", "overlay": "",
     "texto": ("Número once: cómo se roba un coche. Hay dos formas: una ganzúa o romper la ventanilla, como toda la "
               "vida. Y luego, ojo. En una escena, Lucía huye de la policía y quema el coche con un cóctel molotov. "
               "Parece que, si no borras tus huellas, la policía va a por ti con más ganas. Es decir: robar un "
               "coche ya no es solo robarlo. Es un trabajo con posventa."),
     "planos": ["Mirada_Jason_Patio", "Mirada_Coche_Clasico", "Mirada_Calles_1", "VL_Poli_Heli", "VL_Fuego",
                "Mirada_Camiones", "T1_Camioneta", "VL_Fuego"]},
    {"id": "c12", "num": 12, "titulo": "CARRERAS PARA TODOS", "overlay": "",
     "texto": ("Número doce: carreras. La mirada extendida enseña una pista de asfalto, otra de tierra y una "
               "carrera callejera que recuerda a esa saga de carreras de Rockstar que lleva siglos dormida. Suma "
               "motos de cross, motos de agua y lanchas. Y hay sucesos aleatorios en carretera, como una grúa que te "
               "bloquea un carril. Tú ibas a 200... y una grúa. Como en la vida real."),
     "planos": ["Mirada_Carrera", "Mirada_Moto_Calle", "Mirada_Motocross", "Mirada_Hidrodeslizador",
                "Mirada_Mar_Atardecer", "Lanz_Moto_Salto", "T1_Lancha_Rapida", "VL_Moto_Agua"],
     "original": "Mirada_Carrera"},
    {"id": "c13", "num": 13, "titulo": "TU COCHE CON VIDA PROPIA", "overlay": "",
     "texto": ("Número trece: tu coche con vida propia. Según Edge, y esto Rockstar no lo ha confirmado, los coches "
               "tendrían indicador de gasolina y estado del motor, y las armas se guardarían en el maletero en vez "
               "de llevarlas siempre encima. Los coches caros podrían incluso llevar un localizador GPS para que la "
               "policía te encuentre. Si es verdad, robar un deportivo va a ser mucho menos fácil de lo que "
               "parece."),
     "planos": ["VL_Negro_1", "VL_Negro_2", "VL_Negro_3", "VL_Negro_4", "T2_Autopista", "T1_Neones",
                "Mirada_Autopista_1", "VL_Interior_1"]},
    {"id": "c14", "num": 14, "titulo": "EL MINIMAPA YA NO TE CHIVA", "overlay": "",
     "texto": ("Número catorce: el minimapa ya no te chiva. ¿Te acuerdas del truco de toda la vida? Te escondías en "
               "un callejón, mirabas el minimapa y esperabas a que se fueran los puntitos azules. Olvídalo. En GTA 6 "
               "los policías no salen en el minimapa: hay un modo, Focus, para localizarlos. Se acabó el chivato de "
               "bolsillo."),
     "planos": ["VL_Poli_1", "VL_Poli_2", "VL_Poli_3", "VL_Poli_Heli", "VL_HUD_Pasillo", "VL_Poli_4"],
     "original": "VL_Poli_2"},
    {"id": "c15", "num": 15, "titulo": "LA POLICÍA TIENE MEMORIA", "overlay": "",
     "texto": ("Número quince: la policía tiene memoria. Debajo de las estrellas salen iconos que te dicen qué sabe "
               "la policía de ti: tu cara, tu ropa, si vas armado, tu coche. Alejarte ya no basta: pueden volver a "
               "reconocerte. Para librarte tienes que cambiar de ropa, de peinado o de coche. Rob Nelson, de "
               "Rockstar North, dijo que también puedes separar a Jason y Lucía. Y la sexta estrella vuelve; en GTA "
               "5 solo había cinco. La policía de Vice City tiene mejor memoria que yo con las contraseñas."),
     "planos": ["VL_Espejo_1", "VL_Espejo_2", "VL_Dormitorio", "VL_Poli_Heli", "VL_Poli_3", "VL_Poli_4", "VL_Poli_1",
                "Mirada_Calles_2"]},
    {"id": "c16", "num": 16, "titulo": "EL PERRO", "overlay": "",
     "texto": ("Número dieciséis: el perro. Al principio de la mirada extendida, Jason se encuentra un perro y el "
               "juego le da tres opciones: regañarlo, acariciarlo o... estudiarlo. Estudiarlo. A un perro. Jason lo "
               "acaricia, sale un iconito de ángel, suena una campanita... y su karma mejora. Poco después, Lucía "
               "huye de un atraco y se lleva karma negativo. Moraleja: puedes atracar una tienda, pero acaricia al "
               "perro."),
     "planos": ["VL_Perro_Acerca", "VL_Perro_Caricia", "VL_Pasillo_Sigue", "Mirada_Jason_Calle", "VL_Mural",
                "Lanz_Paseo", "VL_Atraco_1"],
     "original": "VL_Perro_Caricia"},
    {"id": "c17", "num": 17, "titulo": "LA BASURA", "overlay": "",
     "texto": ("Número diecisiete: la basura. El perfil criminal no te dice si eres bueno o malo, como el honor de "
               "Red Dead. Registra qué clase de delincuente eres. Amenazar a alguien en un atraco es parte del "
               "trabajo, pero disparar sin motivo o destrozarlo todo por diversión puede pesar con el tiempo. Según "
               "Rob Nelson, si te pasas puede afectar a la historia y a los personajes. ¿Y lo contrario? Según los "
               "medios que lo han visto, tirar la basura a la papelera también suma. O sea: atracar un banco, vale. "
               "Pero el envoltorio, a la papelera."),
     "planos": ["Mirada_Jason_Calle", "VL_Perro_Caricia", "VL_Atraco_1", "VL_Atraco_3", "VL_Mural", "Mirada_Calles_1"]},
    {"id": "c18", "num": 18, "titulo": "JASON Y LUCÍA", "overlay": "",
     "texto": ("Número dieciocho: Jason y Lucía. Lucía Caminos es la primera mujer protagonista jugable de un GTA "
               "principal. Su padre le enseñó a pelear casi antes de andar, acabó en la prisión de Leonida por "
               "defender a su familia y salió, según Rockstar, por pura suerte. Jason Duval creció entre timadores "
               "y pasó por el ejército. Al empezar, los dos quieren que lo suyo sea algo romántico. Si acaban juntos "
               "o no, depende de ti. En la mirada extendida, Lucía suelta una frase que lo resume. Y un dato raro: "
               "Rockstar todavía no ha dicho quién les pone la voz."),
     "planos": ["Mirada_Jason_y_Lucia", "Mirada_Terraza", "Mirada_Azotea", "Lanz_Paseo", "Lanz_Descapotable",
                "Lanz_Balcon", "VL_Interior_1", "Portada_Animada"],
     "original": "VL_Frase_Lucia"},
    {"id": "c19", "num": 19, "titulo": "LA FAUNA DE VICE CITY", "overlay": "",
     "texto": ("Número diecinueve: la fauna de Vice City. Cal Hampton se pasa el día en casa espiando las "
               "comunicaciones de la Guardia Costera con cervezas y pestañas privadas abiertas. Ya sabes: ese primo "
               "tuyo que te manda cadenas de WhatsApp. Boobie Ike tiene un imperio de inmobiliaria, club de "
               "striptease y estudio de grabación, y sonríe... hasta que toca hablar de negocios. Su socio, Dre'Quan, "
               "ha fichado a Real Dimez, dos amigas que han convertido amenazar a camellos en carrera de rap. Brian "
               "Heder, contrabandista de los Cayos, dice que ha movido tanta hierba en su avioneta que podría hacer "
               "levitar Leonida. Y Raúl Bautista, atracador de bancos, siempre busca a gente con talento... y sin "
               "miedo."),
     "planos": ["Clip_Cal", "Clip_Brian", "Clip_DreQuan", "Clip_Boobie", "Clip_Real_Dimez", "T2_Brian"]},
    {"id": "c20", "num": 20, "titulo": "QUÉ HACER ADEMÁS DE ROBAR", "overlay": "",
     "texto": ("Número veinte: qué hacer además de robar. En la mirada extendida se ven pesas, buceo, motos de "
               "agua, baloncesto, carreras de cross y hasta salto base. Y atracar una gasolinera o un local de comida "
               "rápida, claro. Hay ropa para todo: tirantes, trajes, vestidos de lentejuelas. Y no es solo "
               "estética: con una policía que te reconoce por la ropa, cambiarte es táctica. En casa, Jason se abre "
               "una cerveza y ve anuncios satíricos en la tele mientras espera a Lucía. Es muy GTA."),
     "planos": ["VL_Baloncesto", "VL_Pesas", "Mirada_Buceo", "Mirada_Mar_Atardecer", "VL_Moto_Agua", "Mirada_Paracaidas",
                "Mirada_Motocross", "VL_Espejo_1", "VL_Nevera", "VL_Tele_1"],
     "original": "VL_Tele_Audio"},
    {"id": "e1", "num": "E1", "total": 3, "titulo": "UN ZOO ENTERO", "overlay": "",
     "texto": ("Y antes de cerrar, como has llegado hasta aquí, tres curiosidades extra de regalo. Extra uno: un zoo "
               "entero. Según la revista Game Informer, GTA 6 tiene más de 170 especies de animales, y algunas nunca se "
               "habían visto en un juego de Rockstar: flamencos, manatíes, pelícanos, caimanes... Como en la Florida de "
               "verdad, hay hasta especies invasoras: iguanas verdes, sapos de caña y monos macacos. Hay animales raros, "
               "otros que hay que descubrir y otros legendarios, y Rockstar no ha querido decir cuáles. Y en una captura "
               "oficial de un bar de los cayos, los fans encontraron a una mujer con una iguana al hombro... y la iguana "
               "parece llevar su propia ropa. Más estilo que yo, la iguana."),
     "voz": ("Y antes de cerrar, como has llegado hasta aquí, tres curiosidades extra de regalo. Extra uno: un zoo "
               "entero. Según la revista Gueim Informer, GTA 6 tiene más de 170 especies de animales, y algunas nunca se "
               "habían visto en un juego de Rockstar: flamencos, manatíes, pelícanos, caimanes... Como en la Florida de "
               "verdad, hay hasta especies invasoras: iguanas verdes, sapos de caña y monos macacos. Hay animales raros, "
               "otros que hay que descubrir y otros legendarios, y Rockstar no ha querido decir cuáles. Y en una captura "
               "oficial de un bar de los cayos, los fans encontraron a una mujer con una iguana al hombro... y la iguana "
               "parece llevar su propia ropa. Más estilo que yo, la iguana."),
     "planos": ["Mirada_Hidrodeslizador", "T2_Cayos_Aereo", "Mirada_Kayak", "Mirada_Buceo", "T1_Puente_Cayos",
                "Mirada_Mar_Atardecer", "Lanz_Marina", "Mirada_Playa"]},
    {"id": "e2", "num": "E2", "total": 3, "titulo": "EL CUERPO CAMBIA", "overlay": "",
     "texto": ("Extra dos: el cuerpo cambia. Según la revista Dazed, si comes de más, Jason y Lucía engordan, y si vas "
               "al gimnasio, se ponen fuertes. Y el pelo: según Rob Nelson, solo te lo puedes cortar o rapar en los pisos "
               "francos. La pareja también hay que cuidarla: la relación mejora si pasan tiempo juntos, jugando al "
               "billar, al minigolf, en kayak... o atracando bancos. Y si ignoras sus mensajes de buenas noches, lo vas a "
               "pagar. Vamos, como en la vida real, pero con más atracos."),
     "voz": ("Extra dos: el cuerpo cambia. Según la revista Déised, si comes de más, Jason y Lucía engordan, y si vas "
               "al gimnasio, se ponen fuertes. Y el pelo: según Rob Nelson, solo te lo puedes cortar o rapar en los pisos "
               "francos. La pareja también hay que cuidarla: la relación mejora si pasan tiempo juntos, jugando al "
               "billar, al minigolf, en kayak... o atracando bancos. Y si ignoras sus mensajes de buenas noches, lo vas a "
               "pagar. Vamos, como en la vida real, pero con más atracos."),
     "planos": ["VL_Pesas", "T2_Gimnasio_Playa", "VL_Espejo_1", "VL_Dormitorio", "Mirada_Jason_y_Lucia",
                "Mirada_Kayak", "VL_Interior_1", "VL_Atraco_1"]},
    {"id": "e3", "num": "E3", "total": 3, "titulo": "UN ESPAÑOL YA LO HA VISTO", "overlay": "",
     "texto": ("Extra tres: un español que ya lo ha visto. En julio, Rockstar invitó a varios creadores a su estudio de "
               "Edimburgo para enseñarles GTA 6 antes que a nadie. Y uno de ellos fue El Rubius, que pasó unas tres horas "
               "viendo el juego. Lo contó en un vídeo el 27 de agosto, el mismo día de la mirada extendida. Con él "
               "estaban creadores de Australia, Brasil e Italia. Así que, si alguien en España sabe ya cómo es GTA 6 de "
               "verdad... es él. Rubius, si nos ves: ¿qué tal el perro?"),
     "planos": ["Mirada_Vista_Aerea", "Mirada_Skyline_Noche", "VL_Mural", "Mirada_Calles_1", "Lanz_Paseo",
                "Mirada_Skyline_Azotea", "Mirada_Puerto", "Mirada_Atardecer"]},
    {"id": "cierre", "num": None, "titulo": "", "overlay": "",
     "texto": ("Y, como te prometí, las tres cosas que Rockstar todavía no ha contado. Uno: el PC. GTA 6 sale en PS5 "
               "y Xbox Series, y de PC no hay nada oficial. La historia dice que GTA 5 tardó 19 meses en llegar al "
               "ordenador, así que paciencia. Dos: GTA Online. Todo el mundo da por hecho que habrá, pero Rockstar "
               "no ha dicho cuándo, y la mirada extendida no enseñó nada del online. Y tres: la hora exacta. El día "
               "es el 19 de noviembre, pero la hora no la ha confirmado Rockstar. Según la ficha de la tienda de "
               "PlayStation, sería a medianoche, hora local. Mientras tanto, a esperar y a ir practicando eso de "
               "tirar la basura en su sitio. Si te ha gustado, suscríbete a Leónida al Día, que cada día hay un dato "
               "nuevo de GTA 6. Y dime en los comentarios: ¿cuál de las 20 curiosidades te ha sorprendido más? Yo, "
               "lo del perro."),
     "planos": ["Lanz_Cartel_Keys", "VL_Hidroavion", "VL_Atardecer_Final", "VL_Lancha_Pareja", "Mirada_Logo",
                "T1_Letras_Vice", "VL_Rotulo_PS5", "VL_Fecha", "Lanz_Marina"]},
]
