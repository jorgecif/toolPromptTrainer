import streamlit as st
import PIL.Image
import spacy
from streamlit_option_menu import option_menu
from streamlit_extras.let_it_rain import rain
import whisper
from tempfile import NamedTemporaryFile
from numerize.numerize import numerize
import prompts



# Variables para guardar datos de sesión

if 'puntaje_mas_alto' not in st.session_state:
    st.session_state.puntaje_mas_alto = 0

if 'puntaje_guardado' not in st.session_state:
    st.session_state.puntaje_guardado = 0
    


# Parámetros
puntaje_mayor = 0





st.set_page_config(
    page_title="Herramientas AI - Qüid Lab",
    page_icon="random",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Parametros NLP
#nlp = spacy.load("en_core_web_lg")
nlp = spacy.load("en_core_web_sm")


# Oculto botones de Streamlit
hide_streamlit_style = """
				<style>
				#MainMenu {visibility: hidden;}

				footer {visibility: hidden;}
				</style>
				"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Funciones
def success():
	rain(
		emoji="🎈",
		font_size=54,
		falling_speed=5,
		animation_length=1, #'infinite'
	)





def adivinar_prompt(prompt_adivinado, prompt_real):
    frase1 = prompt_adivinado
    frase2 = prompt_real
    fra1 = nlp(frase1)
    fra2 = nlp(frase2)
    similitud_frases = fra1.similarity(fra2)
    puntaje_actual = similitud_frases
    return puntaje_actual


# Logo sidebar
image = PIL.Image.open('logo_blanco.png')
st.sidebar.image(image, width=None, use_column_width=None)

with st.sidebar:
    selected = option_menu(
        menu_title="Selecciona",  # required
        options=["Home", "Iniciar", "Créditos"],  # required
        icons=["house", "caret-right-fill", "caret-right-fill","caret-right-fill",
                        "caret-right-fill", "envelope"],  # optional
        menu_icon="upc-scan",  # optional
        default_index=0,  # optional
    )



if selected == "Home":
	st.title("Experimenta con IA - Adivina el prompt")
	st.write("Esta herramienta te permitirá desarrollar habilidades en el arte de la escritura de prompts.\n \n para la generación de imágenes con IA.\n\n\n\n")
	st.write(' ')
	st.write("**Instrucciones:** \n ")


	"""
	* Selecciona iniciar en el menú de la izquierda.
	* Selecciona una imagen de la lista desplegable. Hay 10 imágenes disponibles.
    * Escribe el prompt que creas se utilizó para generar la imagen. Recuerda que debes escribirlo en inglés pues la mayoría de este tipo de herramientas funcionan sólo en este idioma.
	* Haz clic en el botón "Adivinar".
	* Se mostrará un puntaje de acuerdo a la similitud con el prompt real usado para generar la imagen.
		* El primer valor corresponde al puntaje actual 
		* El segundo al valor más alto de todos los intentos realizados. 

		* Las flechas hacia abajo o hacia arriba indicarán si el puntaje ha subido o bajado de acuerdo a los intentos anteriores.
	* Como último recursos se incluye un checkbox que si lo marcas hará que aparezca el prompt real utilizado para generar la imagen.

	

	\n \n \n NOTA: Esta herramienta es un demo experimental y está sujeta a la demanda de uso. 

	"""


if selected == "Iniciar":
		st.title(f"Adivina el prompt")
		col1,col2= st.columns(2)
		imagen_select = col1.selectbox('Selecciona una imagen', prompts.Archivos_actividad1.keys())
		url_imagen_select = prompts.Archivos_actividad1.get(imagen_select)
		image = PIL.Image.open(url_imagen_select)
		col2.image(image, width=None, use_column_width=True)
		prompt_imagen_select = prompts.Actividad1_ListaPrompts.get(imagen_select)
		
		prompt_adivinado = col1.text_input('¿Cuál crees que es el prompt de esta imagen?', " ")
		boton_adivinar = col1.button("Adivinar")

		if boton_adivinar:
			puntaje_actual = adivinar_prompt(prompt_adivinado, prompt_imagen_select)
			diferencia_con_anterior = puntaje_actual - st.session_state.puntaje_guardado
			st.session_state.puntaje_guardado = puntaje_actual
			
			puntaje_mas_alto = st.session_state.puntaje_mas_alto
			diferencia_con_mas_alto = puntaje_actual - puntaje_mas_alto
				
			if puntaje_actual > puntaje_mas_alto:
				success()
				st.session_state.puntaje_mas_alto = puntaje_actual
			st.session_state.puntaje_guardado = puntaje_actual

			col1.metric(
				label="Puntaje actual y diferencia con puntaje anterior: 🌟",
				value=(numerize(puntaje_actual)),
				delta=numerize(diferencia_con_anterior),
			)

			col1.metric(
				label="Puntaje más alto: 🏆",
				value=(numerize(st.session_state.puntaje_mas_alto)),
			)

		#Ver el prompt real
		ver_prompt = st.checkbox('Ver el prompt 🚫(Sólo en caso de emergencia...)🚫')
		if ver_prompt:
			st.write('Prompt real:')
			st.write(prompt_imagen_select)




if selected == "Créditos":
	st.title(f"Seleccionaste la opción {selected}")
	st.write(' ')
	st.write(' ')
	st.subheader("Qüid Lab")
	body = '<a href="https://www.quidlab.co">https://www.quidlab.co</a>'
	linkedin = 'Linkedin: <a href="https://www.linkedin.com/in/jorgecif/">https://www.linkedin.com/in/jorgecif/</a>' 
	twitter = 'Twitter (X): <a href="https://twitter.com/jorgecif/">https://twitter.com/jorgecif/</a>' 
	st.markdown(body, unsafe_allow_html=True)
	st.write('Creado por: *Jorge O. Cifuentes* :fleur_de_lis:')
	st.markdown(linkedin, unsafe_allow_html=True)
	st.markdown(twitter, unsafe_allow_html=True)

	st.write('Email: *jorge@quidlab.co* ')
	st.write("Quid Lab AI tools")
	st.write("Version 1.0")
	st.text("")







