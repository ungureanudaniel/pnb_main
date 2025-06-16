let hot; // Global reference to Handsontable

document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById('vehicleTable');
  const saveButton = document.getElementById('saveButton');

  if (!container || !saveButton) {
    console.error("Essential elements missing: #vehicleTable or #saveButton.");
    return;
  }

  // Load dropdown data
  fetch(dropdownDataUrl)
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch dropdown data");
      return res.json();
    })
    .then(data => {
      // Clean up old instance
      if (hot) hot.destroy();

      // Init Handsontable
      hot = new Handsontable(container, {
        data: [],
        rowHeaders: true,
        colHeaders: [
          'Proprietar', 'Categorie', 'Numar vehicul', 'Zona',
          'Aviz #', 'Data start', 'Data sfarsit', 'Descriere'
        ],
        columns: [
          { data: 0, type: 'text' },
          { data: 1, type: 'dropdown', source: data.categories || [] },
          { data: 2, type: 'text' },
          { data: 3, type: 'dropdown', source: data.areas || [] },
          { data: 4, type: 'text' },
          { data: 5, type: 'date', dateFormat: 'DD-MM-YYYY', correctFormat: true, allowInvalid: false },
          { data: 6, type: 'date', dateFormat: 'DD-MM-YYYY', correctFormat: true, allowInvalid: false },
          { data: 7, type: 'text' }
        ],
        stretchH: 'all',
        minSpareRows: 5,
        width: '100%',
        licenseKey: 'non-commercial-and-evaluation'
      });
    })
    .catch(err => {
      console.error("Dropdown data load failed:", err);
      alert("Could not load dropdown options.");
    });

  // Save handler
  saveButton.addEventListener('click', () => {
    if (!hot) return;

    const rawData = hot.getData();

    const validData = rawData.filter(row =>
      Array.isArray(row) && row.some(cell => cell !== null && cell !== "")
    );

    fetch(vehicleSaveUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify(validData)
    })
      .then(res => {
        if (!res.ok) throw new Error("Server returned an error");
        return res.json();
      })
      .then(data => {
        alert(data.message || "Saved successfully.");
      })
      .catch(err => {
        console.error("Save failed:", err);
        alert("Failed to save vehicle data.");
      });
  });
});
