# Simple attendance system for work check-in/check-out
import datetime

class SistemaFichajeSencillo:
    def __init__(self):
        # Initialize empty dictionaries for users and records
        self.usuarios = {}
        self.fichajes = {}

    def registrar_usuario(self, usuario: str, contraseña: str):
        # Register new user
        self.usuarios[usuario] = contraseña
        self.fichajes[usuario] = []
        return "Usuario registrado con éxito"

    def fichar_trabajo(self):
        # Main function to handle the check-in/check-out process
        while True:
            print("\n=== SISTEMA DE FICHAJE ===")
            print("1. Iniciar sesión")
            print("2. Salir")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == "2":
                break
                
            if opcion == "1":
                # Login process
                usuario = input("Usuario: ")
                contraseña = input("Contraseña: ")
                
                if self.usuarios.get(usuario) == contraseña:
                    while True:
                        # Show menu after successful login
                        print("\n=== MENÚ DE FICHAJE ===")
                        print(f"Bienvenido {usuario}")
                        print(f"Fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d')}")
                        print(f"Hora actual: {datetime.datetime.now().strftime('%H:%M:%S')}")
                        print("\n1. Fichar entrada")
                        print("2. Fichar salida")
                        print("3. Ver mis fichajes")
                        print("4. Cerrar sesión")
                        
                        opcion_fichaje = input("Seleccione una opción: ")
                        
                        if opcion_fichaje == "1":
                            # Register entry
                            self._registrar_entrada(usuario)
                        elif opcion_fichaje == "2":
                            # Register exit
                            self._registrar_salida(usuario)
                        elif opcion_fichaje == "3":
                            # Show records
                            self._mostrar_fichajes(usuario)
                        elif opcion_fichaje == "4":
                            break
                else:
                    print("Usuario o contraseña incorrectos")

    def _registrar_entrada(self, usuario):
        # Register entry time
        ahora = datetime.datetime.now()
        fecha = ahora.strftime("%Y-%m-%d")
        hora = ahora.strftime("%H:%M:%S")
        
        # Check if already checked in
        for fichaje in self.fichajes[usuario]:
            if fichaje["fecha"] == fecha and fichaje["salida"] is None:
                print("Ya has fichado la entrada hoy")
                return
                
        self.fichajes[usuario].append({
            "fecha": fecha,
            "entrada": hora,
            "salida": None
        })
        print(f"Entrada registrada: {fecha} {hora}")

    def _registrar_salida(self, usuario):
        # Register exit time
        ahora = datetime.datetime.now()
        fecha = ahora.strftime("%Y-%m-%d")
        hora = ahora.strftime("%H:%M:%S")
        
        # Find open entry for today
        for fichaje in self.fichajes[usuario]:
            if fichaje["fecha"] == fecha and fichaje["salida"] is None:
                fichaje["salida"] = hora
                print(f"Salida registrada: {fecha} {hora}")
                return
        print("No hay entrada registrada para hoy")

    def _mostrar_fichajes(self, usuario):
        # Show all records for user
        print("\n=== TUS FICHAJES ===")
        for fichaje in self.fichajes[usuario]:
            print(f"Fecha: {fichaje['fecha']}")
            print(f"Entrada: {fichaje['entrada']}")
            print(f"Salida: {fichaje['salida'] or 'Pendiente'}")
            print("---")

# Example usage
def main():
    # Create system instance
    sistema = SistemaFichajeSencillo()
    
    # Register a test user
    sistema.registrar_usuario("juan", "1234")
    
    # Start the system
    sistema.fichar_trabajo()

if __name__ == "__main__":
    main() 