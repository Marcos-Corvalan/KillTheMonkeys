#! /usr/bin/env python
# -*- coding: utf-8 -*-
import pilasengine
import random

TIEMPO = 6
fin_de_juego = False

pilas = pilasengine.iniciar()

# Usar un fondo estándar
pilas.fondos.Selva()

# Añadir un marcador
puntos = pilas.actores.Puntaje(x=60, y=215, color=pilas.colores.rojo)
puntos.magnitud = 40
puntos.escala = 2

# Añadir el conmutador de Sonido
pilas.actores.Sonido()

# Variables y Constantes
monos = []
tkillmono = None
def monoHabla():    
    frases = ["Ummm...Que rico!!","Gracias!!","BANANAS!"]
    frase = frases[random.randrange(len(frases))]
    return frase

# Funciones
def killmono(mono):
    global tkillmono
    mono.eliminar()
    tkillmono.terminar()

def mono_destruido(disparo, mono):
    global tkillmono
    #global frase
    monos.remove(mono)
    mono.sonreir()
    mono.decir(monoHabla())    
    pilas.utils.interpolar(mono, 'x', mono.x, 2)
    pilas.utils.interpolar(mono, 'y', mono.y, 2)
    tkillmono=pilas.tareas.agregar(.5, killmono, mono) 
    disparo.eliminar()
    puntos.aumentar()

def crear_mono():
    # Crear un enemigo nuevo
    enemigo = pilas.actores.Mono()
    # Hacer que se aparición sea con un efecto bonito
    ##la escala varíe entre 0,25 y 0,75 (Ojo con el radio de colisión)
    enemigo.escala = .5
    # Dotarle de la habilidad de que explote al ser alcanzado por un disparo
    #enemigo.aprender(pilas.habilidades.PuedeExplotar)
    # Situarlo en una posición al azar, no demasiado cerca del jugador
    x = random.randrange(-320, 320)
    y = random.randrange(-240, 240)
    if x >= 0 and x <= 100:
        x = 180
    elif x <= 0 and x >= -100:
        x = -180
    if y >= 0 and y <= 100:
        y = 180
    elif y <= 0 and y >= -100:
        y = -180
    enemigo.x = x
    enemigo.y = y
    # Dotarlo de un movimiento irregular más impredecible
    tipo_interpolacion = ['lineal',
                            'aceleracion_gradual',
                            'desaceleracion_gradual',
                            'rebote_inicial',
                            'rebote_final']
    
    duracion = 1 +random.random()*4
    
    pilas.utils.interpolar(enemigo, 'x', 0, duracion)
    pilas.utils.interpolar(enemigo, 'y', 0, duracion)
    #enemigo.x = pilas.interpolar(0,tiempo,tipo=random.choice(tipo_interpolacion))
    #enemigo.y = pilas.interpolar(0, tiempo,tipo=random.choice(tipo_interpolacion))
    # Añadirlo a la lista de enemigos
    monos.append(enemigo)
    # Permitir la creación de enemigos mientras el juego esté en activo
    if fin_de_juego:
        return False
    else:
        return True

class MiMunicion(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = "banana.png"

    def actualizar(self):
        self.escala = 0.5

def muere_torreta(torreta, mono):

    tarea_crea_mono.terminar()
    torreta.eliminar()
    mono.sonreir()
    mono.decir("Gane!")
    

# Añadir la torreta del jugador

torreta = pilas.actores.Torreta(enemigos=monos, municion_bala_simple=MiMunicion, cuando_elimina_enemigo=mono_destruido)

tarea_crea_mono = pilas.tareas.agregar(1, crear_mono)

pilas.colisiones.agregar(torreta, monos, muere_torreta)
#pilas.mundo.agregar_tarea(1, crear_mono) <-- sintaxis vieja

# Dar un aviso
pilas.avisar("Usa el mouse para darle de comer a los monos")
 
# Arrancar el juego
pilas.ejecutar()
