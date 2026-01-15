document.addEventListener("DOMContentLoaded", function () {
  // Helper to get Cookie for CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  // Toast Function
  function showToast(title, message, isSuccess = true) {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = "toast-notification";
    if (!isSuccess) toast.style.borderLeftColor = "#ef4444";

    toast.innerHTML = `
            <i class="${
              isSuccess ? "icon-shopping_cart" : "icon-error"
            }" style="${!isSuccess ? "color: #ef4444;" : ""}"></i> 
            <div class="toast-content">
                <span class="toast-title">${title}</span>
                <span class="toast-message">${message}</span>
            </div>
        `;

    container.appendChild(toast);
    void toast.offsetWidth;
    toast.classList.add("show");

    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => {
        toast.remove();
      }, 300);
    }, 3000);
  }

  // Event Delegation for Add-to-Cart Forms
  document.body.addEventListener("submit", function (e) {
    const form = e.target;

    // Check if it's a form and action is related to adding to cart
    if (
      form.tagName === "FORM" &&
      form.action &&
      form.action.includes("/cart/add/")
    ) {
      e.preventDefault();

      const submitBtn = form.querySelector(
        'input[type="submit"], button[type="submit"]'
      );
      let originalText = "";
      let originalValue = "";

      if (submitBtn) {
        originalValue = submitBtn.value;
        originalText = submitBtn.innerText;
        submitBtn.disabled = true;

        if (submitBtn.tagName === "INPUT") {
          submitBtn.value = "Adding...";
        } else {
          submitBtn.innerText = "Adding...";
        }
      }

      const url = form.action;
      const formData = new FormData(form);

      fetch(url, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": csrftoken,
        },
        body: formData,
      })
        .then((response) => {
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.indexOf("application/json") !== -1) {
            return response.json();
          } else {
            // If not JSON, it might be a redirect (e.g. to login)
            // We must manually submit the form to follow the redirect
            // But we must remove the event listener or call submit() on the element directly
            throw new Error("Not a JSON response");
          }
        })
        .then((data) => {
          if (data && data.status === "success") {
            const countElements =
              document.querySelectorAll(".site-cart .count");
            countElements.forEach((el) => {
              el.innerText = data.cart_count;
              el.style.transform = "scale(1.2)";
              setTimeout(() => (el.style.transform = "scale(1)"), 200);
            });
            showToast(
              "Added to Cart",
              data.message || "Product added successfully!"
            );

            // If inside a modal (Quick View), maybe close it?
            // const modal = form.closest('.white-popup');
            // if(modal) $.magnificPopup.close();
            // Currently keeping it open allows multiple adds.
          } else {
            window.location.href = "/cart/";
          }
        })
        .catch((error) => {
          console.log("Ajax failed, fallback to normal submit");
          form.submit();
        })
        .finally(() => {
          if (submitBtn) {
            submitBtn.disabled = false;
            if (submitBtn.tagName === "INPUT") {
              submitBtn.value = originalValue;
            } else {
              submitBtn.innerText = originalText;
            }
          }
        });
    }
  });
});
