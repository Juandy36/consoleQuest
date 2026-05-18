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