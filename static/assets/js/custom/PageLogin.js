// Define form element
const form = document.getElementById("kt_sign_in_form");

// Init form validation rules
const validator = FormValidation.formValidation(form, {
  fields: {
    email: {
      validators: {
        notEmpty: {
          message: "O campo de email é obrigatório.",
        },
        emailAddress: {
          message: "Por favor, insira um endereço de email válido.",
        },
      },
    },
    password: {
      validators: {
        notEmpty: {
          message: "O campo de senha é obrigatório.",
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

// Submit button handler
const submitButton = document.getElementById("kt_sign_in_submit");
submitButton.addEventListener("click", function (e) {
  e.preventDefault();

  validator.validate().then(function (status) {
    if (status === "Valid") {
      // Show loading indication
      submitButton.setAttribute("data-kt-indicator", "on");

      // Disable button to avoid multiple clicks
      submitButton.disabled = true;

      // Simulate form submission
      setTimeout(function () {
        submitButton.removeAttribute("data-kt-indicator");
        submitButton.disabled = false;

        // Submit form
        form.submit();
      }, 2000);
    }
  });
});
