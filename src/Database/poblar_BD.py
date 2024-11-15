import sqlite3

try:
    connection = sqlite3.connect("./src/Database/bd")
    cursor = connection.cursor()
    cursor.executescript(
    """
    BEGIN;

    INSERT INTO Especialista (rut, nombre, especialidad, telefono, correo) VALUES
    ('12345678-9', 'Alejandro pérez', 'Cardiología', '+56952834901', 'APerez@gmail.com'),
    ('98765432-1', 'Dra. Beatriz Gómez', 'Dermatología', '987654321', 'beatriz.gomez@example.com'),
    ('11223344-5', 'Dr. Carlos López', 'Neurología', '112233445', 'carlos.lopez@example.com'),
    ('22334455-6', 'Dra. Daniela Fernández', 'Pediatría', '223344556', 'daniela.fernandez@example.com'),
    ('33445566-7', 'Dr. Eduardo Martínez', 'Gastroenterología', '334455667', 'eduardo.martinez@example.com'),
    ('44556677-8', 'Dra. Francisca Torres', 'Oftalmología', '445566778', 'francisca.torres@example.com'),
    ('55667788-9', 'Dr. Gabriel Soto', 'Psiquiatría', '556677889', 'gabriel.soto@example.com'),
    ('66778899-0', 'Dra. Helena Rojas', 'Ginecología', '667788990', 'helena.rojas@example.com'),
    ('77889900-1', 'Dr. Ignacio Vega', 'Urología', '778899001', 'ignacio.vega@example.com'),
    ('88990011-2', 'Dra. Julia Ramírez', 'Endocrinología', '889900112', 'julia.ramirez@example.com');

    INSERT INTO Paciente (rut, nombre, fecha_nacimiento, telefono, correo) VALUES
    ('11111111-1', 'Juan Pérez', '1980-01-15', '+56912345678', 'juan.perez@example.com'),
    ('22222222-2', 'María González', '1990-02-20', '+56923456789', 'maria.gonzalez@example.com'),
    ('33333333-3', 'Carlos Sánchez', '1985-03-25', '+56934567890', 'carlos.sanchez@example.com'),
    ('44444444-4', 'Ana Martínez', '1995-04-30', '+56945678901', 'ana.martinez@example.com'),
    ('55555555-5', 'Luis Ramírez', '1975-05-05', '+56956789012', 'luis.ramirez@example.com'),
    ('66666666-6', 'Laura Torres', '1988-06-10', '+56967890123', 'laura.torres@example.com'),
    ('77777777-7', 'Pedro Fernández', '1992-07-15', '+56978901234', 'pedro.fernandez@example.com'),
    ('88888888-8', 'Sofía López', '1983-08-20', '+56989012345', 'sofia.lopez@example.com'),
    ('99999999-9', 'Miguel Díaz', '1978-09-25', '+56990123456', 'miguel.diaz@example.com'),
    ('22000003-0', 'Elena Rojas', '1996-10-30', '+56901234567', 'elena.rojas@example.com');

    COMMIT;
    """
)

except Exception as ex:
    print(ex)

finally:
    connection.close()