import random   # Importamos random para generar números aleatorios (único import permitido)


# =========================================================================================
# FUNCIONES GENERALES
# Estas funciones pequeñas son los "bloques" con los que se construye todo el juego.
# Cada función hace UNA sola cosa: eso las hace fáciles de entender y de reutilizar.
# =========================================================================================

def is_alive(hp):
    # Comprueba si un personaje sigue vivo.
    # hp: puntos de vida actuales (int o float)
    #
    # En Python, una comparación como "hp > 0" ya produce True o False por sí sola.
    # Entonces podemos devolverla directamente sin necesidad de un if/else.
    # Ejemplo: is_alive(50) devuelve True  |  is_alive(0) devuelve False
    return hp > 0


def show_stats(name, hp, max_hp, potions):
    # Muestra en pantalla las estadísticas actuales del jugador.
    # Se llama al inicio de cada turno de combate para que el jugador sepa cómo va.
    #
    # Los f-strings (f"...") permiten meter variables dentro del texto usando {variable}.
    # El \n al inicio agrega una línea en blanco antes del mensaje para que se vea limpio.
    print(f"\n [{name}]  HP: {hp}/{max_hp}  | Pociones: {potions}")


def get_action():
    # Le pide al jugador que elija una acción durante el combate.
    # Solo acepta "1", "2", "3" o comandos secretos que empiecen con "!".
    # Si el jugador escribe algo inválido, el bucle se repite: el juego nunca se rompe.
    # Retorna: el texto que ingresó el jugador (string).

    while True:
        # "while True" es un bucle infinito: se repite para siempre...
        # ...hasta que el código ejecute un "return", que lo detiene y devuelve el valor.

        print("\n  [1] Atacar   [2] Usar poción   [3] Huir")
        action = input("  Tu acción: ").strip()
        # .strip() elimina espacios vacíos al inicio y al final del texto ingresado.
        # Ejemplo: "  1  " se convierte en "1"

        # Si el texto empieza con "!" es un comando secreto → lo devolvemos tal cual
        if action.startswith("!"):
            return action

        # Si eligió 1, 2 o 3, es una opción válida → la devolvemos
        # "in" comprueba si el valor está dentro de ese grupo de opciones
        if action in ("1", "2", "3"):
            return action

        # Si llegamos hasta aquí, el jugador escribió algo inválido.
        # El bucle while True vuelve a empezar y le pedimos que intente de nuevo.
        print("  Opción inválida. Elige 1, 2 o 3.")


def calculate_damage(base, multiplier, has_crit):
    # Calcula cuánto daño inflige el jugador en un ataque.
    # base:       ataque base del personaje (número entero, ej: 15)
    # multiplier: multiplicador de daño según la clase (decimal, ej: 1.8)
    # has_crit:   True si la clase puede hacer golpe crítico (solo el Rebelde)
    # Retorna:    el daño final como número decimal (float).

    damage = base * multiplier   # Fórmula base: ataque × multiplicador de clase

    # El Rebelde tiene 25% de probabilidad de golpe crítico (daño doble).
    # random.random() genera un número decimal aleatorio entre 0.0 y 1.0.
    # Si ese número es menor a 0.25, significa que "cayó" en el 25% de probabilidad.
    if has_crit and random.random() < 0.25:
        damage = damage * 2           # El daño se duplica
        print("*** CRITICAL HIT! ***")  # Mensaje exacto requerido por el enunciado

    return damage   # Devolvemos el daño final (puede tener decimales)


def apply_potion(hp, max_hp):
    # Aplica una poción de salud al jugador: cura exactamente 40 HP.
    # La vida no puede superar el máximo del personaje (no hay "sobre-curación").
    # hp:     vida actual del jugador
    # max_hp: vida máxima del jugador
    # Retorna: la nueva vida del jugador.

    hp = hp + 40        # Sumamos 40 puntos de vida
    if hp > max_hp:     # Si nos pasamos del máximo permitido...
        hp = max_hp     # ...fijamos la vida exactamente en el máximo
    return hp           # Devolvemos la vida actualizada


def attempt_flee(zone):
    # Intenta que el jugador huya del combate actual.
    # Hay un 40% de probabilidad de éxito en zonas normales.
    # Contra el Dragón (zona 4) es imposible: siempre retorna False.
    # zone:    número de zona (1, 2, 3 o 4)
    # Retorna: True si logró escapar, False si no.

    if zone == 4:
        # La zona 4 es el jefe final (Dragón): no se puede huir nunca
        print(" ¡No puedes huir del Dragón!")
        return False

    # random.random() da un número entre 0.0 y 1.0.
    # Comparar con 0.4 significa: "hay un 40% de probabilidad de que sea menor a 0.4"
    if random.random() < 0.4:
        print(" ¡Lograste huir exitosamente!")
        return True    # Escapó con éxito
    else:
        print(" ¡No pudiste huir!")
        return False   # El intento falló


def zone_reward(hp, max_hp, potions):
    # Entrega las recompensas al completar una zona:
    #   → Restaura 30 HP (sin pasar el máximo)
    #   → Da 1 poción extra
    # hp:      vida actual
    # max_hp:  vida máxima
    # potions: pociones actuales
    # Retorna: dos valores separados por coma → (nueva vida, nuevas pociones)
    # En Python se pueden retornar varios valores así y recibirlos separados también.

    hp = hp + 30           # Restauramos 30 puntos de vida
    if hp > max_hp:        # Si nos pasamos del máximo...
        hp = max_hp        # ...lo limitamos al máximo exacto
    potions = potions + 1  # Le damos una poción extra al jugador
    return hp, potions     # Retornamos los dos valores actualizados


def show_final_score(name, player_class, result, total_kills, zones_cleared,
                     total_damage, total_potions_used, total_turns):
    # Muestra la pantalla de resultados al terminar el juego.
    # Se llama tanto si el jugador ganó como si perdió.
    # Los nombres de las etiquetas son exactamente los que especifica el enunciado (en inglés).

    print("\n" + "=" * 30)
    print(f" HERO:           {name}")
    print(f" CLASS:          {player_class}")
    print(f" RESULT:         {result}")                      # Será "Won!" o "Defeated"
    print(f" Enemies slain:  {total_kills}")                 # Enemigos derrotados
    print(f" Zones cleared:  {zones_cleared}")               # Zonas completadas
    print(f" Damage dealt:   {round(total_damage, 1)}")      # round() redondea a 1 decimal
    print(f" Potions used:   {total_potions_used}")          # Pociones consumidas
    print(f" Turns survived: {total_turns}")                 # Turnos de combate jugados
    print("=" * 30)


# =========================================================================================
# MECÁNICA ÚNICA — COMANDOS SECRETOS  (Adicional obligatorio del enunciado)
# Esta mecánica diferencia nuestro juego: comandos ocultos que el jugador puede descubrir.
# Se escriben en cualquier turno de combate y NO gastan el turno.
# =========================================================================================

def px1(command, player_hp, player_max_hp, player_attack, player_multiplier):
    # Procesa los comandos secretos del juego.
    # command:           el texto escrito por el jugador (empieza con "!")
    # player_hp:         vida actual del jugador
    # player_max_hp:     vida máxima del jugador
    # player_attack:     ataque base del jugador
    # player_multiplier: multiplicador de daño actual
    #
    # Comandos disponibles:
    #   !rezar → sube el multiplicador de daño un 15%, 20% o 30% al azar
    #   !heal  → 50% de curar HP, 50% de perder HP (la magia es impredecible)
    #
    # Retorna los tres valores que pueden cambiar: player_hp, player_attack, player_multiplier

    if command == "!rezar":
        print("\n Rezas en voz baja...")

        # random.random() genera un número decimal entre 0.0 y 1.0.
        # Lo usamos para simular tres posibilidades con distintas probabilidades:
        #   0.0 a 0.33 → ~33% de probabilidad (bendición pequeña)
        #   0.33 a 0.66 → ~33% de probabilidad (bendición media)
        #   0.66 a 1.0  → ~34% de probabilidad (bendición grande)
        resultado = random.random()

        if resultado < 0.33:
            bonus = 1.15   # +15%: multiplicamos el multiplicador por 1.15
            print(" ¡Los dioses te bendicen! Tu ataque sube un +15%.")
        elif resultado < 0.66:
            bonus = 1.20   # +20%
            print(" ¡Los dioses te bendicen! Tu ataque sube un +20%.")
        else:
            bonus = 1.30   # +30%: el más poderoso
            print(" ¡¡ARMAGEDÓN!! ¡Tu ataque sube un brutal +30%!")

        # Multiplicamos el multiplicador actual por el bonus recibido.
        # Si ya tenía 1.5 y saca +20%, queda en 1.5 × 1.20 = 1.80
        player_multiplier = player_multiplier * bonus
        print(f" Nuevo multiplicador de daño: {round(player_multiplier, 2)}")

    elif command == "!heal":
        print("\n Invocas energía curativa... la magia es impredecible.")

        resultado = random.random()   # Nuevo número aleatorio: 50/50 curar o dañar

        if resultado < 0.5:
            # --- La magia CURA ---
            # random.uniform(a, b) da un decimal aleatorio ENTRE a y b (no entero).
            # Ejemplo: random.uniform(0.01, 0.50) puede dar 0.27, 0.43, 0.08, etc.
            porcentaje = random.uniform(0.01, 0.50)
            curacion = int(player_max_hp * porcentaje)
            # int() convierte el decimal a entero redondeando hacia abajo.
            # Ejemplo: si max_hp=120 y porcentaje=0.35 → 120 * 0.35 = 42.0 → int = 42
            player_hp = player_hp + curacion
            if player_hp > player_max_hp:   # No superar el HP máximo
                player_hp = player_max_hp
            print(f" ¡La magia te cura {curacion} HP!")
        else:
            # --- La magia DAÑA ---
            porcentaje = random.uniform(0.01, 0.20)   # Entre 1% y 20% del HP máximo
            dano = int(player_max_hp * porcentaje)
            player_hp = player_hp - dano
            if player_hp < 1:
                # La magia nunca puede matarte: como mínimo te deja en 1 HP
                player_hp = 1
            print(f" ¡La magia es inestable! Pierdes {dano} HP.")

    else:
        # El jugador escribió algo con "!" pero no coincide con ningún comando conocido
        print(f"  Comando '{command}' no reconocido.")

    # Retornamos los tres valores que pudo haber modificado esta función.
    # player_attack no cambia, pero lo retornamos para que combat() pueda recibirlos todos juntos.
    return player_hp, player_attack, player_multiplier


# =========================================================================================
# SISTEMA DE COMBATE
# Gestiona un combate completo entre el jugador y UN enemigo, turno por turno.
# Recibe todos los datos necesarios y retorna todos los valores actualizados al terminar.
# =========================================================================================

def combat(player_name, player_hp, player_max_hp, player_attack, player_multiplier,
           player_potions, player_crit,
           enemy_name, enemy_hp, enemy_attack,
           zone,
           total_kills, total_damage, total_potions_used, total_turns):

    # Esta función recibe muchos parámetros porque necesita toda la información
    # del jugador, del enemigo y los contadores para funcionar.
    # Al terminar el combate, retorna TODOS esos valores actualizados.
    #
    # El combate sigue este ciclo en cada turno:
    #   1. Muestra el estado del jugador y del enemigo
    #   2. El jugador elige acción (1/2/3 o comando secreto)
    #   3. Se ejecuta la acción elegida
    #   4. Si el enemigo sigue vivo, contraataca
    #   5. Vuelve al paso 1 hasta que alguien llegue a 0 HP o el jugador huya
    #
    # Retorna 10 valores:
    # (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
    #  total_kills, total_damage, total_potions_used, total_turns, enemy_died)
    # enemy_died = True si el enemigo murió, False si el jugador huyó o murió.

    print(f"\n ¡Apareció un {enemy_name}! (HP: {enemy_hp})")

    # El combate continúa mientras los dos personajes estén vivos (HP > 0)
    while is_alive(player_hp) and is_alive(enemy_hp):

        # Mostramos el estado del jugador y el HP actual del enemigo
        show_stats(player_name, player_hp, player_max_hp, player_potions)
        print(f" [{enemy_name}] HP: {enemy_hp}")

        action = get_action()          # Pedimos la acción al jugador
        total_turns = total_turns + 1  # Contamos este como un turno jugado

        # ---------------------------------------------------------------
        # COMANDOS SECRETOS: empiezan con "!" → no gastan turno de combate
        # ---------------------------------------------------------------
        if action.startswith("!"):
            player_hp, player_attack, player_multiplier = px1(
                action, player_hp, player_max_hp, player_attack, player_multiplier
            )
            total_turns = total_turns - 1
            # "continue" salta directo al inicio del while, ignorando el resto del código
            # del turno. Esto significa que el enemigo NO ataca después de un comando secreto.
            continue

        # ---------------------------------------------------------------
        # OPCIÓN 1: ATACAR
        # ---------------------------------------------------------------
        if action == "1":
            damage = calculate_damage(player_attack, player_multiplier, player_crit)
            damage = round(damage, 1)              # Redondeamos a 1 decimal
            enemy_hp = enemy_hp - damage           # Reducimos la vida del enemigo
            total_damage = total_damage + damage   # Sumamos al contador total de daño
            print(f" Atacas al {enemy_name} e infliges {damage} de daño!")

        # ---------------------------------------------------------------
        # OPCIÓN 2: USAR POCIÓN
        # ---------------------------------------------------------------
        elif action == "2":
            if player_potions == 0:
                # No hay pociones → avisamos pero el turno igual se consume
                print(" ¡No tienes pociones disponibles!")
            else:
                player_hp = apply_potion(player_hp, player_max_hp)   # Curamos al jugador
                player_potions = player_potions - 1                    # Gastamos una poción
                total_potions_used = total_potions_used + 1            # Contamos la poción
                print(f" Usaste una poción. HP: {player_hp}/{player_max_hp}")

        # ---------------------------------------------------------------
        # OPCIÓN 3: HUIR
        # ---------------------------------------------------------------
        elif action == "3":
            if attempt_flee(zone):
                # El jugador escapó: salimos de combat() inmediatamente.
                # El False del final indica que el enemigo NO murió (el jugador huyó).
                return (player_hp, player_max_hp, player_attack,
                        player_multiplier, player_potions,
                        total_kills, total_damage, total_potions_used, total_turns,
                        False)

        # ---------------------------------------------------------------
        # CONTRAATAQUE DEL ENEMIGO
        # Solo ocurre si el enemigo sigue vivo después de la acción del jugador
        # ---------------------------------------------------------------
        if is_alive(enemy_hp):
            player_hp = player_hp - enemy_attack
            print(f" {enemy_name} te ataca y te inflige {enemy_attack} de daño!")

    # ---------------------------------------------------------------
    # FIN DEL BUCLE: llegamos aquí porque alguien llegó a 0 HP
    # ---------------------------------------------------------------
    if is_alive(player_hp):
        # El jugador sigue vivo → ganó el combate
        print(f"\n ¡Derrotaste al {enemy_name}!")
        total_kills = total_kills + 1   # Sumamos una victoria al contador
        enemy_died = True
    else:
        # El jugador llegó a 0 HP → fue derrotado
        player_hp = 0   # Nos aseguramos de que no quede en negativo
        print(f"\n ¡Fuiste derrotado por el {enemy_name}...")
        enemy_died = False

    # Retornamos los 10 valores actualizados para que main() los pueda usar
    return (player_hp, player_max_hp, player_attack,
            player_multiplier, player_potions,
            total_kills, total_damage, total_potions_used, total_turns,
            enemy_died)


# =========================================================================================
# CREACIÓN DE PERSONAJE
# Solicita nombre y clase al jugador y asigna las estadísticas correspondientes.
# =========================================================================================

def create_character():
    # Solicita al jugador su nombre y clase, y asigna los stats (estadísticas) según el enunciado.
    # Valida que el nombre no esté vacío y que la clase sea 1, 2 o 3.
    #
    # Retorna 8 valores a la vez (tupla):
    # (player_name, player_class, player_hp, player_max_hp,
    #  player_attack, player_multiplier, player_potions, player_crit)

    print("\n" + "=" * 30)
    print("   CREACIÓN DE PERSONAJE")
    print("=" * 30)

    # --- Pedimos el nombre ---
    # Iniciamos player_name vacío para poder entrar al while
    player_name = ""
    while player_name == "":
        # El bucle se repite mientras el nombre sea una cadena vacía ""
        player_name = input("  Ingresa tu nombre: ").strip()
        if player_name == "":
            print("  El nombre no puede estar vacío.")

    # --- Mostramos las tres clases disponibles con sus estadísticas ---
    print("\n  Elige tu clase:")
    print("  [1] Guerrero  — HP: 120 | Ataque: 15 | Pociones: 3 | Críticos: No")
    print("  [2] Mago      — HP:  70 | Ataque: 12 | Pociones: 2 | Críticos: No  (x1.8 daño)")
    print("  [3] Rebelde   — HP:  90 | Ataque: 13 | Pociones: 2 | Críticos: Sí  (x1.3 daño)")

    # --- Pedimos la clase ---
    # "not in" significa "que NO esté dentro de ese grupo de opciones válidas"
    player_class = ""
    while player_class not in ("1", "2", "3"):
        player_class = input("  Tu clase (1/2/3): ").strip()
        if player_class not in ("1", "2", "3"):
            print("  Opción inválida. Elige 1, 2 o 3.")

    # --- Asignamos los stats según la clase (valores exactos del enunciado) ---
    if player_class == "1":
        # GUERRERO: el más resistente, tiene 3 pociones, sin críticos
        player_class      = "Guerrero"
        player_hp         = 120
        player_max_hp     = 120
        player_attack     = 15
        player_multiplier = 1.0    # Multiplicador neutro: 15 × 1.0 = 15 de daño base
        player_potions    = 3
        player_crit       = False  # No puede hacer golpe crítico

    elif player_class == "2":
        # MAGO: poco HP pero el mayor multiplicador de daño
        player_class      = "Mago"
        player_hp         = 70
        player_max_hp     = 70
        player_attack     = 12
        player_multiplier = 1.8    # 12 × 1.8 = 21.6 de daño base (el más alto)
        player_potions    = 2
        player_crit       = False

    else:
        # REBELDE: equilibrado y el ÚNICO que puede hacer golpe crítico (daño doble)
        player_class      = "Rebelde"
        player_hp         = 90
        player_max_hp     = 90
        player_attack     = 13
        player_multiplier = 1.3    # 13 × 1.3 = 16.9 de daño base
        player_potions    = 2
        player_crit       = True   # Tiene 25% de probabilidad de golpe crítico

    print(f"\n  ¡Bienvenido, {player_name} el {player_class}!")

    # Retornamos los 8 datos del personaje como una tupla.
    # En main() los recibiremos con: (a, b, c, ...) = create_character()
    return (player_name, player_class,
            player_hp, player_max_hp,
            player_attack, player_multiplier,
            player_potions, player_crit)


# =========================================================================================
# FUNCIÓN PRINCIPAL
# Controla el flujo completo: bienvenida → personaje → zonas → jefe final → pantalla final.
# Es obligatoria según el enunciado y es la que arranca todo el juego.
# =========================================================================================

def main():

    # --- Pantalla de bienvenida ---
    print("\n" + "=" * 40)
    print("      CONSOLA QUEST — RPG DE TEXTO")
    print("=" * 40)
    print(" Crea tu personaje y conquista las 3 zonas.")
    print(" Derrota al Dragón para ganar el juego.")
    print("=" * 40)

    # --- Creamos el personaje ---
    # create_character() devuelve 8 valores a la vez.
    # Los "recibimos" listándolos entre paréntesis separados por coma (desempaquetado de tupla).
    (player_name, player_class,
     player_hp, player_max_hp,
     player_attack, player_multiplier,
     player_potions, player_crit) = create_character()

    # --- Inicializamos los 5 contadores de puntuación en cero ---
    total_kills        = 0    # Enemigos derrotados
    total_damage       = 0.0  # Daño total (usamos 0.0 para que sea decimal desde el inicio)
    total_potions_used = 0    # Pociones consumidas
    total_turns        = 0    # Turnos de combate (los comandos secretos no cuentan)
    zones_cleared      = 0    # Zonas completadas

    # ==================================================================================
    # ZONA 1 — EL BOSQUE
    # Enemigos: Goblin (HP 30, Ataque 8) y Wolf (HP 40, Ataque 11)
    # ==================================================================================
    print("\n" + "=" * 40)
    print("          ZONA 1 — EL BOSQUE")
    print("=" * 40)

    # Llamamos a combat() y recibimos los 10 valores que retorna.
    # Los parámetros son: datos del jugador, datos del enemigo, zona, contadores.
    # "enemy_died" recibe el último valor (True/False): si el enemigo murió o no.
    # combat() siempre retorna 10 valores; el último es enemy_died (True/False).
    # Lo recibimos aunque no lo usemos directamente, porque en main() preferimos
    # verificar el resultado con is_alive(player_hp), que es más claro de leer.
    (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
     total_kills, total_damage, total_potions_used, total_turns, enemy_died) = combat(
        player_name, player_hp, player_max_hp, player_attack, player_multiplier,
        player_potions, player_crit,
        "Goblin", 30, 8,   # nombre, HP y ataque del enemigo
        1,                  # número de zona
        total_kills, total_damage, total_potions_used, total_turns
    )

    # Después de cada combate revisamos si el jugador murió.
    # Si murió (HP = 0), mostramos la pantalla final y terminamos main() con return.
    if not is_alive(player_hp):
        show_final_score(player_name, player_class, "Defeated",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)
        return

    (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
     total_kills, total_damage, total_potions_used, total_turns, enemy_died) = combat(
        player_name, player_hp, player_max_hp, player_attack, player_multiplier,
        player_potions, player_crit,
        "Wolf", 40, 11,
        1,
        total_kills, total_damage, total_potions_used, total_turns
    )

    if not is_alive(player_hp):
        show_final_score(player_name, player_class, "Defeated",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)
        return

    # Zona 1 superada: sumamos 1 a zonas completadas y entregamos la recompensa
    zones_cleared = zones_cleared + 1
    player_hp, player_potions = zone_reward(player_hp, player_max_hp, player_potions)
    print(f"\n ¡Zona 1 completada! HP: {player_hp}/{player_max_hp} | Pociones: {player_potions}")

    # ==================================================================================
    # ZONA 2 — LA MAZMORRA
    # Enemigos: Skeleton (HP 55, Ataque 14) y Troll (HP 80, Ataque 18)
    # ==================================================================================
    print("\n" + "=" * 40)
    print("        ZONA 2 — LA MAZMORRA")
    print("=" * 40)

    (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
     total_kills, total_damage, total_potions_used, total_turns, enemy_died) = combat(
        player_name, player_hp, player_max_hp, player_attack, player_multiplier,
        player_potions, player_crit,
        "Skeleton", 55, 14,
        2,
        total_kills, total_damage, total_potions_used, total_turns
    )

    if not is_alive(player_hp):
        show_final_score(player_name, player_class, "Defeated",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)
        return

    (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
     total_kills, total_damage, total_potions_used, total_turns, enemy_died) = combat(
        player_name, player_hp, player_max_hp, player_attack, player_multiplier,
        player_potions, player_crit,
        "Troll", 80, 18,
        2,
        total_kills, total_damage, total_potions_used, total_turns
    )

    if not is_alive(player_hp):
        show_final_score(player_name, player_class, "Defeated",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)
        return

    zones_cleared = zones_cleared + 1
    player_hp, player_potions = zone_reward(player_hp, player_max_hp, player_potions)
    print(f"\n ¡Zona 2 completada! HP: {player_hp}/{player_max_hp} | Pociones: {player_potions}")

    # ==================================================================================
    # ZONA 3 — EL CASTILLO
    # Enemigos: Dark Knight (HP 100, Ataque 20-30) y Witch (HP 85, Ataque 25-45)
    # Los ataques de esta zona son aleatorios: se generan con random.randint(min, max),
    # que devuelve un número entero aleatorio entre min y max (ambos incluidos).
    # ==================================================================================
    print("\n" + "=" * 40)
    print("        ZONA 3 — EL CASTILLO")
    print("=" * 40)

    dark_knight_attack = random.randint(20, 30)   # Entero aleatorio entre 20 y 30
    witch_attack       = random.randint(25, 45)   # Entero aleatorio entre 25 y 45

    (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
     total_kills, total_damage, total_potions_used, total_turns, enemy_died) = combat(
        player_name, player_hp, player_max_hp, player_attack, player_multiplier,
        player_potions, player_crit,
        "Dark Knight", 100, dark_knight_attack,
        3,
        total_kills, total_damage, total_potions_used, total_turns
    )

    if not is_alive(player_hp):
        show_final_score(player_name, player_class, "Defeated",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)
        return

    (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
     total_kills, total_damage, total_potions_used, total_turns, enemy_died) = combat(
        player_name, player_hp, player_max_hp, player_attack, player_multiplier,
        player_potions, player_crit,
        "Witch", 85, witch_attack,
        3,
        total_kills, total_damage, total_potions_used, total_turns
    )

    if not is_alive(player_hp):
        show_final_score(player_name, player_class, "Defeated",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)
        return

    zones_cleared = zones_cleared + 1
    player_hp, player_potions = zone_reward(player_hp, player_max_hp, player_potions)
    print(f"\n ¡Zona 3 completada! HP: {player_hp}/{player_max_hp} | Pociones: {player_potions}")

    # ==================================================================================
    # JEFE FINAL — EL DRAGÓN
    # HP mínimo 200 (entre 200 y 250), Ataque entre 35 y 50.
    # Zona 4: attempt_flee() siempre retorna False → no se puede huir.
    # ==================================================================================
    print("\n" + "=" * 40)
    print("       JEFE FINAL — EL DRAGÓN")
    print(" ¡No hay escapatoria! ¡A vencer o morir!")
    print("=" * 40)

    dragon_hp     = random.randint(200, 250)   # HP mínimo 200 según el enunciado
    dragon_attack = random.randint(35, 50)     # Ataque entre 35 y 50

    (player_hp, player_max_hp, player_attack, player_multiplier, player_potions,
     total_kills, total_damage, total_potions_used, total_turns, enemy_died) = combat(
        player_name, player_hp, player_max_hp, player_attack, player_multiplier,
        player_potions, player_crit,
        "Dragon", dragon_hp, dragon_attack,
        4,   # Zona 4 → no se puede huir
        total_kills, total_damage, total_potions_used, total_turns
    )

    # --- Pantalla final: victoria o derrota ---
    if is_alive(player_hp):
        zones_cleared = zones_cleared + 1   # Contamos la zona del Dragón
        print("\n ¡¡¡FELICITACIONES!!! ¡Derrotaste al Dragón y salvaste el reino!")
        show_final_score(player_name, player_class, "Won!",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)
    else:
        show_final_score(player_name, player_class, "Defeated",
                         total_kills, zones_cleared, total_damage, total_potions_used, total_turns)


# =========================================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
#
# Cuando Python ejecuta un archivo directamente (ej: python main.py),
# la variable especial __name__ toma el valor "__main__".
# Esta línea verifica eso y llama a main() para arrancar el juego.
#
# Si alguien importara este archivo desde otro script, __name__ sería diferente
# y main() NO se ejecutaría sola. Es una buena práctica en Python.
# =========================================================================================
if __name__ == "__main__":
    main()
