document.addEventListener("DOMContentLoaded", () => {
  const menuLinks = document.querySelectorAll(
    "#kt_app_sidebar_menu_wrapper .menu-link"
  ); // Seleciona todos os links do menu

  // URL atual da página
  const currentUrl = window.location.pathname;

  // Itera sobre os links e adiciona a classe 'active' se corresponder à URL atual
  menuLinks.forEach((link) => {
    if (link.getAttribute("href") === currentUrl) {
      link.classList.add("active");
      const menuItem = link.closest(".menu-item"); // Seleciona o item do menu pai
      if (menuItem) {
        menuItem.classList.add("active", "show"); // Garante que o menu pai também fique ativo
      }
    } else {
      link.classList.remove("active"); // Remove 'active' de links que não correspondem
    }
  });
});
