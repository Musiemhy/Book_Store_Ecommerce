document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.getElementById("searchButton");
  const searchQuery = document.getElementById("searchQuery");
  const authorFilter = document.getElementById("authorFilter");
  const publisherFilter = document.getElementById("publisherFilter");
  const yearFilter = document.getElementById("yearFilter");
  const resultsSection = document.getElementById("results");

  // Populate filters with options from the backend
  fetch("/filters")
    .then((response) => response.json())
    .then((data) => {
      populateFilterOptions(authorFilter, data.authors);
      populateFilterOptions(publisherFilter, data.publishers);
      populateFilterOptions(yearFilter, data.years);
    });

  // Handle search
  searchButton.addEventListener("click", () => {
    const query = searchQuery.value.trim();
    const author = authorFilter.value;
    const publisher = publisherFilter.value;
    const year = yearFilter.value;

    if (!query && !author && !publisher && !year) {
      alert("Please use at least one method for filtering or searching.");
      return;
    }

    const payload = {};
    if (query) payload.query = query;
    if (author) payload.author = author;
    if (publisher) payload.publisher = publisher;
    if (year) payload.year = year;

    fetch("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => displayResults(data.embedding_results))
      .catch((error) => console.error("Error:", error));
  });

  function populateFilterOptions(selectElement, options) {
    options.forEach((option) => {
      const opt = document.createElement("option");
      opt.value = option;
      opt.textContent = option;
      selectElement.appendChild(opt);
    });
  }

  function displayResults(results) {
    resultsSection.innerHTML = "";
    results.forEach((result) => {
      const item = document.createElement("div");
      item.className = "result-item";
      item.innerHTML = `
                <img src="${result.image_url_m}" alt="${result.book_title}">
                <h3>${result.book_title}</h3>
                <p><strong>Author:</strong> ${result.book_author}</p>
                <p><strong>Publisher:</strong> ${result.publisher}</p>
                <p><strong>Year:</strong> ${result.year_of_publication}</p>
            `;
      resultsSection.appendChild(item);
    });
  }
});
