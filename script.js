document.addEventListener("DOMContentLoaded", () => {
  const btnGuardar = document.querySelector(".btn");
  const inputs = document.querySelectorAll('input[type="password"]');

  btnGuardar.addEventListener("click", async (e) => {
    e.preventDefault();

    const nueva_contrasena = inputs[0].value.trim();
    const confirmar_contrasena = inputs[1].value.trim();
    const correo = "usuario@unsaac.edu.pe"; // correo fijo de prueba

    if (!nueva_contrasena || !confirmar_contrasena) {
      alert("Por favor, completa ambos campos.");
      return;
    }

    const datos = {
      correo: correo,
      nueva_contrasena: nueva_contrasena,
      confirmar_contrasena: confirmar_contrasena,
    };

    try {
      const respuesta = await fetch("http://127.0.0.1:5000/actualizar_contrasena", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      });

      const resultado = await respuesta.json();

      if (respuesta.ok) {
        alert(resultado.mensaje);
        inputs[0].value = "";
        inputs[1].value = "";
      } else {
        alert(resultado.error);
      }
    } catch (error) {
      console.error("Error al conectar con el backend:", error);
      alert("No se pudo conectar con el servidor Flask.");
    }
  });
});


// Mostrar / ocultar contraseña
document.querySelectorAll(".toggle-password").forEach(icon => {
  icon.addEventListener("click", () => {
    const input = document.getElementById(icon.getAttribute("data-target"));
    const isPassword = input.type === "password";

    input.type = isPassword ? "text" : "password";
    icon.classList.toggle("fa-eye");
    icon.classList.toggle("fa-eye-slash");
  });
});
