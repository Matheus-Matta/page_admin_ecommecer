document.addEventListener("DOMContentLoaded", function () {
  // Inicializa o stepper
  const stepperElement = document.querySelector("#employeeStepper");
  const form = document.getElementById("form_employee_create");
  const stepper = new KTStepper(stepperElement);

  function swal_required(
    message = "Por favor, preencha os campos obrigatórios antes de continuar.",
    status = "error"
  ) {
    Swal.fire({
      text: message,
      icon: status,
      buttonsStyling: false,
      confirmButtonText: "Ok, entendi!",
      customClass: {
        confirmButton: "btn btn-primary",
      },
    });
  }

  // Função genérica para avançar etapas
  function handleNextStep(validator) {
    const currentStep = stepper.getCurrentStepIndex();
    const totalSteps = stepperElement.querySelectorAll(
      '[data-kt-stepper-element="content"]'
    ).length;
    const stepContent = stepperElement.querySelector(
      `[data-kt-stepper-element="content"]:nth-child(${currentStep})`
    );
    if (currentStep > 3) {
      const name = document.querySelector('input[name="name"').value;
      const emailField = document.getElementById("user_email");
      const passField = document.getElementById("user_pass");
      if (name) {
        const { email, password } = generateEmailAndPassword(name);
        if (!emailField.value) emailField.value = email;
        if (!passField.value) passField.value = password;
      }
    }
    // Valida o conteúdo do passo atual
    validator.validate(stepContent).then(function (status) {
      if (status === "Valid") {
        if (currentStep === totalSteps) {
          const formData = new FormData(form);

          fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
              "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]")
                .value,
            },
          })
            .then((response) => {
              return response.json();
            })
            .then((data) => {
              console.log(data);
              if (data.success) {
                swal_required("Funcionário cadastrado com sucesso!", "success");
                setTimeout(() => window.location.reload(), 1000);
              } else {
                throw new Error(data.message);
              }
            })
            .catch((error) => {
              swal_required(
                error.message ||
                  "Ocorreu um erro inesperado ao enviar o formulário."
              );
            });
        } else {
          stepper.goNext(); // Avança para o próximo passo
        }
      } else {
        swal_required();
      }
    });
  }

  function generateEmailAndPassword(fullName) {
    const firstName = fullName.split(" ")[0]; // Primeiro nome
    const secondName = fullName.split(" ")[1] || ""; // Segundo nome
    const domain = "@maxxxmoveis.com.br";

    // Gera o e-mail com base nos dois primeiros nomes
    const email = `${firstName.toLowerCase()}.${secondName.toLowerCase()}${domain}`;

    // Gera a senha
    const randomNumber = Math.floor(Math.random() * 100) + 1; // Número aleatório até 100
    const password = `${firstName.toLowerCase()}@${randomNumber}`;

    return { email, password };
  }

  // Botão "Voltar"
  stepper.on("kt.stepper.previous", function (stepper) {
    stepper.goPrevious();
  });

  //
  // start config step 1 modal create
  //

  // Aplica máscara de Data de Nascimento (dd/mm/yyyy)
  Inputmask({
    mask: "99/99/9999",
  }).mask("#birth_date");

  // Aplica máscara de CPF (formato brasileiro)
  Inputmask({
    mask: "999.999.999-99",
  }).mask("#cpf");

  // Aplica máscara de RG (formato numérico padrão)
  Inputmask({
    mask: "99.999.999-9",
  }).mask("#rg");

  // Aplica máscara de Telefone (formato brasileiro com DDD)
  Inputmask({
    mask: "(99) 99999-9999",
  }).mask("#phone");

  // Aplica máscara de CNH (número alfanumérico)
  Inputmask({
    mask: "99999999999",
  }).mask("#cnh");

  // Aplica máscara de CTPS (formato numérico com série)
  Inputmask({
    mask: "999.99999.99-9",
  }).mask("#ctps");

  // Aplica máscara de PIS/PASEP (formato padrão)
  Inputmask({
    mask: "999.99999.99-9",
  }).mask("#pis_pasep");

  // Máscara de E-mail
  Inputmask({
    alias: "email",
  }).mask("#email");

  // Aplica máscara para o campo de Horário (HH:MM)
  Inputmask({
    mask: "99:99", // Formato HH:MM
    placeholder: "HH:MM",
    regex: "^([01]\\d|2[0-3]):([0-5]\\d)$", // Garante horas válidas entre 00:00 e 23:59
  }).mask("#start_time");

  Inputmask({
    mask: "99:99",
    placeholder: "HH:MM",
    regex: "^([01]\\d|2[0-3]):([0-5]\\d)$",
  }).mask("#end_time");

  // Máscara de entrada para o campo de salário bruto
  Inputmask({
    alias: "currency",
    prefix: "R$ ",
    groupSeparator: ".",
    radixPoint: ",",
    autoGroup: true,
    digits: 2,
    digitsOptional: false,
    placeholder: "0",
    rightAlign: false,
    removeMaskOnSubmit: true,
  }).mask("#gross_salary");

  const validator_1 = FormValidation.formValidation(form, {
    fields: {
      name: {
        validators: {
          notEmpty: {
            message: "O nome é obrigatório",
          },
        },
      },
      cpf: {
        validators: {
          notEmpty: {
            message: "O CPF é obrigatório",
          },
          regexp: {
            regexp: /^\d{3}\.\d{3}\.\d{3}-\d{2}$/,
            message: "Formato de CPF inválido. Ex.: 123.456.789-00",
          },
        },
      },
      rg: {
        validators: {
          notEmpty: {
            message: "O RG é obrigatório",
          },
        },
      },
      birth_date: {
        validators: {
          notEmpty: {
            message: "A data de nascimento é obrigatória",
          },
          regexp: {
            regexp: /^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[0-2])\/(19|20)\d{2}$/,
            message: "A data de nascimento deve estar no formato DD/MM/YYYY",
          },
        },
      },
      email: {
        validators: {
          notEmpty: {
            message: "O e-mail é obrigatório",
          },
          emailAddress: {
            message: "O e-mail não é válido",
          },
        },
      },
      phone: {
        validators: {
          notEmpty: {
            message: "O telefone é obrigatório",
          },
          regexp: {
            regexp: /^\(\d{2}\) \d{4,5}-\d{4}$/,
            message: "Formato de telefone inválido. Ex.: (11) 98765-4321",
          },
        },
      },
    },
    plugins: {
      trigger: new FormValidation.plugins.Trigger(),
      bootstrap: new FormValidation.plugins.Bootstrap5({
        rowSelector: ".fv-row",
        eleInvalidClass: "",
        eleValidClass: "",
      }),
    },
  });

  //
  // end config step 1 modal create
  //

  //
  // start config step 2 modal create
  //

  const validator_2 = FormValidation.formValidation(form, {
    fields: {
      contract_type: {
        validators: {
          callback: {
            message: "Selecione um tipo de contrato válido.",
            callback: function (input) {
              return (
                input.value !== "" && input.value !== "Selecione uma opção"
              );
            },
          },
        },
      },
      role: {
        validators: {
          callback: {
            message: "Selecione um cargo válido.",
            callback: function (input) {
              return (
                input.value !== "" && input.value !== "Selecione uma opção"
              );
            },
          },
        },
      },
      gross_salary: {
        validators: {
          notEmpty: {
            message: "O salário bruto é obrigatório.",
          },
        },
      },
      start_date: {
        validators: {
          notEmpty: {
            message: "A data de início da vigência é obrigatória.",
          },
        },
      },
    },
    plugins: {
      trigger: new FormValidation.plugins.Trigger(),
      bootstrap: new FormValidation.plugins.Bootstrap5({
        rowSelector: ".fv-row",
        eleInvalidClass: "",
        eleValidClass: "",
      }),
    },
  });

  //
  // end config step 2 modal create
  //

  //
  // start config step 3 modal create
  //

  const validator_3 = FormValidation.formValidation(form, {
    fields: {
      street: {
        validators: {
          notEmpty: {
            message: "A rua é obrigatória.",
          },
        },
      },
      number: {
        validators: {
          notEmpty: {
            message: "O número é obrigatório.",
          },
        },
      },
      city: {
        validators: {
          notEmpty: {
            message: "A cidade é obrigatória.",
          },
        },
      },
      state: {
        validators: {
          notEmpty: {
            message: "O estado é obrigatório.",
          },
        },
      },
      country: {
        validators: {
          notEmpty: {
            message: "O país é obrigatório.",
          },
        },
      },
      postal_code: {
        validators: {
          notEmpty: {
            message: "O CEP é obrigatório.",
          },
          regexp: {
            regexp: /^\d{5}-\d{3}$/,
            message: "Formato de CEP inválido. Ex.: 12345-678",
          },
        },
      },
    },
    plugins: {
      trigger: new FormValidation.plugins.Trigger(),
      bootstrap: new FormValidation.plugins.Bootstrap5({
        rowSelector: ".fv-row",
        eleInvalidClass: "",
        eleValidClass: "",
      }),
    },
  });

  $("#address_repeater").repeater({
    initEmpty: false,
    /**
     * Função que é executada quando um item é adicionado ou mostrado.
     * Adiciona validação dinamicamente para novos campos e atualiza as labels dinamicamente.
     * Além disso, aplica máscaras de entrada para os campos de entrada.
     */
    show: function () {
      // Mostra o item adicionado
      $(this).slideDown();

      // Adiciona validação dinamicamente para novos campos
      const inputs = $(this).find("input");
      inputs.each(function () {
        const name = $(this).attr("name");
        if (name) {
          // Adiciona validação para o campo
          validator_3.addField(name, {
            validators: {
              notEmpty: {
                message: "Este campo é obrigatório.",
              },
            },
          });
        }
      });

      // Atualiza as labels dinamicamente
      updateLabelsStep3();
      // Aplica máscaras de entrada para os campos de entrada
      applyMasks();
    },
    hide(deleteElement) {
      $(this).slideUp(deleteElement);

      const inputs = $(this).find("input");
      inputs.each((_, input) => {
        const name = $(input).attr("name");
        if (name) {
          validator_3.removeField(name);
        }
      });
      updateLabelsStep3();
    },
  });

  /**
   * Atualiza as labels dinamicamente do STEP 3
   *
   * Esta função é executada sempre que um item é adicionado ou removido do
   * repeater do STEP 3. Ela atualiza as labels dinamicamente com o número do
   * item atual.
   */
  function updateLabelsStep3() {
    const items = $("#address_repeater [data-repeater-item]");
    items.each((index, item) => {
      const $label = $(item).find(".repeater-label-step3");
      $label.text(`Endereço ${index + 1}`);
    });
  }

  // Inicializa as labels no carregamento
  updateLabelsStep3();

  function applyMasks() {
    Inputmask({
      mask: "99999-999",
    }).mask("#postal_code");
  }

  applyMasks();

  //
  // end config step 3 modal create
  //

  //
  // start config step 4 modal create
  //

  const validator_4 = FormValidation.formValidation(form, {
    fields: {
      payment_type: {
        validators: {
          notEmpty: {
            message: "O tipo de pagamento é obrigatório.",
          },
        },
      },
      pix_key: {
        validators: {
          callback: {
            message: "A chave PIX é obrigatória para o tipo de pagamento PIX.",
            callback: function (input) {
              const pixKeyGroup = document.getElementById("pix_key_group");
              if (!pixKeyGroup.classList.contains("d-none")) {
                return input.value.trim() !== "";
              }
              return true;
            },
          },
        },
      },
      bank_name: {
        validators: {
          callback: {
            message: "O nome do banco é obrigatório para depósitos.",
            callback: function (input) {
              const bankFields = document.getElementById("bank_fields");
              if (!bankFields.classList.contains("d-none")) {
                return input.value.trim() !== "";
              }
              return true;
            },
          },
        },
      },
      account_number: {
        validators: {
          callback: {
            message: "O número da conta deve conter apenas dígitos.",
            callback: function (input) {
              const bankFields = document.getElementById("bank_fields");
              if (!bankFields.classList.contains("d-none")) {
                return /^\d+$/.test(input.value);
              }
              return true;
            },
          },
        },
      },
      agency_number: {
        validators: {
          callback: {
            message: "O número da agência deve conter apenas dígitos.",
            callback: function (input) {
              const bankFields = document.getElementById("bank_fields");
              if (!bankFields.classList.contains("d-none")) {
                return /^\d+$/.test(input.value);
              }
              return true;
            },
          },
        },
      },
      payment_method: {
        validators: {
          callback: {
            message: "Selecione um metodo válido.",
            callback: function (input) {
              return (
                input.value !== "" && input.value !== "Selecione uma opção"
              );
            },
          },
        },
      },
    },
    plugins: {
      trigger: new FormValidation.plugins.Trigger(),
      bootstrap: new FormValidation.plugins.Bootstrap5({
        rowSelector: ".fv-row",
        eleInvalidClass: "",
        eleValidClass: "",
      }),
    },
  });

  // Aplica máscaras
  Inputmask({
    regex: "\\d{1,20}", // Aceita até 20 dígitos
    placeholder: "",
  }).mask("#account_number");

  Inputmask({
    regex: "\\d{1,10}", // Aceita até 10 dígitos
    placeholder: "",
  }).mask("#agency_number");

  // Configuração de exibição dinâmica
  const paymentType = document.getElementById("payment_type");
  const pixKeyGroup = document.getElementById("pix_key_group");
  const bankFields = document.getElementById("bank_fields");

  paymentType.addEventListener("change", function () {
    const value = this.value;

    // Esconde todos os grupos de campos inicialmente
    pixKeyGroup.classList.add("d-none");
    bankFields.classList.add("d-none");

    // Mostra os campos relevantes com base no tipo de pagamento
    if (value === "pix") {
      pixKeyGroup.classList.remove("d-none");
      // Ativa a validação para PIX
      validator_4.enableValidator("pix_key");
    } else {
      // Desativa a validação para PIX
      validator_4.disableValidator("pix_key");
    }

    if (value === "deposit") {
      bankFields.classList.remove("d-none");
      // Ativa a validação para os campos de banco
      validator_4.enableValidator("bank_name");
      validator_4.enableValidator("account_number");
      validator_4.enableValidator("agency_number");
    } else {
      // Desativa a validação para os campos de banco
      validator_4.disableValidator("bank_name");
      validator_4.disableValidator("account_number");
      validator_4.disableValidator("agency_number");
    }
  });

  //
  // end config step 4 modal create
  //

  //
  // start config step 5 modal create
  //

  var uploadedFiles = [];
  var inputFile = document.getElementById("docs_files_employee"); // O input file oculto
  var dataTransfer = new DataTransfer(); // Objeto para gerenciar os arquivos

  var myDropzone = new Dropzone("#kt_dropzonejs_employee_documents", {
    url: "/", // URL fictícia
    autoProcessQueue: false, // Desativa o envio automático
    addRemoveLinks: true,
    init: function () {
      console.log("Dropzone configurado.");
    },
  });

  myDropzone.on("addedfile", function (file) {
    uploadedFiles.push(file); // Adiciona o arquivo ao array local
    dataTransfer.items.add(file); // Adiciona o arquivo ao DataTransfer
    inputFile.files = dataTransfer.files; // Atualiza o input file com os arquivos
  });

  myDropzone.on("removedfile", function (file) {
    // Remove o arquivo do array local
    uploadedFiles = uploadedFiles.filter((f) => f.name !== file.name);

    // Remove o arquivo do DataTransfer
    const newDataTransfer = new DataTransfer();
    for (let i = 0; i < dataTransfer.items.length; i++) {
      if (dataTransfer.items[i].getAsFile().name !== file.name) {
        newDataTransfer.items.add(dataTransfer.items[i].getAsFile());
      }
    }
    dataTransfer = newDataTransfer; // Atualiza o DataTransfer
    inputFile.files = dataTransfer.files; // Atualiza o input file com os arquivos restantes
  });

  //
  // end config step 5 modal create
  //

  //
  // start config step 6 modal create
  //

  const validator_6 = FormValidation.formValidation(form, {
    fields: {
      user_email: {
        validators: {
          notEmpty: {
            message: "O e-mail de acesso é obrigatório.",
          },
          emailAddress: {
            message: "O e-mail não é válido.",
          },
        },
      },
      user_pass: {
        validators: {
          notEmpty: {
            message: "A senha de acesso é obrigatória.",
          },
          stringLength: {
            min: 8,
            message: "A senha deve ter pelo menos 8 caracteres.",
          },
        },
      },
    },
    plugins: {
      trigger: new FormValidation.plugins.Trigger(),
      bootstrap: new FormValidation.plugins.Bootstrap5({
        rowSelector: ".fv-row",
        eleInvalidClass: "",
        eleValidClass: "",
      }),
    },
  });

  //
  // end config step 6 modal create
  //

  const validators = {
    1: validator_1,
    2: validator_2,
    3: validator_3,
    4: validator_4,
    5: null,
    6: validator_6,
  };

  // Botão "Avançar"
  const nextButton = document.querySelector("#next-step-employee");
  const saveButton = document.querySelector("#save-step-employee");
  nextStep(nextButton);
  nextStep(saveButton);
  function nextStep(element) {
    element.addEventListener("click", function (e) {
      // Obtém o validador para o passo atual
      const currentStep = stepper.getCurrentStepIndex();
      const currentValidator = validators[currentStep];

      if (currentValidator) {
        handleNextStep(currentValidator);
      } else {
        stepper.goNext();
      }
    });
  }
});
