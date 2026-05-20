import random


#=========================================================================================
# FUNCIONES GENERALES
#=========================================================================================

def is_alive(hp):
    """Basicamente comprobamos que el jugador este vivo si da true es pq ta vivo sino ps ta muerto"""
    return hp > 0

def show_stats(name, hp, max_hp, potions):
    """Mostramos las estadisticas iniciales del jugador"""
    print(f"\n [{name}]  HP: {hp}/{max_hp}   | Pociones: {potions}")

def get_action():
    """
    -Le pedimos al jugador una accion luego procedemos a validarla, sino pues se mete en un bucle hasta que se ingrese una accion como 1,2 o 3.
    -A su vez detectamos los comandos secretos que empiezan con "!".
    -Retornamos el texto ingresado por el jugador.
    """
    while True:
        print("\n  [1] Atacar   [2] Usar poción   [3] Huir")
        action = input("  Tu acción: ").strip()
 
        # Si es un comando secreto, lo devuelve directamente
        if action.startswith("!"):
            return action
 
        # Solo acepta 1, 2 o 3 como opciones válidas
        if action in ("1", "2", "3"):
            return action
 
        print("   Opción inválida. Elige 1, 2 o 3.")

def calculate_damage(base, multiplier, has_crit):
    """
    -Calcula el daño que inflinge el jugador.
    -Si eligio una clase con has_crit con random, el daño se multplica.
    -retornamos el daño final como un float. 
    """
    damage = base * multiplier

    if has_crit and random.random() < 0.25:
        damage = damage * 2
        print(" GOLPE CRITICO!!!!")

    return damage

def apply_potions(hp, max_hp):
    """
    -Aplica una poción de salud al jugador.
    -Retorna el nuevo valor de salud del jugador.
    """
    hp = hp + 40
    if hp > max_hp:
        hp = max_hp
    return hp

def attemple_flee(zone):
    """
    -Intenta huir del combate, con una probabildad de exito del 40%
    -Claramente es imposible huir del boss final, sino no tendria sentido.
    -Retorna True si logro escapar
    """
    if zone == 4:
        print(" Crees que puedes huir del Dragon? pfffffffffff")
        return False
    if random.random() < 0.4:
        print(" Lograste huir exitosamente!")
        return True
    else:
        print(" No pudiste huir!")
        return False
    
def zone_reward(hp, max_hp, potions):
    """
    -Damos las recompensas entre zonas
    --Recupera 30 HP (sin pasarse claramente)
    --Da 1 pocion extra
    -Retorna el nuevo hp y pociones del jugador
    """

    hp = hp + 30
    if hp > max_hp:
        hp = max_hp
    potions = potions + 1
    return hp, potions

def show_final_score(name, player_class, result, total_kills, zones_cleared, total_damage, total_potions_used, total_turns):
    """ Mostramos la pantalla final con el resultado de la partida"""
    print("\n" + "=" * 40)
    print(f" HEROE:          {name}")
    print(f" CLASE:          {player_class}")
    print(f" RESULTADO:      {result}")
    print(f" ENEMIGOS DERROTADOS: {total_kills}")
    print(f" ZONAS LIMPIADAS: {zones_cleared}")
    print(f" DAÑO TOTAL INFLIGIDO: {total_damage}")
    print(f" POCIONES USADAS: {total_potions_used}")
    print(f" TURNOS JUGADOS:  {total_turns}")
    print("=" * 40)

#=========================================================================================
# MECANICA ESPECIAL
#=========================================================================================

def px1(command, player_hp, player_max_hp, player_attack, player_multiplier):
    """
    procesa los comandos. 

    !rezar = Los diodes bendicen al jugar con una espada con player_multiplier de 15%, 20%, 30% aleatoriamente.
    (solo funciona por partida y todo es aleatorio)

    !heal = Un hechizo claramente inestable no todo es beneficio: cura o daña al jugador
    curacion maxima: 50% de max_hp
    daño maximo: 20% de max_hp pero no puede matar al jugador

    y retornan (player_hp, player_attack, player_multiplier)
    """

    if command == "!rezar":
        print("\n Rezas en voz baja...")
        resultado = random.random()

        if resultado < 0.33:
            bonus = 1.15
            print(" Los dioses te bendicen! Tu espada ahora obtuvo un +15% de poder.")
        elif resultado < 0.66:
            bonus = 1.20
            print(" Los dioses te bendicen! Tu espada ahora obtuvo un +20% de poder.")
        else:
            bonus = 1.30
            print("  HAS OBTENIDO ARMAGEDON!!! Tu espada ahora obtuvo un +30% de poder.")

        player_multiplier = player_multiplier * bonus
        print(f"Tu nuevo multiplicador de daño es: {round(player_multiplier, 2)}")

    elif command == "!heal":
        print("\n Invocas energía curativa...")
        resultado = random.random()

        if resultado < 0.5:
            # aqui va la curacion entre 1% y 50% del max_hp
            porcentaje = random.uniform(0.01, 0.50)
            curacion = int(player_max_hp * porcentaje)
            player_hp = player_hp + curacion
            if player_hp > player_max_hp:
                player_hp = player_max_hp
            print(f"  >> ¡La magia te cura {curacion} HP!")
        else:
            # Daño: entre 1% y 20% del max_hp
            porcentaje = random.uniform(0.01, 0.20)
            dano = int(player_max_hp * porcentaje)
            player_hp = player_hp - dano
            if player_hp < 20:
                player_hp = 1
            print(f"  >> ¡La magia es inestable! Pierdes {dano} HP.")
 
    else:
        print(f"  >> Comando '{command}' no reconocido.")
 
    return player_hp, player_attack, player_multiplier

#=========================================================================================
# SISTEMA DE COMBATE
#=========================================================================================

def combat(player_name, player_hp, player_max_hp, player_attack, player_multiplier, player_potions, player_crit, enemy_name, enemy_hp, enemy_attack, zone, total_kills, total_damage, total_potions_used, total_turns):

    """
    gestiamos el combate completo entre el jufador y un enemigo.
    retorna todos los valores actualizados al terminar.
    """

    print(f"\n ¡Aparecio un {enemy_name}! (HP: {enemy_hp})")

    # El combate continua hasta que alguno ps se muera (como logico no? JAJAJAJ)
    while is_alive(player_hp) and is_alive(enemy_hp):

        show_stats(player_name, player_hp, player_max_hp, player_potions)
        print(f" [{enemy_name}] HP: {enemy_hp}")

        action = get_action()
        total_turns = total_turns + 1

        #----------- PROCESAMOS EL COMANDO ---------------
        if action.startswith("!"):
            player_hp, player_attack, player_multiplier = px1(action, player_hp, player_max_hp, player_attack, player_multiplier)

            # los comandos no consumen turnos
            total_turns = total_turns - 1
            continue
        #----------- Acción 1: Ataque ----------------
        if action == "1":
            damage = calculate_damage(player_attack, player_multiplier, player_crit)
            damage = round(damage, 1)
            enemy_hp = enemy_hp - damage
            total_damage = total_damage + damage
            print(f" Atacas al {enemy_name} e infliges {damage} de daño!")
        
        #----------- Acción 2: Tomar poción ---------------
        elif action == "2":
            if player_potions == 0:
                print(" No tienes pociones disponibles!")
            else: 
                player_hp = apply_potions(player_hp, player_max_hp)
                player_potions = player_potions - 1
                total_potions_used = total_potions_used + 1
                print(f" Usaste una pocion, HP: {player_hp}/{player_max_hp}")
        #----------- Acción 3: Huir ------------------------
        elif action == "3":
            if attemple_flee(zone):
                # logra volarse: el enemigo no muere, pero el combate termina
                return (player_hp, player_max_hp, player_attack,
                        player_multiplier, player_potions,
                        total_kills, total_damage, total_potions_used, total_turns,
                        False) # el false indica que como se volo pues el enemigo quedo vivo 
            
        #----- el enemigo contraataca (si sigue vivo obvio)---------------------
        if is_alive(enemy_hp):
            player_hp = player_hp - enemy_attack
            print(f" {enemy_name} te ataca e inflinge {enemy_attack} de daño!")

#------------ Resultados del pvp ---------------------------
    if is_alive(player_hp):
        print(f"\n ¡Derrotaste al {enemy_name}!")
        total_kills = total_kills + 1
        enemy_died = True
    else:
        player_hp = 0
        print(f"\n ¡Fuiste derrotado por el {enemy_name}...")
        enemy_died = False

    return (player_hp, player_max_hp, player_attack,
            player_multiplier, player_potions,
            total_kills, total_damage, total_potions_used, total_turns,
            enemy_died)
            
 