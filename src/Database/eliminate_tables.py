import sqlite3

try:
    connection = sqlite3.connect("./src/Database/bd")
    cursor = connection.cursor()

    cursor.executescript(
        """
        BEGIN;

        DROP TABLE IF EXISTS Prevision_Especialista;
        DROP TABLE IF EXISTS Citas;
        DROP TABLE IF EXISTS Horario_Atencion;
        DROP TABLE IF EXISTS Prevision;
        DROP TABLE IF EXISTS Especialista;
        DROP TABLE IF EXISTS Paciente;

        COMMIT;
        """
    )
except Exception as ex:
    print(ex)
finally:
    connection.close()