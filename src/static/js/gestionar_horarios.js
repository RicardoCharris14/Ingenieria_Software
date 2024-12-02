let selectedRow = null;

function selectRow(row) {
    if (selectedRow) {
        selectedRow.classList.remove('selected');
    }
    selectedRow = row;
    selectedRow.classList.add('selected');
}

function eliminarHorario() {
    if (selectedRow) {
        const disponible = selectedRow.getAttribute('data-disponible');
        if (disponible === '1') {
            const id = selectedRow.getAttribute('data-id');
            fetch(`/eliminar_horario/${id}`, {
                method: 'DELETE'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al eliminar el horario.');
                }
                return response.json();
            })
            .then(result => {
                if (result.success) {
                    selectedRow.remove();
                    selectedRow = null;
                } else {
                    alert('Error al eliminar el horario.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al eliminar el horario.');
            });
        } else {
            alert('Solo se pueden eliminar horarios disponibles.');
        }
    } else {
        alert('Por favor, seleccione un horario para eliminar.');
    }
}