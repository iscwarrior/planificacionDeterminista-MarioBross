Versión gráfica básica en consola tipo tablero (grid) donde Mario se 
mueve paso a paso hasta llegar a la meta.

Funcionamiento (planificación determinista):
* Mario (M) empieza en la columna 0.
* Hay un hongo (🍄) en la columna 2.
* Una llave (🔑) en la columna 4.
* Una puerta (🚪) en la columna 6.
** Mario debe tomar el hongo → tomar la llave → abrir la puerta → entrar.

Explicación:

* El planificador BFS encuentra un plan para que Mario complete el nivel: 
    ** MoveToMushroom → TakeMushroom → MoveToKey → GetKey → MoveToDoor → OpenDoor → EnterDoor.

Simulación paso a paso en consola:

* Representación del mundo como una línea (grid de 7 casillas).
* Mario (M) se mueve hacia los objetos y los va recogiendo.
* La puerta 🚪 cambia a 🚪✅ cuando se abre.
* Finalmente, aparece el mensaje  ¡Nivel completado!.