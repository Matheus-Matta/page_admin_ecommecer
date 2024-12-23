document.addEventListener("DOMContentLoaded", () => {
  const htmlElement = document.documentElement; // Seleciona o elemento <html>
  const bodyElement = document.querySelector("body"); // Seleciona o sidebar
  const themeButtons = document.querySelectorAll('[data-kt-element="mode"]'); // Seleciona os botões do menu

  // Função para alterar o tema
  function setTheme(theme) {
    // Define o tema no elemento <html>
    htmlElement.setAttribute("data-bs-theme", theme);
    localStorage.setItem("theme", theme);

    // Alterna o layout do sidebar
    if (theme === "dark") {
      bodyElement.setAttribute("data-kt-app-layout", "dark-sidebar");
    } else {
      bodyElement.setAttribute("data-kt-app-layout", "light-sidebar");
    }

    // Atualizar o botão ativo
    themeButtons.forEach((button) => {
      const buttonTheme = button.getAttribute("data-kt-value");
      if (buttonTheme === theme) {
        button.classList.add("active"); // Adiciona a classe 'active' ao botão atual
      } else {
        button.classList.remove("active"); // Remove a classe 'active' dos outros botões
      }
    });
  }

  // Verifica se há um tema salvo no localStorage
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    setTheme(savedTheme);
  } else {
    // Define um tema padrão se não houver nenhum salvo
    setTheme("light");
  }

  // Adiciona evento de clique aos botões de tema
  themeButtons.forEach((button) => {
    button.addEventListener("click", (event) => {
      event.preventDefault();
      const selectedTheme = button.getAttribute("data-kt-value");
      setTheme(selectedTheme);
    });
  });
});
