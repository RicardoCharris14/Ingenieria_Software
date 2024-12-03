function eliminarCita(idHorario) {
    fetch(`/eliminar_cita/${idHorario}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(result => {
        if (result.success) {
            location.reload();
        } else {
            alert('Error al eliminar la cita.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error al eliminar la cita.');
    });
}