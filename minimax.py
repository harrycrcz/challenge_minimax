import random  # Utilizaremos este modulo para obtener un valor randomizado para las posiciones iniciales

# Variables a utilizar
tablero_t = 5  # Tamaño del tablero. Usamos una variable para poder cambiarlo de ser necesario sin reescribir tanto codigo
max_turnos = 10  # Turnos maximos que podra correr el juego
profundidad = 4  # Limitamos la profundidad del algoritmo a 4 turnos

# Posibles movimientos, utilizamos 4 (arriba, abajo, izquierda, derecha)
movimientos = {
    'arriba': (-1, 0),
    'abajo': (1, 0),
    'izquierda': (0, -1),
    'derecha': (0, 1)
}

# Variables globales que necesitara nuestra logica de juego
tablero = [[None for _ in range(tablero_t)] for _ in range(tablero_t)]
gato = None
raton = None
salidas = []
turnos = 0


def posiciones_iniciales_random():  # Funcion que define las posiciones iniciales de nuestros jugadores, posiciones aleatorias
    global gato, raton
    # Genera mis filas y columnas para el gato
    gato = (random.randint(0, tablero_t-1), random.randint(0, tablero_t-1))
    # Genera mis filas y columnas para el raton
    raton = (random.randint(0, tablero_t-1), random.randint(0, tablero_t-1))
    # Si las posiciones iniciales son invalidas, vuelve a generar
    while gato == raton or gato in salidas or raton in salidas:
        gato = (random.randint(0, tablero_t-1), random.randint(0, tablero_t-1))
        raton = (random.randint(0, tablero_t-1),
                 random.randint(0, tablero_t-1))


def generar_salidas():  # Funcion que genera 4 salidas en el tablero para nuestro raton, para colorear un poco el juego ;)
    global salidas
    for i in range(tablero_t):  # Iteramos sobre nuestro tamaño de tablero (-1 siempre)
        salidas.append((0, i))          # Fila superior
        salidas.append((tablero_t-1, i))  # Fila inferior
        salidas.append((i, 0))          # Columna izquierda
        salidas.append((i, tablero_t-1))  # Columna derecha


def movimiento_valido(posicion):  # Revisamos si el movimiento es valido
    x, y = posicion  # Descomponemos la tupla posición en dos variabes
    # Verificamos si x e y están dentro del tablero y retornamos
    return 0 <= x < tablero_t and 0 <= y < tablero_t


def mover(posicion, direccion_mov):  # Ejecutamos el movimiento, siempre que sea valido
    # Recibimos la dirección de movimiento y la separamos en coordenadas
    dx, dy = movimientos[direccion_mov]
    # Guardamos la nueva posición utilizando las coordenadas recibidas
    nueva_posicion = (posicion[0] + dx, posicion[1] + dy)
    # Llamamos a la función movimiento_valido para verificar
    if movimiento_valido(nueva_posicion):
        # Si es valido, la función retorna un True y la nueva posición es retornada
        return nueva_posicion
    return posicion  # De no ser válido el movimiento, se retorna la posición original


def distancia(pos1, pos2):  # Calculamos la distancia
    # Utilizamos la distancia Manhattan, retornamos valores absolutos
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def minimax(gato_posicion, raton_posicion, depth, maximiza):  # Funcion minimax
    if depth == profundidad or turnos >= max_turnos:
        return distancia(gato_posicion, raton_posicion)
    if gato_posicion == raton_posicion:
        return float('-inf') if maximiza else float('inf')
    if raton_posicion in salidas:
        return float('10000') if maximiza else float('-10000')

    if maximiza:
        max_eval = float('-inf')
        for direccion_mov in movimientos:
            new_raton_posicion = mover(raton_posicion, direccion_mov)
            eval = minimax(gato_posicion, new_raton_posicion, depth + 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for direccion_mov in movimientos:
            new_gato_posicion = mover(gato_posicion, direccion_mov)
            eval = minimax(new_gato_posicion, raton_posicion, depth + 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


# Funcion que verifica el mejor movimiento de acuerdo al max y al min
def mejor_movimiento(maximiza):
    mejor_valor = float('-inf') if maximiza else float('inf')
    mejor_movimiento = None
    posicion_actual = raton if maximiza else gato

    for direccion_mov in movimientos:
        nueva_posicion = mover(posicion_actual, direccion_mov)
        if maximiza:
            mover_valor = minimax(gato, nueva_posicion, 0, False)
            if mover_valor > mejor_valor:
                mejor_valor = mover_valor
                mejor_movimiento = nueva_posicion
        else:
            mover_valor = minimax(nueva_posicion, raton, 0, True)
            if mover_valor < mejor_valor:
                mejor_valor = mover_valor
                mejor_movimiento = nueva_posicion

    return mejor_movimiento if mejor_movimiento is not None else posicion_actual


def jugar():  # Logica del juego
    global turnos, gato, raton
    generar_salidas()
    posiciones_iniciales_random()

    while turnos < max_turnos:
        print(f"Round {turnos + 1}")
        print(f"gato: {gato}, raton: {raton}")
        turnos += 1

        # raton mover
        raton = mejor_movimiento(True)
        if gato == raton:
            print("El gato ha cenado!")
            return
        if raton in salidas:
            print("El ratón escapó por una salida!")
            return

        # gato mover
        gato = mejor_movimiento(False)
        if gato == raton:
            print("El gato ha cenado!")
            return

    print("El ratón sobrevivió por 10 rondas!")


jugar()
