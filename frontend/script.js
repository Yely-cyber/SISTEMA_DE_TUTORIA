const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const respuesta = await fetch("http://127.0.0.1:5000/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await respuesta.json();

    if (data.success) {
      mostrarAlerta("✅ " + data.message, "success");
      console.log("Token:", data.token);
      // window.location.href = "dashboard.html";
    } else {
      mostrarAlerta("❌ " + data.message, "error");
    }
  } catch (error) {
    mostrarAlerta("⚠️ Error al conectar con el servidor.", "warning");
    console.error(error);
  }
});

// --- Función para crear alertas dinámicamente ---
function mostrarAlerta(mensaje, tipo = "success") {
  const alertContainer = document.getElementById("alertContainer");
  const alerta = document.createElement("div");
  alerta.classList.add("alert", tipo);
  alerta.textContent = mensaje;
  alertContainer.appendChild(alerta); 

  // Se elimina automáticamente después de 4 segundos
  setTimeout(() => {
    alerta.remove();
  }, 4000);
}
