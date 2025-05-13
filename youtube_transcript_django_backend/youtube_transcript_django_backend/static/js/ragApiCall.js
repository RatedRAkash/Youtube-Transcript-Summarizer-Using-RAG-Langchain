document.getElementById('ragForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent default form submission

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const youtubeLink = document.getElementById('youtubeLink').value;
    const query = document.getElementById('query').value;

    loader.style.display = 'block'; // SHOW LOADER
    document.getElementById('summaryOutput').innerText = '' // Blank Text

    // Calling API via AJAX
    fetch("/api/get-summary", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken,
        },
        body: new URLSearchParams({
          youtube_url: youtubeLink,
          user_query: query,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.summary) {
          loader.style.display = 'none'; // HIDE LOADER
          document.getElementById('summaryOutput').innerText = data.summary;
        }
        else if (data.errors) {
          loader.style.display = 'none'; // HIDE LOADER
          document.getElementById('summaryOutput').innerText = 'Form error: ' + JSON.stringify(data.errors);
        }
    })
    .catch(error => {
        loader.style.display = 'none'; // HIDE LOADER
        document.getElementById('summaryOutput').innerText = 'Request failed: ' + error;
    });
});