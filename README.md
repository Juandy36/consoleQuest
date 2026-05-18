# ⚔️ Console Quest RPG

> Un RPG de texto por consola — elige tu clase, atraviesa tres zonas y derrota al Dragón final.

---

## 📖 Descripción

**Console Quest** es un juego de rol basado en texto que se ejecuta completamente en la terminal. El jugador crea su personaje, combate a través de tres zonas con enemigos progresivamente más difíciles y se enfrenta a un jefe final. Al terminar (victoria o derrota) se muestra una pantalla de puntuación con estadísticas detalladas.

---

## 🎮 Clases de Personaje

| Stat              | Warrior | Mage | Rogue |
|-------------------|---------|------|-------|
| HP                | 120     | 70   | 90    |
| Ataque base       | 15      | 12   | 13    |
| Multiplicador     | 1.0     | 1.8  | 1.3   |
| Pociones iniciales| 3       | 2    | 2     |
| Crítico           | ✗       | ✗    | ✓     |

> **Rogue** tiene un 25% de probabilidad de asestar un **golpe crítico** que duplica el daño.

---

## 🗺️ Zonas y Enemigos

### Zona 1 — The Forest
| Enemigo | HP | Ataque |
|---------|----|--------|
| Goblin  | 30 | 8      |
| Wolf    | 40 | 11     |

### Zona 2 — The Dungeon
| Enemigo  | HP | Ataque |
|----------|----|--------|
| Skeleton | 55 | 14     |
| Troll    | 80 | 18     |

### Zona 3 — The Castle
| Enemigo    | HP  | Ataque       |
|------------|-----|--------------|
| Dark Knight| 100 | random(20–30)|
| Witch      | 85  | random(25–45)|

### 🐉 Jefe Final — The Dragon
| Enemigo | HP mín. | Ataque       |
|---------|---------|--------------|
| Dragon  | 200     | random(35–50)|

> ⚠️ **No se puede huir del Dragón.**

---

## ⚔️ Sistema de Combate

En cada turno el jugador elige una acción:

```
[1] Attack      — Inflige (ataque × multiplicador) de daño
[2] Use Potion  — Restaura 40 HP (máx: HP máximo); requiere tener pociones
[3] Flee        — 40% de probabilidad de escapar (imposible contra el Dragón)
```

Después de la acción del jugador, el enemigo contraataca si sigue vivo. El combate termina cuando alguno llega a 0 HP.

---

## 🎁 Recompensas entre Zonas

Al completar cada zona:
- ❤️ +30 HP (sin superar el máximo)
- 🧪 +1 poción
- 📊 Se muestran los stats actualizados

---

## ✨ Mecánica Única
 
### 🔮 Comandos Secretos
Durante cualquier turno de combate, el jugador puede escribir comandos especiales en lugar de elegir una acción normal. Estos comandos tienen efectos **aleatorios e impredecibles**, lo que añade un elemento de riesgo y decisión estratégica.
 
Para activarlos, el jugador escribe el comando directamente cuando se le pide su acción:
 
---
 
#### `!rezar`
El jugador invoca a los dioses para que bendigan su arma. El resultado es **completamente aleatorio** — no hay garantía de recibir el mayor bonus:
 
| Resultado | Efecto |
|-----------|--------|
| 33% de probabilidad | +15% al multiplicador de daño |
| 33% de probabilidad | +20% al multiplicador de daño |
| 33% de probabilidad | +30% al multiplicador de daño |
 
> El bonus es permanente para el resto de la partida y se acumula si se usa varias veces.
 
---
 
#### `!heal`
El jugador canaliza energía mágica inestable. Puede **curar o dañar** — nadie lo sabe hasta que ocurre:
 
| Resultado | Efecto |
|-----------|--------|
| 50% de probabilidad | Cura entre el 1% y el 50% del HP máximo |
| 50% de probabilidad | Quita entre el 1% y el 20% del HP máximo |
 
> Usar `!heal` con poca vida es una apuesta arriesgada.
 
---
 
**Notas de diseño:**
- Los comandos no consumen el turno de combate — el enemigo no contraataca cuando se usan.
- Están disponibles en todas las zonas, incluyendo el combate contra el Dragon.
- No hay límite de usos, pero el efecto aleatorio desalienta el spam.
 

## 📊 Puntuación Final

La pantalla final se muestra tanto en victoria como en derrota:

```
==============================
  HERO:           [nombre]
  CLASS:          [clase]
  RESULT:         [Won! / Defeated]
  Enemies slain:  [total_kills]
  Zones cleared:  [zones_cleared]
  Damage dealt:   [total_damage]
  Potions used:   [total_potions_used]
  Turns survived: [total_turns]
==============================
```

---

## 🛠️ Funciones Implementadas

| Función           | Parámetros                        | Retorna      | Propósito                              |
|-------------------|-----------------------------------|--------------|----------------------------------------|
| `calculate_damage`| `base, multiplier, has_crit`      | `float`      | Calcula daño y aplica críticos         |
| `is_alive`        | `hp`                              | `bool`       | Retorna `True` si `hp > 0`             |
| `get_action`      | —                                 | `string`     | Entrada validada, repite si es inválida|
| `apply_potion`    | `hp, max_hp`                      | `int`        | HP curado sin superar el máximo        |
| `attempt_flee`    | `zone`                            | `bool`       | `True` si el jugador escapa            |
| `zone_reward`     | `hp, max_hp, potions`             | `int, int`   | Nuevo HP y pociones tras la zona       |
| `show_stats`      | `name, hp, max_hp, potions`       | —            | Muestra el estado del jugador          |
| `show_final_score`| `...`                             | —            | Muestra resultados finales             |
| `main()`          | —                                 | —            | Punto de entrada del programa          |

---

## ▶️ Cómo Ejecutar

**Requisitos:** Python 3.x (sin dependencias externas)

```bash
python game.py
```

El juego solicitará un nombre y clase al inicio. Todas las entradas inválidas son manejadas sin causar errores.

---

## 📋 Reglas de Implementación

- Solo se usa `import random`
- No se usan clases, listas ni diccionarios
- Toda la lógica está encapsulada en funciones
- Los nombres de variables son descriptivos (`player_hp`, no `x`)
- El programa no falla con entradas inválidas
- El punto de entrada es obligatoriamente `main()`

---

## 👥 Integrantes del Grupo

|              Nombre               |     Rol       |
|-----------------------------------|---------------|
| Juan Diego Ortiz Mora (U00192281) | Desarrollador |
| Alejandra Suarez Duran            | Desarrollador |
| Betsy Ardila Ardila               | Desarrollador |

---

*Proyecto académico — Fundamentos de programacion *