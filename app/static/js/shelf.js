// Clicking a book pulls it off the shelf and opens its details in a modal.

const peek = document.getElementById("peek");

if (peek && typeof peek.showModal === "function") {
  const fields = {
    title: peek.querySelector(".peek__title"),
    byline: peek.querySelector('[data-field="byline"]'),
    status: peek.querySelector('[data-field="status"]'),
    notes: peek.querySelector('[data-field="notes"]'),
    cover: peek.querySelector('[data-field="cover"]'),
  };
  let pulled = null;

  const open = (book) => {
    const d = book.dataset;
    fields.title.textContent = d.title;
    fields.byline.textContent = `${d.author} · ${d.year}`;
    fields.status.textContent = d.rating
      ? `${d.status} · ${"★".repeat(Number(d.rating))}`
      : d.status;
    fields.notes.textContent = d.notes;
    fields.notes.hidden = !d.notes;

    // Every book with cover art shows it here, face out on the shelf or not.
    if (d.cover) {
      fields.cover.src = d.cover;
      fields.cover.alt = `Cover of ${d.title}`;
    }
    fields.cover.hidden = !d.cover;

    pulled?.classList.remove("is-pulled");
    pulled = book;
    book.classList.add("is-pulled");
    peek.showModal();
  };

  document.querySelectorAll(".book").forEach((book) => {
    book.addEventListener("click", () => open(book));
  });

  peek.addEventListener("click", (event) => {
    if (event.target.hasAttribute("data-close")) {
      peek.close();
      return;
    }
    // A click on the backdrop is reported on the <dialog> itself, so compare
    // against the panel's box rather than the event target.
    const box = peek.getBoundingClientRect();
    const outside =
      event.clientX < box.left ||
      event.clientX > box.right ||
      event.clientY < box.top ||
      event.clientY > box.bottom;
    if (outside) peek.close();
  });

  // Fires for the close button, the backdrop, and Escape alike.
  peek.addEventListener("close", () => {
    pulled?.classList.remove("is-pulled");
    pulled = null;
  });
}
