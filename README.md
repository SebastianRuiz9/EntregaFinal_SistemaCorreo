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
