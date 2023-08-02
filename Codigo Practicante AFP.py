#!/usr/bin/env python
# coding: utf-8

# In[56]:


# A continuación se presenta el código de Python para administrar el acceso de vehículos a un estacionamiento de pago:


# Importamos las librerías necesarias
import sqlite3

# Creamos la conexión a la base de datos
conn = sqlite3.connect('parking.db')

# Creamos la tabla de vehículos
c = conn.cursor()
c.execute('CREATE TABLE vehicles (plate TEXT, type TEXT, time INTEGER)')

# Insertamos algunos datos de prueba
c.execute('INSERT INTO vehicles VALUES ("ABC123", "Official", 0)')
c.execute('INSERT INTO vehicles VALUES ("DEF456", "Resident", 0)')
c.execute('INSERT INTO vehicles VALUES ("GHI789", "Non-resident", 0)')

# Cerramos la conexión
conn.close()


# Código para gestionar las estancias de los vehículos:


# Ahora vamos a crear las clases que nos permitirán gestionar los vehículos con sus datos asociados (estancias, tiempo, etc.), las listas de vehículos registrados como oficiales y residentes, etc.

class Vehiculo:
    def __init__(self, placa, tipo, tiempo):
        self.placa = placa
        self.tipo = tipo
        self.tiempo = tiempo
class Estancia:
    def __init__(self, fecha_entrada, fecha_salida, tiempo):
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.tiempo = tiempo
class ListaVehiculosOficiales:
    def __init__(self):
        self.lista = []
    def agregar_vehiculo(self, vehiculo):
        self.lista.append(vehiculo)
    def obtener_vehiculo(self, placa):
        for vehiculo in self.lista:
            if vehiculo.placa == placa:
                return vehiculo
class ListaVehiculosResidentes:
    def __init__(self):
        self.lista = []
    def agregar_vehiculo(self, vehiculo):
        self.lista.append(vehiculo)
    def obtener_vehiculo(self, placa):
        for vehiculo in self.lista:
            if vehiculo.placa == placa:
                return vehiculo
            



# In[ ]:


# Código para calcular el monto a pagar por el estacionamiento:


def calculate_parking_fee(plate):
    
    # Conectamos a la base de datos
    conn = sqlite3.connect('parking.db')
    # Creamos un cursor
    c = conn.cursor()
    # Consultamos el tipo de vehículo
    c.execute('SELECT type FROM vehicles WHERE plate = ?', (plate,))
    # Obtenemos el tipo de vehículo
    type = c.fetchone()[0]
    # Calculamos el tiempo de estacionamiento
    c.execute('SELECT time FROM vehicles WHERE plate = ?', (plate,))
    # Obtenemos el tiempo de estacionamiento
    time = c.fetchone()[0]
    # Calculamos el monto a pagar
    if type == "Official":
        monto = 0
    elif type == "Resident":
        monto = time * 0.05
    else:
        monto = time * 0.5
    return monto
    


# In[55]:


# Si le sale el mensaje de que la tabla Table Vehicles existe, utilizar el siguiente código: 
 
# c.execute('DROP TABLE vehicles')

 # Para crear la tabla nuevamente: 
 
 # c.execute('CREATE TABLE vehicles (plate TEXT, type TEXT, time INTEGER)')
 


# In[47]:


# Para el caso de uso "Registra entrada":


# Ahora vamos a crear una función que nos permita registrar la entrada de un vehículo

def register_entry(plate):
    
    # Conectamos a la base de datos
    
    conn = sqlite3.connect('parking.db')
    
    # Creamos un cursor
    
    c = conn.cursor()
    
    # Consultamos el tipo de vehículo
    
    c.execute('SELECT type FROM vehicles WHERE plate = ?', (plate,))
    
    # Obtenemos el tipo de vehículo
    type = c.fetchone()[0]
    
    # Actualizamos el tiempo de estacionamiento
    
    c.execute('UPDATE vehicles SET time = time + 1 WHERE plate = ?', (plate,))
    
    # Guardamos los cambios
    conn.commit()
    
    # Cerramos la conexión
    conn.close()
    
    # Ahora vamos a llamar a la función para registrar la entrada del vehículo
    register_entry("ABC123")


# In[48]:


# Para el caso de uso "Registra salida" : 


# Ahora vamos a crear una función que nos permita registrar la salida de un vehículo

def register_exit(plate):
    # Conectamos a la base de datos
    conn = sqlite3.connect('parking.db')
    # Creamos un cursor
    c = conn.cursor()
    # Consultamos el tipo de vehículo
    c.execute('SELECT type FROM vehicles WHERE plate = ?', (plate,))
    # Obtenemos el tipo de vehículo
    type = c.fetchone()[0]
    # Calculamos el tiempo de estacionamiento
    c.execute('SELECT time FROM vehicles WHERE plate = ?', (plate,))
    # Obtenemos el tiempo de estacionamiento
    time = c.fetchone()[0]
    # Realizamos las acciones correspondientes al tipo de vehículo
    if type == "Official":
        # Asociamos la estancia (hora de entrada y hora de salida) con el vehículo
        c.execute('INSERT INTO estancias VALUES (?, ?)', (plate, time))
    elif type == "Resident":
        # Sumamos la duración de la estancia al tiempo total acumulado
        c.execute('UPDATE vehicles SET time = time + ? WHERE plate = ?', (time, plate))
    else:
        # Obtenemos el importe a pagar
        amount = calculate_parking_fee(plate)
        # Guardamos los cambios
        conn.commit()
        # Cerramos la conexión
        conn.close()
        
        # Ahora vamos a llamar a la función para registrar la salida del vehículo
        register_exit("ABC123")


# In[49]:


# Para el caso de uso "Da de alta vehículo oficial":


# Ahora vamos a crear una función que nos permita dar de alta un vehículo oficial

def register_official_vehicle(plate):
    
    # Conectamos a la base de datos
    conn = sqlite3.connect('parking.db')
    # Creamos un cursor
    c = conn.cursor()
    # Consultamos el tipo de vehículo
    c.execute('SELECT type FROM vehicles WHERE plate = ?', (plate,))
    # Obtenemos el tipo de vehículo
    type = c.fetchone()[0]
    # Si el tipo de vehículo es "Official", añadimos el vehículo a la lista de vehículos oficiales
    if type == "Official":
        c.execute('INSERT INTO official_vehicles VALUES (?)', (plate,))
    # Guardamos los cambios
    conn.commit()
    # Cerramos la conexión
    conn.close()
# Ahora vamos a llamar a la función para dar de alta el vehículo oficial
register_official_vehicle("ABC123")



# In[50]:


# Para el caso de uso "Da de alta vehículo de residente":


# Ahora vamos a crear una función que nos permita dar de alta un vehículo de residente

def register_resident_vehicle(plate):
    # Conectamos a la base de datos
    conn = sqlite3.connect('parking.db')
    # Creamos un cursor
    c = conn.cursor()
    # Consultamos el tipo de vehículo
    c.execute('SELECT type FROM vehicles WHERE plate = ?', (plate,))
    # Obtenemos el tipo de vehículo
    type = c.fetchone()[0]
    # Si el tipo de vehículo es "Resident", añadimos el vehículo a la lista de vehículos de residentes
    if type == "Resident":
        c.execute('INSERT INTO resident_vehicles VALUES (?)', (plate,))
    # Guardamos los cambios
    conn.commit()
    # Cerramos la conexión
    conn.close()
# Ahora vamos a llamar a la función para dar de alta el vehículo de residente
register_resident_vehicle("DEF456")




# In[51]:


# Para el caso de uso "Comienza mes":


# Ahora vamos a crear una función que nos permita comenzar el mes

def begin_month():
    # Conectamos a la base de datos
    conn = sqlite3.connect('parking.db')
    # Creamos un cursor
    c = conn.cursor()
    # Eliminamos las estancias registradas en los coches oficiales
    c.execute('DELETE FROM vehicles WHERE type = "Official"')
    # Ponemos a cero el tiempo estacionado por los vehículos de residentes
    c.execute('UPDATE vehicles SET time = 0 WHERE type = "Resident"')
    # Guardamos los cambios
    conn.commit()
    # Cerramos la conexión
    conn.close()
# Ahora vamos a llamar a la función para comenzar el mes
begin_month()


# In[52]:


# Para el caso de uso "Pagos de residentes":


# Ahora vamos a crear una función que nos permita generar el informe de pagos de residentes

def generate_resident_payment_report(filename):
    
    # Conectamos a la base de datos
    conn = sqlite3.connect('parking.db')
    # Creamos un cursor
    c = conn.cursor()
    # Consultamos los vehículos de residentes
    c.execute('SELECT plate, time FROM vehicles WHERE type = "Resident"')
    # Guardamos los resultados en una lista
    results = c.fetchall()
    # Cerramos la conexión
    conn.close()
    # Abrimos el archivo de salida
    with open(filename, 'w') as f:
        
        # Escribimos el encabezado del archivo
        f.write('Núm. placa\tTiempo estacionado (min.)\tCantidad a pagar\n')
        
        # Escribimos los resultados en el archivo
        for result in results:
            f.write('{}\t{}\t{}\n'.format(result[0], result[1], calculate_parking_fee(result[0])))
            
# Ahora vamos a llamar a la función para generar el informe de pagos de residentes
generate_resident_payment_report('resident_payment_report.txt')


# In[53]:


# El siguiente código muestra un ejemplo de cómo utilizar Hibernate para almacenar datos en una base de datos:

# La información de cada una de las estancias de los vehículos se almacenará en una base de datos. 

# Debido a que el manejador de base de datos puede ser modificado en cualquier momento, se utilizará Hibernate como ORM. 

# Hibernate es un framework de persistencia de datos que proporciona una capa de abstracción sobre la base de datos subyacente. 

# Esto permite que las aplicaciones sean independientes del manejador de base de datos que se utilice. 

# Para utilizar Hibernate, primero es necesario crear un modelo de datos que represente la estructura de la base de datos. 

# Una vez creado el modelo, se puede utilizar Hibernate para generar el código SQL necesario para almacenar y recuperar datos de la base de datos.

# Creamos un modelo de datos que represente la estructura de la base de datos

public class Vehicle {
    private String plate;
    private String type;
    private int time;
    public String getPlate() {
        return plate;
    }
    public void setPlate(String plate) {
        this.plate = plate;
    }
    public String getType() {
        return type;
    }
    public void setType(String type) {
        this.type = type;
    }
    public int getTime() {
        return time;
    }
    public void setTime(int time) {
        this.time = time;
    }
}


# In[61]:


# Una vez creado el modelo de datos, se puede utilizar Hibernate para generar el código SQL 
# necesario para almacenar y recuperar datos de la base de datos. 

# El siguiente código muestra un ejemplo de cómo utilizar Hibernate para almacenar datos en una base de datos:


# Creamos una sesión con Hibernate

Session session = HibernateUtil.getSessionFactory().openSession();

# Guardamos un vehículo en la base de datos

Vehicle vehicle = new Vehicle();
vehicle.setPlate("ABC123");
vehicle.setType("Official");
vehicle.setTime(0);
session.save(vehicle);

# Cerramos la sesión
session.close();

# El código anterior guardará un vehículo con la matrícula "ABC123" y el tipo "Official" en la base de datos.






