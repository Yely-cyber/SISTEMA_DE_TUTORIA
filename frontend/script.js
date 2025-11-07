// === script.js ===
document.addEventListener("DOMContentLoaded", () => {
  const btnGuardar = document.querySelector(".btn");
  const inputs = document.querySelectorAll('input[type="password"]');

  btnGuardar.addEventListener("click", async (e) => {
    e.preventDefault();

    const nueva_contrasena = inputs[0].value.trim();
    const confirmar_contrasena = inputs[1].value.trim();
    const correo = localStorage.getItem("emailVerificacion");

    if (!correo) {
      mostrarAlerta("No se encontró el correo. Por favor, repite el proceso de recuperación.", "error");
      return;
    }

    if (!nueva_contrasena || !confirmar_contrasena) {
      mostrarAlerta("Por favor, completa ambos campos.", "warning");
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
        mostrarAlerta("✅ " + resultado.mensaje, "success");

        inputs[0].value = "";
        inputs[1].value = "";

        localStorage.removeItem("emailVerificacion");

        setTimeout(() => {
          window.location.href = "../../INICIAR_SESION/frontend/index.html";
        }, 1500);
      } else {
        mostrarAlerta("❌ " + (resultado.mensaje || "Error al cambiar la contraseña"), "error");
      }
    } catch (error) {
      console.error("Error al conectar con el backend:", error);
      mostrarAlerta("⚠️ No se pudo conectar con el servidor Flask.", "error");
    }
  });
});

// === Mostrar / ocultar contraseña ===
document.querySelectorAll(".toggle-password").forEach(icon => {
  icon.addEventListener("click", () => {
    const input = document.getElementById(icon.getAttribute("data-target"));
    const isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password";
    icon.classList.toggle("fa-eye");
    icon.classList.toggle("fa-eye-slash");
  });
});

// === 📢 ALERTAS TIPO CÓMIC ===
function mostrarAlerta(mensaje, tipo = "success") {
  let alertContainer = document.getElementById("alertContainer");

  if (!alertContainer) {
    alertContainer = document.createElement("div");
    alertContainer.id = "alertContainer";
    document.body.appendChild(alertContainer);
  }

  const alerta = document.createElement("div");
  alerta.classList.add("alert", tipo);
  alerta.textContent = mensaje;
  alertContainer.appendChild(alerta);

  setTimeout(() => alerta.remove(), 4000);
}
