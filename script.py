import datetime
import json
from typing import Dict, List

class SistemaFichaje:
    def __init__(self):
        # Initialize the system with an empty users dictionary and attendance records
        self.usuarios = {}  # Store user credentials
        self.registros = {} # Store attendance records
        self.archivo_registros = "registros_fichaje.json"
        self.cargar_registros()

    def cargar_registros(self):
        # Load existing records from JSON file
        try:
            with open(self.archivo_registros, 'r') as f:
                self.registros = json.load(f)
        except FileNotFoundError:
            self.registros = {}

    def guardar_registros(self):
        # Save records to JSON file
        with open(self.archivo_registros, 'w') as f:
            json.dump(self.registros, f)

    def registrar_usuario(self, usuario: str, contraseña: str):
        # Register a new user in the system
        self.usuarios[usuario] = contraseña
        if usuario not in self.registros:
            self.registros[usuario] = []
        self.guardar_registros()

    def iniciar_sesion(self, usuario: str, contraseña: str) -> bool:
        # Verify user credentials
        return self.usuarios.get(usuario) == contraseña

    def fichar_entrada(self, usuario: str) -> str:
        # Register entry time for user
        ahora = datetime.datetime.now()
        registro = {
            "fecha": ahora.strftime("%Y-%m-%d"),
            "hora_entrada": ahora.strftime("%H:%M:%S"),
            "hora_salida": None
        }
        
        if usuario not in self.registros:
            self.registros[usuario] = []
        
        # Check if user already checked in today
        for reg in self.registros[usuario]:
            if reg["fecha"] == registro["fecha"] and reg["hora_salida"] is None:
                return "Ya has fichado la entrada hoy"

        self.registros[usuario].append(registro)
        self.guardar_registros()
        return f"Entrada registrada: {registro['fecha']} {registro['hora_entrada']}"

    def fichar_salida(self, usuario: str) -> str:
        # Register exit time for user
        ahora = datetime.datetime.now()
        
        if usuario not in self.registros:
            return "No hay registros para este usuario"

        # Find today's open entry
        for registro in reversed(self.registros[usuario]):
            if registro["fecha"] == ahora.strftime("%Y-%m-%d") and registro["hora_salida"] is None:
                registro["hora_salida"] = ahora.strftime("%H:%M:%S")
                self.guardar_registros()
                return f"Salida registrada: {registro['fecha']} {registro['hora_salida']}"
        
        return "No hay entrada registrada para hoy"

    def consultar_fichajes(self, usuario: str) -> List[Dict]:
        # Get all attendance records for a user
        if usuario not in self.registros:
            return []
        return self.registros[usuario]

# Example usage
def main():
    # Create system instance
    sistema = SistemaFichaje()
    
    # Register a test user
    sistema.registrar_usuario("empleado1", "1234")
    
    # Login
    if sistema.iniciar_sesion("empleado1", "1234"):
        print("Sesión iniciada correctamente")
        
        # Check in
        print(sistema.fichar_entrada("empleado1"))
        
        # Simulate work time
        import time
        time.sleep(2)
        
        # Check out
        print(sistema.fichar_salida("empleado1"))
        
        # Query records
        registros = sistema.consultar_fichajes("empleado1")
        print("\nRegistros del empleado:")
        for registro in registros:
            print(f"Fecha: {registro['fecha']}")
            print(f"Entrada: {registro['hora_entrada']}")
            print(f"Salida: {registro['hora_salida']}")
            print("---")

if __name__ == "__main__":
    main()
