document.addEventListener("DOMContentLoaded", function () {
  var toggle = document.getElementById("navToggle");
  var mobileNav = document.getElementById("mobileNav");

  if (toggle && mobileNav) {
    toggle.addEventListener("click", function () {
      var isOpen = mobileNav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });

    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        mobileNav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Une seule séquence d'entrée orchestrée pour le hero, respectant
  // prefers-reduced-motion (voir CSS : durées ramenées à 0 dans ce cas).
  var hero = document.querySelector(".hero");
  if (hero) {
    hero.style.opacity = "0";
    hero.style.transform = "translateY(8px)";
    requestAnimationFrame(function () {
      hero.style.transition = "opacity 0.5s ease, transform 0.5s ease";
      hero.style.opacity = "1";
      hero.style.transform = "translateY(0)";
    });
  }
});
