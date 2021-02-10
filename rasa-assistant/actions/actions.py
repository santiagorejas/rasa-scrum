# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, FollowupAction

animo = "bien"

class ActionMisTareas(Action):
    def name(self) -> Text:
        return "action_mis_tareas"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Queres saber tus tarea DESDE ACTIONS")
        print('HOLA DESDE LA TERMINAL SERVER')
        entities = print(tracker.latest_message['entities'])
        
        print(entities)

        return []

class ActionSetTemaMencionado(Action):
    def name(self) -> Text:
        return "action_set_tema_mencionado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("tema_mencionado", True)]

class ActionSetNombreDado(Action):
#
    def name(self) -> Text:
        return "action_set_nombre_dado"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        SlotSet("nombre_dado", True)        
        dispatcher.utter_message(text="SE HA DADO EL NOMBRE")

        return [SlotSet("nombre_dado", True)]


### ASIGNACION TAREA

class ValidateNameForm(Action):
    def name(self) -> Text:
        return "pedir_nombre_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slot = "desarrollador"

        if tracker.slots.get(required_slot) is None:
            # The slot is not filled yet. Request the user to fill this slot next.
            return [SlotSet("requested_slot", required_slot)]

        # All slots are filled.
        return [SlotSet("requested_slot", None), SlotSet("nombre_dado", True)]

class ActionAsignarTarea(Action):
    def name(self) -> Text:
        return "action_asignar_tarea"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
    
        message = ""
        tema = "asd"
        desarrollador = tracker.get_slot("desarrollador")
        name = desarrollador.lower()

        if name == "juan":
            message = "primero tenés que asistir al daily scrum, a las 10:00 AM."
            tema = "daily scrum"
        elif name == "ana":
            message = "tenés que definir las user stories."
            tema = "user story"
        else:
            message = "tenés que actualizar el scrum board"
            tema = "scrum board"
        
        dispatcher.utter_message(text=desarrollador + ", " + message)

        return [SlotSet("tema", tema)]

### EXPLICACION TEMA

class ValidateTopicForm(Action):
    def name(self) -> Text:
        return "pedir_tema_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slot = "tema"

        if tracker.slots.get(required_slot) is None:
            # The slot is not filled yet. Request the user to fill this slot next.
            return [SlotSet("requested_slot", required_slot)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionExplicarTarea(Action):
    def name(self) -> Text:
        return "action_explicar_tema"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
    
        tema = tracker.get_slot("tema")
        print(tema)
        message = ""
        encourage_message = ""

        if tema == "user story":
            message = "Una User Story o historia de usuario es una petición que se formula en el lenguaje cotidiano o de negocios a un programa de ordenador en un máximo de dos frases."
        elif tema == "burn down":
            message = "Un diagrama burn down es una representación gráfica del trabajo por hacer en un proyecto en el tiempo. Usualmente el trabajo remanente (o backlog) se muestra en el eje vertical y el tiempo en el eje horizontal."
        elif tema == "dividir tarea":
            message = "El proceso de dividir tareas comienza con un primer análisis y diseño técnico. Ayuda en este caso dibujar los diferentes componentes software y sus relaciones (cómo interactúan entre ellos). Con un diagrama será muy sencillo identificar todas las tareas necesarias para crear los componentes que falten o modificar los existentes y así obtener una nueva funcionalidad."
        elif tema == "scrum team":
            message = "El Equipo Scrum consiste en un Dueño de Producto (Product Owner), el Equipo de Desarrollo (Development Team) y un Scrum Master. Los Equipos Scrum entregan productos de forma iterativa e incremental, maximizando las oportunidades de obtener retroalimentación."
        elif tema == "product owner":
            message = "El Dueño de Producto es el responsable de maximizar el valor del producto resultante del trabajo del Equipo de Desarrollo."
        elif tema == "development team":
            message = "El Equipo de Desarrollo consiste en los profesionales que realizan el trabajo de entregar un Incremento de producto “Terminado” que potencialmente se pueda poner en producción al final de cada Sprint."
        elif tema == "scrum master":
            message = "El Scrum Master es responsable de promover y apoyar Scrum como se define en la Guía de Scrum. Los Scrum Masters hacen esto ayudando a todos a entender la teoría, prácticas, reglas y valores de Scrum."
        elif tema == "scrum board":
            message = "El Scrum Board es el tablero que se utiliza en Scrum como soporte visual. En él se establecen los elementos del backlog que entran en el sprint por cada línea y sus tareas correspondientes necesarias para llegar a fecha término del sprint con la DoD (Definition of Done)."
        elif tema == "scrum artifacts":
            message = "Los artefactos de Scrum representan trabajo o valor en diversas formas que son útiles para proporcionar transparencia y oportunidades para la inspección y adaptación. Los artefactos definidos por Scrum están diseñados específicamente para maximizar la transparencia de la información clave, necesaria para asegurar que todos tengan el mismo entendimiento del artefacto."
        elif tema == "product backlog":
            message = "La Lista de Producto es una lista ordenada de todo lo que se conoce que es necesario en el producto. Es la única fuente de requisitos para cualquier cambio a realizarse en el producto. El Dueño de Producto (Product Owner) es el responsable de la Lista de Producto, incluyendo su contenido, disponibilidad y ordenación."
        elif tema == "sprint backlog":
            message = "El Sprint Backlog o lista de pendientes del sprint, es el conjunto de tareas seleccionadas del product backlog durante el sprint planning para el Sprint actual, es decir, las tareas necesarias para realizar un incremento de producto."
        elif tema == "increment":
            message = "El Incremento es la suma de todos los elementos de la Lista de Producto completados durante un Sprint y el valor de los incrementos de todos los Sprints anteriores."
        elif tema == "etapas scrum":
            message = "En Scrum existen eventos predefinidos con el fin de crear regularidad y minimizar la necesidad de reuniones no definidas en Scrum. Todos los eventos son bloques de tiempo (time-boxes), de tal modo que todos tienen una duración máxima."
        elif tema == "sprint":
            message = "El Sprint es un bloque de tiempo (time-box) de un mes o menos durante el cual se crea un incremento de producto “Terminado” utilizable y potencialmente desplegable"
        elif tema == "sprint planning":
            message = "El trabajo a realizar durante el Sprint se planifica en la Planificación de Sprint. Este plan se crea mediante el trabajo colaborativo del Equipo Scrum completo. La Planificación de Sprint responde a las siguientes preguntas:  ¿Qué puede entregarse en el Incremento resultante del Sprint que comienza? ¿Cómo se conseguirá hacer el trabajo necesario para entregar el Incremento?"
        elif tema == "daily scrum":
            message = "Un daily scrum es una reunión diaria que se realiza durante el sprint. En ella tendrás que responder tres preguntas; ¿Qué hiciste ayer?¿Qué harás hoy?¿Hay impedimentos en tu camino?"
        elif tema == "sprint review":
            message = "El Sprint Review es uno de los cinco eventos de Scrum, y ocurre en el final del Sprint, para inspeccionar el incremento y adaptar el Product Backlog en caso de que sea necesario. Es una gran oportunidad para poder recibir feedback sobre el desarrollo del producto."
        elif tema == "sprint retrospective":
            message = "La Retrospectiva de Sprint es una oportunidad para el Equipo Scrum de inspeccionarse a sí mismo y de crear un plan de mejoras que sean abordadas durante el siguiente Sprint. La Retrospectiva de Sprint tiene lugar después de la Revisión de Sprint y antes de la siguiente Planificación de Sprint."
        else:
            message = "De momento no te puedo explicar ese tema."
        
        if animo == "desconocimiento":
            encourage_message = "Espero que ésta explicación te haya ayudado a entender mejor el tema!"
        elif animo == "desanimo":
            encourage_message = "Espero que la explicación te haya servido. Vos podés!"
        else:
            encourage_message = "Espero que la explicación te haya cambiado de parecer sobre $tema!"

        dispatcher.utter_message(text=message)
        
        if animo != "bien":
            dispatcher.utter_message(text=encourage_message)

        return []

### Sentimientos del desarrollador:

class ActionAnimoDesconocimiento(Action):
    def name(self) -> Text:
        return "action_animo_desconocimiento"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

       dispatcher.utter_message(text="Tranquilo, estoy acá para ayudarte a entender mejor los temas.")

       animo = "desconocimiento"

       return[]

class ActionAnimoDisconformidad(Action):
    def name(self) -> Text:
        return "action_animo_disconformidad"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

       dispatcher.utter_message(text="Poner alguna frase para motivar al usuario.")

       animo = "disconformidad"

       return[]

class ActionAnimoDesanimo(Action):
    def name(self) -> Text:
        return "action_animo_desanimo"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

       dispatcher.utter_message(text="Vos podes " + str(tracker.get_slot("desarrollador")) + "! tenes mucha capacidad!")

       animo = "desanimo"

       return[]

class ActionAnimoMejoraEntendimiento(Action):
    def name(self) -> Text:
        return "action_animo_mejora_entendimiento"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

       dispatcher.utter_message(text="Me alegro mucho " + str(tracker.get_slot("desarrollador")) + "!")
       
       animo = "bien"

       return[]
    

### ------ ejemplos

class ActionDarEjemplo(Action):
    def name(self) -> Text:
        return "action_dar_ejemplo"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:

        message = ""
        tema = tracker.get_slot("tema")

        if tema == "user story":
            message = "COMO usuario QUIERO poder hacer un backup de mi disco rígido PARA proteger mis archivos."
        elif tema == "burn down":
            message = "A continuacion te muestro como sería graficamente: \nhttps://es.scrum-time.com/infobase/media/burn-down-chart-graph-1.png"
        elif tema == "dividir tarea":
            message = "El diagrama para la división de tareas se puede aproximar a un diagrama de flujo de datos. Un ejemplo podría ser éste: \nwww.samuelcasanova.com/wp-content/uploads/2016/11/dividir-en-tareas-una-historia-de-usuario.jpg"
        elif tema == "scrum board":
            message = "Un scrum board se podría ver así: \nhttps://scrumenespanol.files.wordpress.com/2015/09/scrum-taskboard-planificacion-iteracion-final.jpg"
        elif tema == "daily scrum":
            message = "Un miembro del equipo que tiene una tarea asignada de 7 horas de duración. Al llegar a la Daily Scrum le dice al Scrum Master que el día de ayer estuvo haciendo esa tarea durante 5 horas y no se encontró ningún problema. Entonces el Scrum Master refleja esas horas de avance en el burn-down."
        else:
            message = "Lo siento, " + str(tema) + " es un tema más teórico. No te podría ejemplificarlo."
            dispatcher.utter_message(text=message)
            return[]

        mensaje_animo = ""

        if animo == "desconocimiento":
            mensaje_animo = "Espero que el ejemplo te haya ayudado a entender mejor el tema!"
        elif animo == "desanimo":
            mensaje_animo = "Espero que el ejemplo te haga parecer menos aburrido el tema!"
        elif animo == "disconformidad":
            mensaje_animo = "Ánimo! si seguís con dudas te puedo dar más ejemplos"

        
        dispatcher.utter_message(text=message)
        dispatcher.utter_message(text=mensaje_animo)

        return[]