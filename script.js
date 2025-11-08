// THEME + ANIMATION + MODAL + FILTER
document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("theme-toggle");
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme === "dark") document.documentElement.setAttribute("data-theme", "dark");
  updateIcon();

  themeToggle.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    if (current === "dark") {
      document.documentElement.removeAttribute("data-theme");
      localStorage.removeItem("theme");
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      localStorage.setItem("theme", "dark");
    }
    updateIcon();
  });

  function updateIcon() {
    themeToggle.textContent = document.documentElement.getAttribute("data-theme") === "dark" ? "☀️" : "🌙";
  }

  document.getElementById("year").textContent = new Date().getFullYear();

  // Section animation
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll(".animated-section").forEach(sec => observer.observe(sec));

  // Project Filters
  const filters = document.querySelectorAll(".filter-btn");
  const search = document.getElementById("project-search");
  const cards = document.querySelectorAll(".project-card");

  filters.forEach(btn => {
    btn.addEventListener("click", () => {
      filters.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      filterProjects();
    });
  });

  search?.addEventListener("input", filterProjects);

  function filterProjects() {
    const active = document.querySelector(".filter-btn.active")?.dataset.filter || "all";
    const query = search?.value.toLowerCase() || "";
    cards.forEach(card => {
      const tags = card.dataset.tags.toLowerCase();
      const title = card.dataset.title.toLowerCase();
      const matchFilter = active === "all" || tags.includes(active);
      const matchSearch = title.includes(query);
      card.style.display = matchFilter && matchSearch ? "" : "none";
    });
  }

  // Modal
  const modal = document.getElementById("project-modal");
  if (modal) {
    const modalImg = document.getElementById("modal-img");
    const modalTitle = document.getElementById("modal-title");
    const modalDesc = document.getElementById("modal-desc");
    const modalTech = document.getElementById("modal-tech");
    const modalLive = document.getElementById("modal-live");
    const modalGit = document.getElementById("modal-github");

    document.querySelectorAll(".details-btn").forEach(btn => {
      btn.addEventListener("click", e => {
        const card = e.target.closest(".project-card");
        modalImg.src = card.querySelector("img").src;
        modalTitle.textContent = card.dataset.title;
        modalDesc.textContent = card.dataset.description;
        modalTech.textContent = card.dataset.tech;
        modalLive.href = card.dataset.live;
        modalGit.href = card.dataset.github;
        modal.classList.add("active");
      });
    });

    modal.querySelector(".modal-close").addEventListener("click", () => {
      modal.classList.remove("active");
    });

    modal.addEventListener("click", e => {
      if (e.target === modal) modal.classList.remove("active");
    });
  }
});
