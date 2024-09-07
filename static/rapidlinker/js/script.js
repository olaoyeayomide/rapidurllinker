// HAMBURGER
document.addEventListener("DOMContentLoaded", () => {
  const btnOpen = document.querySelector("#btnOpen");
  const btnClose = document.querySelector("#btnClose");
  const media = window.matchMedia("(width < 40em)");
  // const media = window.matchMedia("(max-width: 768px)");
  const topNavMenu = document.querySelector(".topnav__menu");
  const main = document.querySelector("main");
  const body = document.querySelector("body");

  function openMobileMenu() {
    btnOpen.setAttribute("aria-expanded", "true");
    topNavMenu.removeAttribute("inert");
    topNavMenu.removeAttribute("style");
    main.setAttribute("inert", "");
    bodyScrollLockUpgrade.disableBodyScroll(body);
    btnClose.focus();
  }

  function closeMobileMenu() {
    btnOpen.setAttribute("aria-expanded", "false");
    topNavMenu.setAttribute("inert", "");
    main.removeAttribute("inert");
    bodyScrollLockUpgrade.enableBodyScroll(body);
    btnOpen.focus();

    setTimeout(() => {
      topNavMenu.style.transition = "none";
    }, 500);
  }

  function setupTopNav(e) {
    if (e.matches) {
      // is mobile
      console.log("is mobile");
      topNavMenu.setAttribute("inert", "");
      topNavMenu.style.transition = "none";
    } else {
      // is tablet/desktop
      console.log("is desktop");
      closeMobileMenu();
      topNavMenu.removeAttribute("inert");
    }
  }

  setupTopNav(media);

  btnOpen.addEventListener("click", openMobileMenu);
  btnClose.addEventListener("click", closeMobileMenu);

  media.addEventListener("change", function (e) {
    setupTopNav(e);
  });
});

// MODAL
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("result-modal");
  const overlay = document.getElementById("overlay");
  const closeModalBtn = document.getElementById("close-modal");
  const modalGotItBtn = document.getElementById("modal-got-it");

  // Show the modal if there's a shortened URL
  if (modal && modal.querySelector("#shortened-url").textContent) {
    modal.classList.remove("hidden");
    overlay.classList.remove("hidden");
  }

  // Function to close the modal
  const closeModal = function () {
    modal.classList.add("hidden");
    overlay.classList.add("hidden");
  };

  // Close modal on button click
  closeModalBtn.addEventListener("click", closeModal);
  overlay.addEventListener("click", closeModal);
  modalGotItBtn.addEventListener("click", closeModal);

  // Close modal on pressing the Escape key
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !modal.classList.contains("hidden")) {
      closeModal();
    }
  });
});

// TABLE
const search = document.querySelector(".input-group input"),
  table_rows = document.querySelectorAll("tbody tr"),
  table_headings = document.querySelectorAll("thead th");

// 2. Sorting | Ordering data of HTML table

table_headings.forEach((head, i) => {
  let sort_asc = true;
  head.onclick = () => {
    table_headings.forEach((head) => head.classList.remove("active"));
    head.classList.add("active");

    document
      .querySelectorAll("td")
      .forEach((td) => td.classList.remove("active"));
    table_rows.forEach((row) => {
      row.querySelectorAll("td")[i].classList.add("active");
    });

    head.classList.toggle("asc", sort_asc);
    sort_asc = head.classList.contains("asc") ? false : true;

    sortTable(i, sort_asc);
  };
});

function sortTable(column, sort_asc) {
  [...table_rows]
    .sort((a, b) => {
      let first_row = a
          .querySelectorAll("td")
          [column].textContent.toLowerCase(),
        second_row = b.querySelectorAll("td")[column].textContent.toLowerCase();

      return sort_asc
        ? first_row < second_row
          ? 1
          : -1
        : first_row < second_row
        ? -1
        : 1;
    })
    .map((sorted_row) =>
      document.querySelector("tbody").appendChild(sorted_row)
    );
}

document.addEventListener("DOMContentLoaded", function () {
  const copyButtons = document.querySelectorAll(".btn-copy");

  copyButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const urlToCopy = this.getAttribute("data-url");

      navigator.clipboard
        .writeText(urlToCopy)
        .then(() => {
          alert("URL copied to clipboard!");
        })
        .catch((err) => {
          console.error("Failed to copy: ", err);
        });
    });
  });
});
