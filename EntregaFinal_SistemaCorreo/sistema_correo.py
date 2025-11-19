from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import uuid
import heapq


# =======================
#  ENTIDADES BÁSICAS
# =======================

class Mensaje:
    """
    Representa un correo electrónico.
    Entrega 1: encapsulamiento de atributos y métodos de acceso.
    """

    #--- Valida campos obligatorios y guarda los datos del mensaje ---
    def __init__(
        self,
        remitente: str,
        destinatario: str,
        asunto: str,
        cuerpo: str,
        prioridad: str = "Media",
    ):
        if not destinatario:
            raise ValueError("El mensaje debe tener destinatario.")
        if prioridad not in {"Alta", "Media", "Baja"}:
            prioridad = "Media"

        self._id = str(uuid.uuid4())
        self._remitente = remitente
        self._destinatario = destinatario
        self._asunto = asunto
        self._cuerpo = cuerpo
        self._fecha = datetime.now()
        self._leido = False
        self._prioridad = prioridad

    # --- propiedades (encapsulamiento) ---
    @property
    def id(self) -> str:
        return self._id

    @property
    def remitente(self) -> str:
        return self._remitente

    @property
    def destinatario(self) -> str:
        return self._destinatario

    @property
    def asunto(self) -> str:
        return self._asunto

    @property
    def cuerpo(self) -> str:
        return self._cuerpo

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def prioridad(self) -> str:
        return self._prioridad

    @property
    def leido(self) -> bool:
        return self._leido

    # --- Cambia el estado del mensaje a "leido" ---
    def marcar_leido(self) -> None:
        self._leido = True

    # --- Cambia el estado del mensaje a "no leido" ---
    def marcar_no_leido(self) -> None:
        self._leido = False
    # --- representacion legible del mensaje ---
    def __repr__(self) -> str:
        marca = "✓" if self._leido else "•"
        return f"<{marca} {self._asunto} ({self._prioridad})>"


class Carpeta:
    """
    Nodo del árbol general de carpetas.
    Entrega 2: soporta subcarpetas recursivas.
    """

    # --- Crea una carpeta, opcionalmente ligada a un padre en el arbol ---
    def __init__(self, nombre: str, padre: Optional["Carpeta"] = None):
        self._nombre = nombre
        self._mensajes: List[Mensaje] = []
        self._subcarpetas: Dict[str, "Carpeta"] = {}
        self._padre = padre

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def padre(self) -> Optional["Carpeta"]:
        return self._padre

    @property
    def subcarpetas(self) -> Dict[str, "Carpeta"]:
        return self._subcarpetas

    # --- agrega un mensaje a esta carpeta ---
    def agregar_mensaje(self, mensaje: Mensaje) -> None:
        self._mensajes.append(mensaje)
    # --- Elimina un mensaje si existe alguno en la carpeta ---
    def quitar_mensaje(self, mensaje: Mensaje) -> None:
        self._mensajes.remove(mensaje)

    def mensajes(self) -> List[Mensaje]:
        # devuelvo copia para no exponer la lista interna
        return list(self._mensajes)

    def obtener_por_indice(self, idx: int) -> Optional[Mensaje]:
        return self._mensajes[idx] if 0 <= idx < len(self._mensajes) else None

    # --- Crea una subcarpeta y la agrega al diccionario de subcarpetas ---
    def crear_subcarpeta(self, nombre: str) -> "Carpeta":
        if nombre in self._subcarpetas:
            raise ValueError(f"La subcarpeta '{nombre}' ya existe.")
        nueva = Carpeta(nombre, padre=self)
        self._subcarpetas[nombre] = nueva
        return nueva

    def obtener_subcarpeta(self, nombre: str) -> Optional["Carpeta"]:
        return self._subcarpetas.get(nombre)

    # --- utilitarios para menú ---
    def listar_mensajes(self, con_indices: bool = False) -> None:
        if not self._mensajes:
            print("No hay mensajes.")
            return
        for i, m in enumerate(self._mensajes, start=1):
            marca = "✓" if m.leido else "•"
            pref = f"{i}. " if con_indices else ""
            print(
                f"{pref}{marca} {m.fecha:%Y-%m-%d %H:%M} | "
                f"De: {m.remitente} | Asunto: {m.asunto} | Prioridad: {m.prioridad}"
            )
    # --- Imprime la estructura de carpetas y mensajes de forma recursiva
    def listar_contenido(self, nivel: int = 0) -> None:
        indent = "  " * nivel
        print(f"{indent}📁 {self._nombre}")
        for m in self._mensajes:
            marca = "✓" if m.leido else "•"
            print(f"{indent}   {marca} {m.asunto}")
        for sub in self._subcarpetas.values():
            sub.listar_contenido(nivel + 1)


# =======================
#  SISTEMA DE CARPETAS
# =======================

class SistemaCorreo:
    """
    Gestiona el árbol de carpetas de un usuario.

    Complejidad (peor caso):
      - buscar_mensajes_recursivo: Tiempo O(N + C), Espacio O(N + D)
      - mover_mensaje (con carpeta conocida): Tiempo O(1) para extraer/insertar
        N = total de mensajes, C = total de carpetas, D = profundidad del árbol.
    """

    def __init__(self, carpeta_raiz: Carpeta):
        self._carpeta_raiz = carpeta_raiz

    @property
    def carpeta_raiz(self) -> Carpeta:
        return self._carpeta_raiz

    #--- recibe una ruta tipo entrada/importante y devuelve la carpeta correspondiente
    def obtener_por_ruta(self, ruta: str) -> Carpeta:
        """Navega una ruta tipo 'Entrada/Trabajo/2025'."""
        partes = ruta.strip("/").split("/")
        actual = self._carpeta_raiz
        for p in partes:
            sub = actual.obtener_subcarpeta(p)
            if not sub:
                raise ValueError(f"No existe la carpeta '{p}' en la ruta '{ruta}'")
            actual = sub
        return actual

    # ---Búsqueda DFS en todo el árbol: recorre subcarpetas y junta coincidencias---
    def buscar_mensajes_recursivo(self, texto: str) -> List[Tuple[Carpeta, Mensaje]]:
        """Búsqueda recursiva por remitente o asunto que contengan 'texto'."""
        texto = texto.lower()

        def _buscar(carpeta: Carpeta) -> List[Tuple[Carpeta, Mensaje]]:
            resultado: List[Tuple[Carpeta, Mensaje]] = []
            for m in carpeta.mensajes():
                if texto in m.asunto.lower() or texto in m.remitente.lower():
                    resultado.append((carpeta, m))
            for sub in carpeta.subcarpetas.values():
                resultado.extend(_buscar(sub))
            return resultado

        return _buscar(self._carpeta_raiz)

    # --- Mueve un mensaje desde una carpeta origen a otra carpeta destino ---
    def mover_mensaje(self, carpeta_origen: Carpeta, indice: int, carpeta_destino: Carpeta) -> None:
        mensaje = carpeta_origen.obtener_por_indice(indice)
        if mensaje is None:
            raise IndexError("Índice de mensaje fuera de rango.")
        carpeta_origen.quitar_mensaje(mensaje)
        carpeta_destino.agregar_mensaje(mensaje)


# =======================
#  COLA DE PRIORIDADES
# =======================

class ColaPrioridades:
    """
    Cola de prioridades basada en heapq.
    Entrega 3: gestionar mensajes 'urgentes'.
    """

    # --- Asigna prioridades a numeros para el heap (menor numero = mayor prioridad) ---
    _valor = {"Alta": 1, "Media": 2, "Baja": 3}

    def __init__(self):
        self._heap: List[Tuple[int, Mensaje]] = []

    # --- Inserta un mensaje al heap junto con su nivel de prioridad ---
    def agregar(self, mensaje: Mensaje) -> None:
        prioridad_num = self._valor.get(mensaje.prioridad, 2)
        heapq.heappush(self._heap, (prioridad_num, mensaje))

    # --- EXTRAE Y RETORNA EL MENSAJE CON MAYOR PRIORIDAD ---
    def procesar(self) -> Optional[Mensaje]:
        """Devuelve el mensaje siguiente según prioridad o None si está vacía."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[1]

    def esta_vacia(self) -> bool:
        return not self._heap


# =======================
#  INTERFAZ DE MENSAJERÍA
# =======================

class IMensajeria(ABC):
    """Entrega 1: interfaz para servicios de correo."""

    @abstractmethod
    def enviar(self, mensaje: Mensaje) -> None:
        ...

    @abstractmethod
    def recibir(self, email: str) -> List[Mensaje]:
        ...

    @abstractmethod
    def listar(self, email: str, carpeta: str) -> List[Mensaje]:
        ...


# =======================
#  SERVIDOR DE CORREO
# =======================

class ServidorCorreo(IMensajeria):
    """
    Maneja usuarios, filtros automáticos y cola de prioridades.
    """

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._usuarios: Dict[str, Usuario] = {}
        # palabra clave -> carpeta de destino
        self._filtros: Dict[str, str] = {
            "urgente": "Prioritarios",
            "oferta": "Promociones",
            "universidad": "Academicos",
        }
        self._cola_prioridades = ColaPrioridades()

    @property
    def nombre(self) -> str:
        return self._nombre

    # --- gestión de usuarios ---
    def registrar_usuario(self, usuario: "Usuario") -> None:
        if usuario.email in self._usuarios:
            raise ValueError(f"El email {usuario.email} ya está registrado.")
        self._usuarios[usuario.email] = usuario

    def _obtener_usuario(self, email: str) -> "Usuario":
        usuario = self._usuarios.get(email)
        if not usuario:
            raise ValueError(f"No existe el usuario {email} en el servidor {self._nombre}.")
        return usuario

    # --- filtros automáticos ---
    def agregar_filtro(self, palabra_clave: str, carpeta_destino: str) -> None:
        self._filtros[palabra_clave.lower()] = carpeta_destino

    def _aplicar_filtros(self, mensaje: Mensaje, usuario_destino: "Usuario") -> None:
        texto = (mensaje.asunto + " " + mensaje.cuerpo).lower()
        carpeta_nombre = "Entrada"
        for palabra, carpeta in self._filtros.items():
            if palabra in texto:
                carpeta_nombre = carpeta
                break
        carpeta = usuario_destino.obtener_carpeta(carpeta_nombre)
        carpeta.agregar_mensaje(mensaje)

    # --- implementación de la interfaz ---
    def enviar(self, mensaje: Mensaje) -> None:
        # Enviador (si está en este servidor) guarda copia en Enviados
        remitente = self._usuarios.get(mensaje.remitente)
        if remitente:
            remitente.obtener_carpeta("Enviados").agregar_mensaje(mensaje)

        # El mensaje entra a la cola de prioridades
        self._cola_prioridades.agregar(mensaje)

        # Entrega inmediata al destinatario (si existe en este servidor)
        try:
            destinatario = self._obtener_usuario(mensaje.destinatario)
            self._aplicar_filtros(mensaje, destinatario)
        except ValueError:
            # podría ser un usuario de otro servidor; lo maneja RedServidores
            pass

    def procesar_mensajes_prioritarios(self) -> None:
        """Muestra los mensajes según prioridad (Alta primero)."""
        print("\nProcesando mensajes por prioridad:")
        while not self._cola_prioridades.esta_vacia():
            m = self._cola_prioridades.procesar()
            print(f" - {m.prioridad}: {m.asunto} (para {m.destinatario})")

    def recibir(self, email: str) -> List[Mensaje]:
        usuario = self._obtener_usuario(email)
        return usuario.obtener_carpeta("Entrada").mensajes()

    def listar(self, email: str, carpeta: str) -> List[Mensaje]:
        usuario = self._obtener_usuario(email)
        c = usuario.obtener_carpeta(carpeta)
        return c.mensajes()


# =======================
#  RED DE SERVIDORES (GRAFO)
# =======================

class RedServidores:
    """
    Modela la red como un grafo no dirigido.
    Entrega 3: BFS y DFS para recorrer/conectar servidores.
    """

    def __init__(self):
        self._servidores: Dict[str, ServidorCorreo] = {}
        self._conexiones: Dict[str, List[str]] = {}

    def agregar_servidor(self, servidor: ServidorCorreo) -> None:
        self._servidores[servidor.nombre] = servidor
        self._conexiones.setdefault(servidor.nombre, [])

    # --- AGREGA UNA CONEXION (ARISTA) BIDIRECCIONAL ENTRE DOS SERVIDORES ---
    def conectar(self, a: str, b: str) -> None:
        self._conexiones.setdefault(a, []).append(b)
        self._conexiones.setdefault(b, []).append(a)

    # --- BFS (para encontrar ruta más corta de servidores) ---
    def bfs(self, origen: str, destino: str) -> Optional[List[str]]:
        visitados = set()
        cola: List[Tuple[str, List[str]]] = [(origen, [origen])]
        while cola:
            actual, camino = cola.pop(0)
            if actual == destino:
                return camino
            if actual in visitados:
                continue
            visitados.add(actual)
            for vecino in self._conexiones.get(actual, []):
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino]))
        return None

    # --- DFS (para recorrer toda la red) ---
    def dfs(self, origen: str, visitados: Optional[set] = None) -> List[str]:
        if visitados is None:
            visitados = set()
        visitados.add(origen)
        resultado = [origen]
        for vecino in self._conexiones.get(origen, []):
            if vecino not in visitados:
                resultado.extend(self.dfs(vecino, visitados))
        return resultado

    # --- envío entre servidores usando la ruta BFS ---
    def enviar_entre_servidores(self, mensaje: Mensaje, nombre_origen: str, nombre_destino: str) -> None:
        ruta = self.bfs(nombre_origen, nombre_destino)
        if not ruta:
            print("No hay ruta entre servidores.")
            return
        print("Ruta elegida (BFS):", " -> ".join(ruta))
        servidor_destino = self._servidores.get(nombre_destino)
        if not servidor_destino:
            print("Servidor destino inexistente.")
            return
        servidor_destino.enviar(mensaje)


# =======================
#  USUARIO
# =======================

class Usuario:
    """
    Entrega 1: clase Usuario con encapsulamiento.
    Cada usuario tiene un árbol de carpetas propio (Entrega 2).
    """

    def __init__(self, nombre: str, email: str):
        self._nombre = nombre
        self._email = email
        self._raiz = Carpeta("Root")
        # carpetas básicas
        self._raiz.crear_subcarpeta("Entrada")
        self._raiz.crear_subcarpeta("Enviados")
        self._raiz.crear_subcarpeta("Prioritarios")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo: str) -> None:
        if nuevo:
            self._nombre = nuevo

    @property
    def email(self) -> str:
        return self._email

    def raiz(self) -> Carpeta:
        return self._raiz

    def obtener_carpeta(self, nombre: str) -> Carpeta:
        sub = self._raiz.obtener_subcarpeta(nombre)
        if not sub:
            sub = self._raiz.crear_subcarpeta(nombre)
        return sub

    # --- CREA UN MENSAJE (SIN ENVIARLO) ---
    def redactar(self, destinatario: str, asunto: str, cuerpo: str, prioridad: str = "Media") -> Mensaje:
        return Mensaje(self.email, destinatario, asunto, cuerpo, prioridad)

    def enviar_mensaje(
        self,
        servidor: ServidorCorreo,
        destinatario: str,
        asunto: str,
        cuerpo: str,
        prioridad: str = "Media",
    ) -> None:
        msg = self.redactar(destinatario, asunto, cuerpo, prioridad)
        servidor.enviar(msg)


# =======================
#  FUNCIONES DE MENÚ (CLI)
# =======================

def seleccionar_carpeta(usuario: Usuario) -> Optional[Carpeta]:
    print("\nSeleccionar carpeta:")
    print("1. Entrada")
    print("2. Enviados")
    print("3. Prioritarios")
    op = input("Opción: ").strip()
    if op == "1":
        return usuario.obtener_carpeta("Entrada")
    if op == "2":
        return usuario.obtener_carpeta("Enviados")
    if op == "3":
        return usuario.obtener_carpeta("Prioritarios")
    print("Opción inválida.")
    return None


def crear_subcarpeta_menu(sistema: SistemaCorreo) -> None:
    print("\n-- Crear subcarpeta --")
    ruta_base = input("Ruta base (por ej. 'Entrada' o 'Entrada/Trabajo'): ").strip()
    try:
        base = sistema.obtener_por_ruta(ruta_base)
    except ValueError as e:
        print(e)
        return
    nombre = input("Nombre de la nueva subcarpeta: ").strip()
    try:
        base.crear_subcarpeta(nombre)
        print(f"Subcarpeta '{nombre}' creada dentro de '{ruta_base}'.")
    except ValueError as e:
        print(e)


def mover_mensaje_menu(sistema: SistemaCorreo) -> None:
    print("\n-- Mover mensaje --")
    ruta_origen = input("Ruta carpeta origen: ").strip()
    ruta_destino = input("Ruta carpeta destino: ").strip()
    try:
        carpeta_origen = sistema.obtener_por_ruta(ruta_origen)
        carpeta_destino = sistema.obtener_por_ruta(ruta_destino)
    except ValueError as e:
        print(e)
        return

    carpeta_origen.listar_mensajes(con_indices=True)
    idx_txt = input("Número de mensaje a mover: ").strip()
    if not idx_txt.isdigit():
        print("Índice inválido.")
        return
    idx = int(idx_txt) - 1
    try:
        sistema.mover_mensaje(carpeta_origen, idx, carpeta_destino)
        print("Mensaje movido correctamente.")
    except Exception as e:
        print(e)


def buscar_mensajes_menu(sistema: SistemaCorreo) -> None:
    print("\n-- Buscar mensajes (recursivo en todo el árbol) --")
    texto = input("Texto a buscar (en asunto o remitente): ").strip()
    resultados = sistema.buscar_mensajes_recursivo(texto)
    if not resultados:
        print("No se encontraron mensajes.")
        return
    print(f"Se encontraron {len(resultados)} mensajes:\n")
    for carpeta, m in resultados:
        print(f"📁 {carpeta.nombre} | De: {m.remitente} | Asunto: {m.asunto} | Prioridad: {m.prioridad}")


def explorar_arbol(usuario: Usuario) -> None:
    def _explorar(c: Carpeta) -> None:
        while True:
            print(f"\n📁 Carpeta actual: {c.nombre}")
            c.listar_mensajes()
            if c.subcarpetas:
                print("\nSubcarpetas:")
                for i, sub in enumerate(c.subcarpetas.values(), start=1):
                    print(f" {i}. {sub.nombre}")
            else:
                print("\n(No hay subcarpetas)")

            print("\nOpciones:")
            print("1. Entrar en subcarpeta")
            print("2. Volver (a carpeta padre)")
            op = input("Opción: ").strip()
            if op == "1":
                if not c.subcarpetas:
                    print("No hay subcarpetas.")
                    continue
                num = input("Número de subcarpeta: ").strip()
                if not num.isdigit():
                    print("Número inválido.")
                    continue
                num = int(num)
                if num < 1 or num > len(c.subcarpetas):
                    print("Fuera de rango.")
                    continue
                sub = list(c.subcarpetas.values())[num - 1]
                _explorar(sub)
            elif op == "2":
                return
            else:
                print("Opción inválida.")

    _explorar(usuario.raiz())


def demo_red_servidores() -> None:
    print("\n--- DEMO RED DE SERVIDORES ---")
    s1 = ServidorCorreo("Servidor_A")
    s2 = ServidorCorreo("Servidor_B")
    s3 = ServidorCorreo("Servidor_C")

    u1 = Usuario("Luis", "luis@a.com")
    u2 = Usuario("Ana", "ana@b.com")

    s1.registrar_usuario(u1)
    s2.registrar_usuario(u2)

    red = RedServidores()
    red.agregar_servidor(s1)
    red.agregar_servidor(s2)
    red.agregar_servidor(s3)
    red.conectar("Servidor_A", "Servidor_C")
    red.conectar("Servidor_C", "Servidor_B")

    msg = u1.redactar("ana@b.com", "Prueba red urgente", "Mensaje que viaja por la red", "Alta")
    red.enviar_entre_servidores(msg, "Servidor_A", "Servidor_B")

    print("\nRecorrido DFS de la red desde Servidor_A:")
    print(" -> ".join(red.dfs("Servidor_A")))


# =======================
#  MENÚ PRINCIPAL (CLI)
# =======================

def menu_principal(usuario: Usuario, servidor: ServidorCorreo, sistema: SistemaCorreo) -> None:
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Enviar mensaje")
        print("2. Ver bandeja de entrada")
        print("3. Ver enviados")
        print("4. Crear subcarpeta")
        print("5. Buscar mensajes (recursivo)")
        print("6. Mover mensaje entre carpetas")
        print("7. Ver árbol completo")
        print("8. Procesar mensajes por prioridad")
        print("9. Cambiar nombre de usuario")
        print("10. Demo red de servidores (BFS/DFS)")
        print("0. Salir")

        op = input("Opción: ").strip()

        if op == "1":
            dest = input("Destinatario: ").strip()
            asunto = input("Asunto: ").strip()
            cuerpo = input("Mensaje: ").strip()
            prioridad = input("Prioridad (Alta/Media/Baja) [Media]: ").strip().capitalize() or "Media"
            usuario.enviar_mensaje(servidor, dest, asunto, cuerpo, prioridad)
            print("Mensaje enviado.")

        elif op == "2":
            usuario.obtener_carpeta("Entrada").listar_mensajes(con_indices=True)

        elif op == "3":
            usuario.obtener_carpeta("Enviados").listar_mensajes(con_indices=True)

        elif op == "4":
            crear_subcarpeta_menu(sistema)

        elif op == "5":
            buscar_mensajes_menu(sistema)

        elif op == "6":
            mover_mensaje_menu(sistema)

        elif op == "7":
            usuario.raiz().listar_contenido()

        elif op == "8":
            servidor.procesar_mensajes_prioritarios()

        elif op == "9":
            nuevo = input("Nuevo nombre de usuario: ").strip()
            usuario.nombre = nuevo
            print("Nombre actualizado.")

        elif op == "10":
            demo_red_servidores()

        elif op == "0":
            print("Hasta luego.")
            break

        else:
            print("Opción inválida.")


# =======================
#  MAIN
# =======================

def main() -> None:
    servidor = ServidorCorreo("Servidor_Local")
    u1 = Usuario("Luis", "luis@mail.com")
    u2 = Usuario("Ana", "ana@mail.com")
    servidor.registrar_usuario(u1)
    servidor.registrar_usuario(u2)

    sistema = SistemaCorreo(u1.raiz())

    menu_principal(u1, servidor, sistema)


if __name__ == "__main__":
    main()
