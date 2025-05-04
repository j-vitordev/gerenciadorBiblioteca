import pyodbc

def listar_drivers():
    drivers = [driver for driver in pyodbc.drivers()]
    print("Drivers disponíveis:", drivers)

if __name__ == '__main__':
    listar_drivers()
