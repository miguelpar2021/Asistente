import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance
import pyjokes
import webbrowser
import datetime
import wikipedia


#opciones de voz / idioma
id1 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
id2 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
id3 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'




#escuchar nuestro microfono y delvolver el audio como texto
def transformar_audio_en_texto():

    #Almacenar el reconocedor en una variable
    r = sr.Recognizer()

    #configurar el microfono
    with sr.Microphone() as origen:

        #Tiempo de Espera
        r.pause_threshold =0.8

        #informar que comenzo la grabacion
        print('Ya puedes hablar')

        #Guardar lo que eschuche como audio
        audio= r.listen(origen)

        try:
            # Reconocer el audio utilizando Google
            pedido = r.recognize_google(audio, language='es-ar')

            #Prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            #devolver pedido
            return pedido

        #En caso de que no comprenda
        except sr.UnknownValueError:

            #No comprendio el audio
            print("No se pudo entender el audio")

            #devolver error
            return "Sigo esperando"

        #En caso de no compredio el pedido
        except sr.RequestError:
            print("No pudo resolver el Pedido")

            # devolver error
            return "Sigo esperando"

        #Error inisperado

        except:

            #Prueba de que no compredio el audio
            print('ups, algo ha salido mal')

            #Devolver error
            return "Sigo esperando"


#Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    #Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice',id3)

    #pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


def pedir_dia():

    #crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    #solo dia
    dia_semana= dia.weekday()
    print(dia_semana)

    #Diccionario dia
    calendario = {0:'Lunes',
                  1:'Martes',
                  2:'Miércoles',
                  3:'Jueves',
                  4:'Viernes',
                  5:'Sábado',
                  6:'Domingo'}

    #decir dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


#informar que hora es
def pedir_hora():

    #Variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos'
    print(hora)

    #decir la hora
    hablar(hora)


# funcion saludo inicial
def saludo_inicial():
    # crear variable con datos de hora
    hora = datetime.datetime.now()

    if hora.hour in range(4, 13):
        momento = 'Buen día'
    elif hora.hour in range(13, 20):
        momento = 'Buenas tardes'
    else:
        momento = 'Buenas noches'
    # decir el saludo
    hablar(f'{momento}, soy Helena, tu asistente personal. Por favor, dime '
           f'en que te puedo ayudar')


#Funcion Central
def pedir_cosas():

    #Activo Inicial
    saludo_inicial()


    #Variable para cortar
    comenzar = True

    #loop central
    while comenzar:

        #Activa el micro y guarda en str
        pedido= transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto estoy abriendo Youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir el navegador' in pedido:
            hablar('Claro,estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar("Buscando eso en Wikipedia")
            pedido = pedido.replace('busca en wikipedia','')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice esto: ')
            hablar(resultado)
        elif 'busca en internet' in pedido:
            hablar("Ya estoy en eso")
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif 'reproducir' in pedido:
            hablar('Excelente eleccion, ya lo reprodusco')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera={'apple':'APPL',
                     'amazon':'AMZN',
                     'google':'GOOGL'}
            try:
                accion_buscada=cartera[accion]
                accion_buscada = yfinance.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regulartMarketPrice']
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar("No la he encontrado")
                continue
        elif 'adiós' in pedido:
            hablar("Me voy a descansar, si me necesitas me buscas")
            break


pedir_cosas()