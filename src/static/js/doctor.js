// Manejo de la ventana de notificaciones
function toggleNotificaciones() {
    const ventana = document.getElementById('ventanaNotificaciones');
    if (ventana.style.display === 'none') {
        ventana.style.display = 'block'; // Mostrar ventana
    } else {
        ventana.style.display = 'none'; // Ocultar ventana
    }
}