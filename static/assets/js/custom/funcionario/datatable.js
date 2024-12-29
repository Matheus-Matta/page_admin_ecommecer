let isExporting = false;
var start = moment().subtract(29, "days");
var end = moment();

$("#startDateEmployee").flatpickr({
  dateFormat: "d/m/Y",
  locale: flatpickr.l10ns.pt, // Aplica o idioma português
});

$("#endDateEmployee").flatpickr({
  dateFormat: "d/m/Y",
  locale: flatpickr.l10ns.pt, // Aplica o idioma português
});

const url = document.getElementById("employeeTable").getAttribute("data-url");

const table = $("#employeeTable").DataTable({
  ajax: {
    url: $("#employeeTable").data("url"), // URL do backend Django
    type: "GET",
    data: function (d) {
      // Adiciona os filtros ao objeto enviado
      d.start_date = $("#startDateEmployee").val(); // Data Inicial
      d.end_date = $("#endDateEmployee").val(); // Data Final
      d.roles = $("#roleFilterEmployee").val(); // IDs dos cargos selecionados
      d.status = $("#statusFilterEmployee").val(); // Situações selecionadas
      if (isExporting) {
        d.export = true; // Adiciona o parâmetro export quando necessário
      }
    },
    dataSrc: "data", // DataTables busca os dados no campo "data"
  },
  columns: [
    {
      data: "user",
      render: function (data, type, row) {
        // Renderiza o campo `user` com HTML para avatar e detalhes do usuário
        let img = `<a href="apps/user-management/users/view.html"><div class="symbol-label fs-3 bg-light-danger text-danger">M</div></a>`;
        if (data.profile) {
          img = `<a href="apps/user-management/users/view.html"><div class="symbol-label"><img src="${data.profile.url}" alt="${data.name}" class="w-100"/></div></a>`;
        }
        return `
          <div class="d-flex align-items-center">
            <div class="symbol symbol-circle symbol-50px overflow-hidden me-3">
            ${img}
            </div>
            <div class="d-flex flex-column">
              <a href="apps/user-management/users/view.html" class="text-gray-800 text-hover-primary mb-1">
                ${data.name}
              </a>
              <span>${data.email}</span>
            </div>
          </div>`;
      },
    },
    { data: "role" },
    {
      data: "last_login",
    },
    {
      data: "situacao",
      render: function (data) {
        // Declarando userStatus localmente
        const userStatus = {
          active: { title: "Ativo", state: "success" },
          on_advanve: { title: "De Ferias", state: "warning" },
          on_leave: { title: "De Licença", state: "info" },
          terminated: { title: "Demitido", state: "danger" },
        };

        if (!data || !userStatus[data]) return "Sem dados";
        return `<span class="ms-2 badge badge-light-${userStatus[data]["state"]} fw-semibold p-6 py-2">${userStatus[data]["title"]}</span>`;
      },
    },
    {
      data: "joined_date",
    },
    {
      data: "user",
      orderable: false,
      render: function (data) {
        return `<a href="#" class="btn btn-light btn-active-light-primary btn-flex btn-center btn-sm" data-kt-menu-trigger="click" data-kt-menu-placement="bottom-end">Ver Perfil</a>`;
      },
      createdCell: function (td, cellData, rowData, row, col) {
        $(td).addClass("text-end");
      },
    },
  ],
  language: {
    sEmptyTable: "Nenhum dado disponível na tabela",
    sInfo: "Mostrando _START_ até _END_ de _TOTAL_ registros",
    sInfoEmpty: "Mostrando 0 até 0 de 0 registros",
    sInfoFiltered: "(filtrado de _MAX_ registros no total)",
    sInfoPostFix: "",
    sInfoThousands: ".",
    sLoadingRecords: "Carregando...",
    sProcessing: "Processando...",
    sSearch: "Buscar:",
    sZeroRecords: "Nenhum registro encontrado",
    oAria: {
      sSortAscending: ": Ordenar colunas de forma ascendente",
      sSortDescending: ": Ordenar colunas de forma descendente",
    },
  },
  pageLength: 10, // Quantidade de registros por página
  serverSide: true, // Habilitar processamento no servidor
  processing: true, // Exibir loader durante requisições
  order: [[0, "asc"]], // Ordena pela primeira coluna (Nome do usuário) por padrão
});

// Evento para capturar o valor do campo de busca e aplicar ao DataTables
$("#searchEmployee").on("keyup", function () {
  table.search(this.value).draw(); // Aplica a busca no DataTables
});

// Aplica os filtros ao clicar no botão "Aplicar"
$("#applyFiltersEmployee").on("click", function () {
  table.ajax.reload(); // Recarrega a tabela com os novos filtros
});

$("#resetFiltersEmployee").on("click", function () {
  // Limpa os valores dos filtros
  $("#roleFilterEmployee").val(null).trigger("change");
  $("#statusFilterEmployee").val(null).trigger("change");

  const startPicker = $("#startDateEmployee").flatpickr();
  const endPicker = $("#endDateEmployee").flatpickr();

  if (startPicker) startPicker.clear();
  if (endPicker) endPicker.clear();

  // Remove os parâmetros extras dos filtros no DataTables
  table.ajax.params().start_date = "";
  table.ajax.params().end_date = "";
  table.ajax.params().roles = [];
  table.ajax.params().status = [];

  // Recarrega a tabela sem filtros
  table.ajax.reload();
});

const exportButtons = () => {
  const documentTitle = "Relatório de Funcionários";

  const exportData = (type) => {
    const params = {
      start_date: $("#startDateEmployee").val(),
      end_date: $("#endDateEmployee").val(),
      roles: $("#roleFilterEmployee").val(),
      status: $("#statusFilterEmployee").val(),
      export: true, // Sinaliza que é uma exportação
    };

    $.ajax({
      url: $("#employeeTable").data("url"),
      type: "GET",
      data: params,
      success: function (response) {
        const data = response.data;

        // Configurações de exportação
        const exportConfig = {
          copy: () => {
            const copyData = data.map((row) => {
              return [
                row.user.name,
                row.user.email,
                row.role,
                row.last_login,
                row.situacao,
                row.joined_date,
              ].join("\t");
            });
            navigator.clipboard.writeText(copyData.join("\n"));
            alert("Dados copiados para a área de transferência!");
          },
          excel: () => {
            const workbook = XLSX.utils.book_new();

            // Dados com cabeçalhos traduzidos
            const worksheetData = [
              [
                "Nome",
                "E-mail",
                "Cargo",
                "Último Login",
                "Situação",
                "Data de Admissão",
              ], // Cabeçalhos
              ...data.map((row) => [
                row.user.name,
                row.user.email,
                row.role,
                row.last_login,
                row.situacao,
                row.joined_date,
              ]),
            ];

            // Criação da planilha
            const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);

            // Estilos (opcional) - somente com bibliotecas adicionais como XLSX-Style
            // worksheet['A1'].s = { font: { bold: true } };

            XLSX.utils.book_append_sheet(workbook, worksheet, "Funcionários");
            XLSX.writeFile(workbook, "Relatorio_Funcionarios.xlsx");
          },
          csv: () => {
            const csvData = [
              `"Nome","E-mail","Cargo","Último Login","Situação","Data de Admissão"`, // Cabeçalhos
              ...data.map((row) =>
                [
                  `"${row.user.name}"`,
                  `"${row.user.email}"`,
                  `"${row.role}"`,
                  `"${row.last_login}"`,
                  `"${row.situacao}"`,
                  `"${row.joined_date}"`,
                ].join(",")
              ),
            ];

            const blob = new Blob([csvData.join("\n")], {
              type: "text/csv;charset=utf-8;",
            });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "Relatorio_Funcionarios.csv";
            link.click();
          },
          pdf: () => {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF({
              orientation: "landscape", // Configuração de orientação
              unit: "pt", // Unidade de medida
              format: "A4", // Tamanho do papel
            });

            // Título do documento
            doc.setFontSize(14);
            doc.text(documentTitle, 40, 30);

            // Cabeçalhos e dados
            const headers = [
              [
                "Nome",
                "E-mail",
                "Cargo",
                "Último Login",
                "Situação",
                "Data de Admissão",
              ],
            ];
            const rows = data.map((row) => [
              row.user.name,
              row.user.email,
              row.role,
              row.last_login,
              row.situacao,
              row.joined_date,
            ]);

            // Configuração da tabela
            doc.autoTable({
              startY: 50, // Início da tabela no eixo Y
              head: headers,
              body: rows,
              styles: {
                fontSize: 10, // Tamanho da fonte
                cellPadding: 5, // Espaçamento interno das células
              },
              headStyles: {
                fillColor: [0, 102, 204], // Cor do fundo do cabeçalho
                textColor: [255, 255, 255], // Cor do texto do cabeçalho
                fontSize: 12, // Tamanho da fonte do cabeçalho
              },
              alternateRowStyles: {
                fillColor: [240, 240, 240], // Cor das linhas alternadas
              },
            });

            // Salvar o documento
            doc.save("Relatorio_Funcionarios.pdf");
          },
        };

        if (exportConfig[type]) {
          exportConfig[type](); // Executa apenas se o tipo existir no mapeamento
        } else {
          console.error(`Tipo de exportação "${type}" inválido.`);
        }
      },
      error: function () {
        alert("Erro ao exportar os dados!");
      },
    });
  };

  // Configura os botões de exportação
  document
    .querySelectorAll("#kt_datatable_employee_export_menu [data-kt-export]")
    .forEach((button) => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const exportType = button.getAttribute("data-kt-export");
        exportData(exportType);
      });
    });
};

// Inicializa os botões de exportação
exportButtons();

function formatDateDifference(dateString) {
  const now = new Date(); // Data atual
  const targetDate = new Date(dateString); // Data fornecida
  const differenceInMs = now - targetDate; // Diferença em milissegundos

  const oneMinute = 60 * 1000;
  const oneHour = 60 * oneMinute;
  const oneDay = 24 * oneHour;
  const oneWeek = 7 * oneDay;
  const oneMonth = 30 * oneDay;
  const oneYear = 365 * oneDay;

  if (differenceInMs < oneHour) {
    const minutes = Math.floor(differenceInMs / oneMinute);
    return `${minutes} minuto${minutes === 1 ? "" : "s"} atrás`;
  } else if (differenceInMs < oneDay) {
    const hours = Math.floor(differenceInMs / oneHour);
    return `${hours} hora${hours === 1 ? "" : "s"} atrás`;
  } else if (differenceInMs < oneWeek) {
    const days = Math.floor(differenceInMs / oneDay);
    return `${days} dia${days === 1 ? "" : "s"} atrás`;
  } else if (differenceInMs < oneMonth) {
    const weeks = Math.floor(differenceInMs / oneWeek);
    return `${weeks} semana${weeks === 1 ? "" : "s"} atrás`;
  } else if (differenceInMs < oneYear) {
    const months = Math.floor(differenceInMs / oneMonth);
    return `${months} mês${months === 1 ? "" : "es"} atrás`;
  } else {
    const years = Math.floor(differenceInMs / oneYear);
    return `${years} ano${years === 1 ? "" : "s"} atrás`;
  }
}
