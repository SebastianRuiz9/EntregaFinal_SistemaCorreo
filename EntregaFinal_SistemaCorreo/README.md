
README - TP Sistema de Correo Electrónico

Grupo 39
Integrantes: Luis Sanchez, Yamila Baez, Sebastián Ruiz

---------------------------------------------------
DESCRIPCIÓN GENERAL
---------------------------------------------------
Este proyecto implementa un sistema completo de correo electrónico utilizando
Programación Orientada a Objetos (POO) y estructuras de datos avanzadas.

Incluye:
- Árbol general de carpetas (estructura recursiva)
- Filtros automáticos usando listas y diccionarios
- Cola de prioridades para mensajes urgentes (heapq)
- Red de servidores modelada como grafo (BFS/DFS)
- Interfaz de línea de comandos (CLI)
- Documentación completa y justificación del diseño

---------------------------------------------------
JUSTIFICACIONES DE DISEÑO ORIENTADO A OBJETOS
---------------------------------------------------

1. Clase Mensaje — Encapsulamiento y coherencia
   - Atributos privados con properties.
   - Responsabilidad única: representar un correo.
   - Garantiza integridad y evita modificaciones externas.

2. Clase Carpeta — Árbol general recursivo
   - Implementa composición: carpetas contienen subcarpetas.
   - Permite un árbol N-ario ilimitado.
   - Métodos recursivos para búsqueda y visualización.

3. SistemaCorreo — Controlador del árbol
   - Intermediario entre Usuario y estructura de carpetas.
   - Mantiene bajo acoplamiento (Carpeta no depende del usuario).
   - Permite búsquedas recursivas y mover correos sin duplicar lógica.

4. ColaPrioridades — heap
   - Implementa una cola mínima (min-heap).
   - Prioridad: Alta → Media → Baja.
   - Encapsula totalmente la estructura heap.

5. Interfaz IMensajeria — Polimorfismo
   - Contrato para cualquier implementación de correo.
   - Permite agregar nuevos tipos de servidor.
   - Promueve programación contra interfaces (OCP).

6. ServidorCorreo — Filtros y entrega
   - Maneja usuarios, filtros automáticos, prioridades.
   - Open/Closed Principle: filtros ampliables sin modificar código existente.
   - No mezcla responsabilidades del árbol ni del usuario.

7. RedServidores — Grafo + BFS/DFS
   - Simula red real de servidores.
   - BFS: encuentra ruta más corta de entrega.
   - DFS: recorrido exploratorio.
   - Diseño extensible para futuros protocolos/redes.

8. Usuario — Fachada simple
   - Expone acciones sencillas (enviar, redactar).
   - Encapsula el árbol completo de carpetas.
   - Evita que el resto del sistema manipule carpetas directamente.

9. Menú (CLI) — Independencia total del modelo
   - Solo ejecuta acciones sobre las clases.
   - Si mañana se reemplaza por GUI, no hay que tocar el modelo.
   - Principio de separación de responsabilidades.

---------------------------------------------------
ESTRUCTURAS DE DATOS UTILIZADAS
---------------------------------------------------
- Árbol general → carpetas y subcarpetas
- Listas → colecciones de mensajes
- Diccionarios → subcarpetas y filtros automáticos
- Heap → cola de prioridades
- Grafo → red de servidores (adyacencia)
- BFS / DFS → algoritmos de búsqueda y recorrido

+------------------+
|     Usuario      |
+------------------+
| - __nombre       |
| - __email        |
| - __carpetas     |
+------------------+
| +nombre          |
| +email           |
| +enviar_mensaje()|
| +listar_mensajes()|
+------------------+
        |
        | contiene
        v
+------------------+
|     Carpeta      |
+------------------+
| - __nombre       |
| - __mensajes     |
+------------------+
| +agregar_mensaje()|
| +listar_mensajes()|
+------------------+
        |
        | contiene
        v
+------------------+
|     Mensaje      |
+------------------+
| - __remitente    |
| - __destinatario |
| - __asunto       |
| - __cuerpo       |
+------------------+
| +remitente       |
| +destinatario    |
| +asunto          |
| +cuerpo          |
+------------------+
        ^
        | usa
        |
+------------------+
| ServidorCorreo   |
+------------------+
| - __usuarios     |
+------------------+
| +registrar_usuario()|
| +enviar_mensaje()   |
+------------------+


