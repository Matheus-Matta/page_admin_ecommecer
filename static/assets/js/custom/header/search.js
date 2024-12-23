document.addEventListener("DOMContentLoaded", () => {
  console.log("search on");
  // Seleção de elementos
  const searchInput = document.querySelector(
    '[data-kt-search-element="input"]'
  );
  const resultsElement = document.querySelector(
    '[data-kt-search-element="results"]'
  );
  const mainElement = document.querySelector('[data-kt-search-element="main"]');
  const emptyElement = document.querySelector(
    '[data-kt-search-element="empty"]'
  );
  const clearButton = document.querySelector(
    '[data-kt-search-element="clear"]'
  );
  const spinnerElement = document.querySelector(
    '[data-kt-search-element="spinner"]'
  );

  if (
    !searchInput ||
    !resultsElement ||
    !mainElement ||
    !emptyElement ||
    !clearButton ||
    !spinnerElement
  ) {
    console.error(
      "Um ou mais elementos necessários não foram encontrados no DOM."
    );
    return;
  }

  // Dados simulados para exibição
  const mockData = {
    links: [
      { name: "Home", url: "/" },
      { name: "Dashboard", url: "/dashboard" },
      { name: "Settings", url: "/settings" },
    ],
    users: [
      {
        name: "John Doe",
        profileUrl: "/user/johndoe",
        email: "john@example.com",
      },
      {
        name: "Jane Smith",
        profileUrl: "/user/janesmith",
        email: "jane@example.com",
      },
    ],
  };

  const displayResults = (searchTerm) => {
    if (!searchTerm) {
      // Mostra o conteúdo principal se a busca estiver vazia
      resultsElement.classList.add("d-none");
      emptyElement.classList.add("d-none");
      mainElement.classList.remove("d-none");
      return;
    }

    const links = mockData.links.filter((link) =>
      link.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const users = mockData.users.filter((user) =>
      user.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (links.length || users.length) {
      const linksHtml = links
        .map(
          (link) =>
            `<div class="d-flex flex-stack py-4"><a href="${link.url}" class="text-hover-primary">${link.name}</a></div>`
        )
        .join("");

      const usersHtml = users
        .map(
          (user) =>
            `<div class="d-flex flex-stack py-4">
                <div>
                  <a href="${user.profileUrl}" class="text-hover-primary fw-bold">${user.name}</a>
                  <div class="text-muted">${user.email}</div>
                </div>
              </div>`
        )
        .join("");

      resultsElement.innerHTML = `
          <div class="mb-4">
            <h5 class="text-muted">Links</h5>
            ${linksHtml || "<p class='text-muted'>Nenhum link encontrado.</p>"}
          </div>
          <div>
            <h5 class="text-muted">Usuários</h5>
            ${
              usersHtml ||
              "<p class='text-muted'>Nenhum usuário encontrado.</p>"
            }
          </div>
        `;
      resultsElement.classList.remove("d-none");
      emptyElement.classList.add("d-none");
      mainElement.classList.add("d-none");
    } else {
      resultsElement.classList.add("d-none");
      emptyElement.classList.remove("d-none");
      mainElement.classList.add("d-none");
    }
  };

  // Eventos
  searchInput.addEventListener("input", (e) => {
    const searchTerm = e.target.value.trim();
    clearTimeout(spinnerElement.timer);

    // Mostra o spinner enquanto processa
    spinnerElement.classList.remove("d-none");

    spinnerElement.timer = setTimeout(() => {
      spinnerElement.classList.add("d-none");
      displayResults(searchTerm);
    }, 500);
  });

  clearButton.addEventListener("click", () => {
    searchInput.value = "";
    displayResults("");
  });
});
