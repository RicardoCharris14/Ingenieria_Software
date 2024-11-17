document.addEventListener('DOMContentLoaded', function() {
    let selectedElement = null;

    // Hacer que los elementos <li> sean seleccionables
    const listaHoras = document.querySelectorAll('.horas_atencion');
    listaHoras.forEach(function(item) {
        item.addEventListener('click', function() {
            // Desmarcar el elemento previamente seleccionado
            if (selectedElement) {
                selectedElement.classList.remove('selected');
            }
            // Marcar el nuevo elemento seleccionado
            item.classList.add('selected');
            selectedElement = item;
        });
    });

    // Manejar el evento del botón
    const reservarBtn = document.getElementById('reservarBtn');
    reservarBtn.addEventListener('click', function() {
        if (selectedElement) {
            const id = selectedElement.dataset.id;
            const rutPaciente = participantes.paciente
            const rutEspecialista = participantes.especialista

            const data = {
                id: id,
                rutPaciente: rutPaciente,
                rutEspecialista: rutEspecialista
            };

            fetch('/reservar_cita', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.success) {
                    alert('Cita reservada con éxito.');
                    window.location.reload()
                } else {
                    alert('Error al reservar la cita.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al reservar la cita.');
            });

        } else {
            alert('Por favor, seleccione una hora antes de reservar.');
        }
    });
});