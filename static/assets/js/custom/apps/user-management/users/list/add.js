"use strict";
var KTUsersAddUser = (function () {
  const modalElement = document.getElementById("kt_modal_add_user"),
        form = modalElement.querySelector("#kt_modal_add_user_form"),
        modal = new bootstrap.Modal(modalElement);

  return {
    init: function () {
      var validator = FormValidation.formValidation(form, {
        fields: {
          user_name: {
            validators: { notEmpty: { message: "Full name is required" } }
          },
          user_email: {
            validators: {
              notEmpty: { message: "Valid email address is required" }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap: new FormValidation.plugins.Bootstrap5({
            rowSelector: ".fv-row",
            eleInvalidClass: "",
            eleValidClass: ""
          })
        }
      });

      const submitButton = modalElement.querySelector('[data-kt-users-modal-action="submit"]');
      submitButton.addEventListener("click", function (event) {
        event.preventDefault();
        validator.validate().then(function (status) {
          if (status === "Valid") {
            Swal.fire({
              text: "Are you sure you want to submit the form?",
              icon: "question",
              showCancelButton: true,
              buttonsStyling: false,
              confirmButtonText: "Yes, submit it!",
              cancelButtonText: "No, cancel",
              customClass: {
                confirmButton: "btn btn-primary",
                cancelButton: "btn btn-default"
              }
            }).then((result) => {
              if (result.isConfirmed) {
                form.submit(); // Form submission
              }
            });
          } else {
            Swal.fire({
              text: "Sorry, looks like there are some errors detected, please try again.",
              icon: "error",
              buttonsStyling: false,
              confirmButtonText: "Ok, got it!",
              customClass: { confirmButton: "btn btn-primary" }
            });
          }
        });
      });

      // Bind cancel and close button actions
      const bindCancelAndCloseActions = function(actionSelector, messageText) {
        const actionElement = modalElement.querySelector(actionSelector);
        actionElement.addEventListener("click", function (event) {
          event.preventDefault();
          Swal.fire({
            text: messageText,
            icon: "warning",
            showCancelButton: true,
            buttonsStyling: false,
            confirmButtonText: "Yes, cancel it!",
            cancelButtonText: "No, return",
            customClass: {
              confirmButton: "btn btn-primary",
              cancelButton: "btn btn-active-light"
            }
          }).then(function (result) {
            if (result.value) {
              form.reset();
              modal.hide();
            } else if (result.dismiss === Swal.DismissReason.cancel) {
              Swal.fire({
                text: "Your form has not been cancelled!",
                icon: "error",
                buttonsStyling: false,
                confirmButtonText: "Ok, got it!",
                customClass: { confirmButton: "btn btn-primary" }
              });
            }
          });
        });
      };

      // Apply to both cancel and close actions
      bindCancelAndCloseActions('[data-kt-users-modal-action="cancel"]', "Are you sure you would like to cancel?");
      bindCancelAndCloseActions('[data-kt-users-modal-action="close"]', "Are you sure you would like to close?");
    }
  };
})();

KTUtil.onDOMContentLoaded(function () {
  KTUsersAddUser.init();
});
