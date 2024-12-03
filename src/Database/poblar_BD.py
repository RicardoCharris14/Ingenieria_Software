import sqlite3

try:
    connection = sqlite3.connect("./src/Database/bd")
    cursor = connection.cursor()
    cursor.executescript(
    """
    BEGIN;

    INSERT INTO Paciente (rut, nombre, contraseña, fecha_nacimiento, telefono, correo) VALUES
        ('11111111-1', 'Juan Pérez', 'password123', '1980-01-15', '+56912345678', 'juan.perez@example.com'),
        ('22222222-2', 'María González', 'password123', '1990-02-20', '+56923456789', 'maria.gonzalez@example.com'),
        ('33333333-3', 'Carlos Sánchez', 'password123', '1985-03-25', '+56934567890', 'carlos.sanchez@example.com'),
        ('44444444-4', 'Ana Martínez', 'password123', '1995-04-30', '+56945678901', 'ana.martinez@example.com'),
        ('55555555-5', 'Luis Ramírez', 'password123', '1975-05-05', '+56956789012', 'luis.ramirez@example.com'),
        ('66666666-6', 'Laura Torres', 'password123', '1988-06-10', '+56967890123', 'laura.torres@example.com'),
        ('77777777-7', 'Pedro Fernández', 'password123', '1992-07-15', '+56978901234', 'pedro.fernandez@example.com'),
        ('88888888-8', 'Sofía López', 'password123', '1983-08-20', '+56989012345', 'sofia.lopez@example.com'),
        ('99999999-9', 'Miguel Díaz', 'password123', '1978-09-25', '+56990123456', 'miguel.diaz@example.com'),
        ('22000003-0', 'Elena Rojas', 'password123', '1996-10-30', '+56901234567', 'elena.rojas@example.com');

    INSERT INTO Especialista (rut, nombre, contraseña, especialidad, valor_atencion, telefono, correo) VALUES
        ('12345678-9', 'Dr. Juan Pérez', 'password123', 'Cardiología', 50000, '+56912345678', 'juan.perez@hospital.com'),
        ('98765432-1', 'Dra. Beatriz Gómez', 'password123', 'Dermatología', 40000, '+56923456789', 'beatriz.gomez@hospital.com'),
        ('11223344-5', 'Dr. Carlos López', 'password123', 'Neurología', 60000, '+56934567890', 'carlos.lopez@hospital.com'),
        ('22334455-6', 'Dra. Daniela Fernández', 'password123', 'Pediatría', 45000, '+56945678901', 'daniela.fernandez@hospital.com'),
        ('33445566-7', 'Dr. Eduardo Martínez', 'password123', 'Ginecología', 55000, '+56956789012', 'eduardo.martinez@hospital.com'),
        ('44556677-8', 'Dra. Francisca Torres', 'password123', 'Oftalmología', 47000, '+56967890123', 'francisca.torres@hospital.com'),
        ('55667788-9', 'Dr. Gabriel Soto', 'password123', 'Psiquiatría', 52000, '+56978901234', 'gabriel.soto@hospital.com'),
        ('66778899-0', 'Dra. Helena Rojas', 'password123', 'Endocrinología', 48000, '+56989012345', 'helena.rojas@hospital.com'),
        ('77889900-1', 'Dr. Ignacio Vega', 'password123', 'Reumatología', 53000, '+56990123456', 'ignacio.vega@hospital.com'),
        ('88990011-2', 'Dra. Julia Ramírez', 'password123', 'Oncología', 60000, '+56901234567', 'julia.ramirez@hospital.com');

    INSERT INTO Horario_Atencion (fecha, hora_inicio, hora_fin, rut_especialista, disponible) VALUES
        ('2024-12-24', '11:00', '12:00', '12345678-9', 1),
        ('2024-12-23', '13:00', '14:00', '12345678-9', 1),
        ('2024-12-23', '20:00', '21:00', '12345678-9', 1),
        ('2024-12-23', '17:31', '20:00', '12345678-9', 1),
        ('2024-12-20', '08:00', '10:00', '98765432-1', 1),
        ('2024-12-22', '12:00', '14:00', '98765432-1', 1),
        ('2024-12-24', '16:00', '18:00', '98765432-1', 1),
        ('2024-12-21', '09:00', '11:00', '11223344-5', 1),
        ('2024-12-23', '15:00', '17:00', '11223344-5', 1),
        ('2024-12-25', '10:00', '12:00', '11223344-5', 1),
        ('2024-12-21', '10:00', '12:00', '22334455-6', 1),
        ('2024-12-23', '13:00', '15:00', '22334455-6', 1),
        ('2024-12-25', '09:00', '11:00', '22334455-6', 1),
        ('2024-12-20', '11:00', '13:00', '33445566-7', 1),
        ('2024-12-22', '09:00', '11:00', '33445566-7', 1),
        ('2024-12-24', '14:00', '16:00', '33445566-7', 1),
        ('2024-12-21', '08:00', '10:00', '44556677-8', 1),
        ('2024-12-23', '12:00', '14:00', '44556677-8', 1),
        ('2024-12-25', '14:00', '16:00', '44556677-8', 1),
        ('2024-12-20', '13:00', '15:00', '55667788-9', 1),
        ('2024-12-22', '10:00', '12:00', '55667788-9', 1),
        ('2024-12-24', '08:00', '10:00', '55667788-9', 1),
        ('2024-12-21', '14:00', '16:00', '66778899-0', 1),
        ('2024-12-23', '09:00', '11:00', '66778899-0', 1),
        ('2024-12-25', '12:00', '14:00', '66778899-0', 1),
        ('2024-12-20', '10:00', '12:00', '77889900-1', 1),
        ('2024-12-22', '13:00', '15:00', '77889900-1', 1),
        ('2024-12-24', '11:00', '13:00', '77889900-1', 1),
        ('2024-12-21', '08:00', '10:00', '88990011-2', 1),
        ('2024-12-23', '15:00', '17:00', '88990011-2', 1),
        ('2024-12-25', '16:00', '18:00', '88990011-2', 1);

    INSERT INTO Parametro (id, contraseña_admin, fecha_inicio, fecha_final) VALUES (1, 'admin', '2024-12-18', '2024-12-25');

    INSERT INTO Prevision (nombre) VALUES
    ('Colmena'),
    ('Cruz blanca'),
    ('Masvida'),
    ('Banmédica'),
    ('Esencial');

    INSERT INTO Prevision_Especialista (nombre_prevision, rut_especialista) VALUES
    -- Dr. Alejandro Pérez
    ('Colmena', '12345678-9'),
    ('Masvida', '12345678-9'),
    ('Esencial', '12345678-9'),

    -- Dra. Beatriz Gómez
    ('Cruz blanca', '98765432-1'),
    ('Masvida', '98765432-1'),

    -- Dr. Carlos López
    ('Banmédica', '11223344-5'),
    ('Colmena', '11223344-5'),

    -- Dra. Daniela Fernández
    ('Esencial', '22334455-6'),
    ('Masvida', '22334455-6'),
    ('Colmena', '22334455-6'),

    -- Dr. Eduardo Martínez
    ('Banmédica', '33445566-7'),
    ('Cruz blanca', '33445566-7'),

    -- Dra. Francisca Torres
    ('Esencial', '44556677-8'),
    ('Colmena', '44556677-8'),

    -- Dr. Gabriel Soto
    ('Banmédica', '55667788-9'),
    ('Masvida', '55667788-9'),
    ('Esencial', '55667788-9'),

    -- Dra. Helena Rojas
    ('Colmena', '66778899-0'),
    ('Cruz blanca', '66778899-0'),
    ('Esencial', '66778899-0'),

    -- Dr. Ignacio Vega
    ('Masvida', '77889900-1'),
    ('Banmédica', '77889900-1'),

    -- Dra. Julia Ramírez
    ('Esencial', '88990011-2'),
    ('Colmena', '88990011-2'),
    ('Banmédica', '88990011-2');
    COMMIT;
    """
)

except Exception as ex:
    print(ex)

finally:
    connection.close()