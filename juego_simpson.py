import pygame
import sys
import time
import cv2
import numpy as np
from pygame import mixer

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
ANCHO = 800
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("CompuGlobalHyperMegaNet")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Fuentes
fuente = pygame.font.Font(None, 32)
fuente_grande = pygame.font.Font(None, 64)
fuente_dialogo = pygame.font.Font(None, 24)  # Nueva fuente más pequeña para los diálogos

# Cargar y redimensionar imágenes
fondo = pygame.image.load("fondo.jpeg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

homer = pygame.image.load("homer.png")
homer = pygame.transform.scale(homer, (150, 225))  # Ajusta estos valores según necesites

comic_book_guy = pygame.image.load("comic_book_guy.png")
comic_book_guy = pygame.transform.scale(comic_book_guy, (150, 225))  # Ajusta estos valores según necesites

def dibujar_borde(superficie, rect, color, grosor=4):
    pygame.draw.rect(superficie, color, rect, grosor)

# Diálogos y opciones
dialogos = [
    {
        "personaje": "Comic Book Guy",
        "texto": "...",
        "opciones": [
            ("¡Bienvenido a internet buen hombre!", False),
            ("Bienvenido a internet", False),
            ("¡Bienvenido a internet, amigo! ¿En qué puedo ayudarte?", True)
        ]
    },
    {
        "personaje": "Comic Book Guy",
        "texto": "Estoy interesado en actualizar mi conexión a internet de 28.8 kilobaudios a una línea T1 de fibra óptica de 1.5 megabits. ¿Podrás proporcionar un enrutador IP compatible con la configuración de mi LAN Ethernet de anillo con token?",
        "opciones": [
            ("Sí, tenemos varios modelos disponibles.", False),
            ("...", True),
            ("¿Qué es un enrutador IP?", False)
        ]
    },
    {
        "personaje": "Homer Simpson",
        "texto": "...",
        "opciones": [
            ("...", True),
            ("(Tose...)", False),
            ("Me voy...", False)
        ]
    },
    {
        "personaje": "Comic Book Guy",
        "texto": "...",
        "opciones": [
            ("¿Puede pagarme ahora?", True),
            ("...", False),
            ("Vaya...", False)
        ]
    }
]

def mostrar_dialogo(personaje, texto):
    lineas = []
    palabras = texto.split()
    linea_actual = personaje + ": "
    for palabra in palabras:
        if len(linea_actual + palabra) > 70:  # Aumentamos el número de caracteres por línea
            lineas.append(linea_actual)
            linea_actual = palabra + " "
        else:
            linea_actual += palabra + " "
    lineas.append(linea_actual)
    
    renders = [fuente_dialogo.render(linea, True, NEGRO) for linea in lineas]
    return renders

def dibujar_boton(texto, x, y, w, h, color_normal, color_hover):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(pantalla, color_hover, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(pantalla, color_normal, (x, y, w, h))
    
    texto_render = fuente.render(texto, True, NEGRO)
    texto_rect = texto_render.get_rect(center=(x + w/2, y + h/2))
    pantalla.blit(texto_render, texto_rect)
    return False

def menu_principal():
    while True:
        pantalla.fill(BLANCO)
        titulo = fuente_grande.render("CompuGlobalHyperMegaNet", True, AMARILLO)
        titulo_rect = titulo.get_rect(center=(ANCHO/2, 100))
        pantalla.blit(titulo, titulo_rect)

        if dibujar_boton("Jugar Normal", 300, 200, 200, 50, GRIS, AMARILLO):
            return "video_normal"
        if dibujar_boton("Jugar Difícil", 300, 275, 200, 50, GRIS, ROJO):
            return "video_dificil"
        if dibujar_boton("Salir", 300, 350, 200, 50, GRIS, AMARILLO):
            return "salir"

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return "salir"

        pygame.display.flip()

def juego(dificultad):
    global jugador_pos, nivel_miedo, bateria, linterna_encendida, vidas_jugador, nivel_actual, enemigo_pos
    dialogo_actual = 0
    puntuacion = 0
    tiempo_limite = 20 if dificultad == "normal" else 5

    while dialogo_actual < len(dialogos):
        tiempo_inicio = time.time()
        seleccion = None
        
        while seleccion is None:
            tiempo_actual = time.time()
            tiempo_restante = tiempo_limite - (tiempo_actual - tiempo_inicio)
            
            if tiempo_restante <= 0:
                return mostrar_resultado("perdiste", puntuacion)
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "salir", puntuacion
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for i, (opcion, _) in enumerate(dialogos[dialogo_actual]["opciones"]):
                        if dibujar_boton(opcion, 50, 400 + i*70, 700, 60, GRIS, AMARILLO):
                            seleccion = i

            pantalla.blit(fondo, (0, 0))
            
            # Dibujar las imágenes de los personajes
            homer_rect = homer.get_rect(topleft=(50, 50))
            comic_book_guy_rect = comic_book_guy.get_rect(topleft=(600, 50))
            
            pantalla.blit(homer, homer_rect)
            pantalla.blit(comic_book_guy, comic_book_guy_rect)

            # Dibujar el borde iluminado alrededor del personaje que habla
            if dialogos[dialogo_actual]["personaje"] == "Homer Simpson":
                dibujar_borde(pantalla, homer_rect, AMARILLO)
            else:
                dibujar_borde(pantalla, comic_book_guy_rect, AMARILLO)

            personaje = dialogos[dialogo_actual]["personaje"]
            texto = dialogos[dialogo_actual]["texto"]
            dialogo_renders = mostrar_dialogo(personaje, texto)
            
            # Dibujar un fondo para el diálogo
            dialogo_altura = len(dialogo_renders) * 25  # Reducimos el espacio entre líneas
            pygame.draw.rect(pantalla, (255, 255, 200), (10, 280, ANCHO - 20, dialogo_altura + 20))
            pygame.draw.rect(pantalla, NEGRO, (10, 280, ANCHO - 20, dialogo_altura + 20), 2)
            
            for i, render in enumerate(dialogo_renders):
                pantalla.blit(render, (20, 290 + i * 25))  # Ajustamos el espaciado vertical

            for i, (opcion, _) in enumerate(dialogos[dialogo_actual]["opciones"]):
                dibujar_boton(opcion, 50, 400 + i*70, 700, 60, GRIS, AMARILLO)

            tiempo_render = fuente.render(f"Tiempo: {int(tiempo_restante)}s", True, ROJO)
            pantalla.blit(tiempo_render, (650, 20))

            puntuacion_render = fuente.render(f"Puntuación: {puntuacion}", True, VERDE)
            pantalla.blit(puntuacion_render, (20, 20))

            pygame.display.flip()

        if dialogos[dialogo_actual]["opciones"][seleccion][1]:  # Si la opción es correcta (True)
            puntuacion += 1
            dialogo_actual += 1
        else:
            return mostrar_resultado("perdiste", puntuacion)

    return mostrar_resultado("ganaste", puntuacion)  # Si completa todos los diálogos

def mostrar_resultado(resultado, puntuacion):
    pantalla.fill(BLANCO)
    if resultado == "ganaste":
        texto = fuente_grande.render("¡HAS GANADO!", True, VERDE)
    else:
        texto = fuente_grande.render("¡Has perdido!", True, ROJO)
    
    texto_rect = texto.get_rect(center=(ANCHO/2, ALTO/2 - 50))
    pantalla.blit(texto, texto_rect)

    puntuacion_texto = fuente.render(f"Puntuación final: {puntuacion}", True, NEGRO)
    puntuacion_rect = puntuacion_texto.get_rect(center=(ANCHO/2, ALTO/2 + 50))
    pantalla.blit(puntuacion_texto, puntuacion_rect)

    pygame.display.flip()
    pygame.time.wait(3000)  # Espera 3 segundos antes de volver al menú

    return "menu"

def reproducir_video():
    # Inicializar el mixer de Pygame para el audio
    mixer.init()
    
    # Cargar el video
    cap = cv2.VideoCapture('intro.mp4')
    
    # Cargar el audio del video
    mixer.music.load('intro.mp3')
    mixer.music.play()

    # Obtener las dimensiones del video
    ancho_video = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto_video = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    reloj = pygame.time.Clock()
    tiempo_inicio = pygame.time.get_ticks()
    mostrar_skip = True

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Convertir el frame de OpenCV a una superficie de Pygame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.transpose(frame, (1, 0, 2))
            frame = pygame.surfarray.make_surface(frame)

            # Escalar el frame al tamaño de la pantalla
            frame = pygame.transform.scale(frame, (ANCHO, ALTO))
            pantalla.blit(frame, (0, 0))

            # Mostrar botón de Skip durante los primeros 7 segundos
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - tiempo_inicio < 7000 and mostrar_skip:
                if dibujar_boton("Skip", ANCHO - 100, ALTO - 50, 80, 40, GRIS, AMARILLO):
                    cap.release()
                    mixer.music.stop()
                    return "menu"

            pygame.display.flip()

            # Controlar la velocidad de reproducción
            reloj.tick(30)  # Ajusta este valor según los FPS del video

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    cap.release()
                    mixer.music.stop()
                    return "salir"
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        cap.release()
                        mixer.music.stop()
                        return "menu"
        else:
            break

    cap.release()
    mixer.music.stop()
    return "menu"

def main():
    estado = "menu"
    
    while True:
        if estado == "menu":
            estado = menu_principal()
        elif estado == "video_normal":
            estado = reproducir_video()
            if estado == "menu":
                estado = "jugar_normal"
        elif estado == "video_dificil":
            estado = reproducir_video()
            if estado == "menu":
                estado = "jugar_dificil"
        elif estado == "jugar_normal":
            estado = juego("normal")
        elif estado == "jugar_dificil":
            estado = juego("dificil")
        elif estado == "salir":
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
