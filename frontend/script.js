// frontend/script.js

async function searchFaculty() {

    const query =
        document.getElementById("query").value.trim();

    const resultsDiv =
        document.getElementById("results");

    if (!query) {

        resultsDiv.innerHTML = `
            <div class="no-results">
                Please enter a search query.
            </div>
        `;

        return;
    }

    resultsDiv.innerHTML = `
        <div class="loading-box">
            Searching Faculty...
        </div>
    `;

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/search?query=${encodeURIComponent(query)}`
        );

        const data = await response.json();

        resultsDiv.innerHTML = "";

        if (!data.results || data.results.length === 0) {

            resultsDiv.innerHTML = `
                <div class="no-results">
                    No matching faculty found.
                </div>
            `;

            return;
        }

        data.results.forEach((prof) => {

            resultsDiv.innerHTML += `

            <div class="faculty-card">

                <h2>${prof.name}</h2>

                ${
                    prof.specialization
                    ? `
                    <div class="section">
                        <h3>Research Areas</h3>
                        <p>${prof.specialization}</p>
                    </div>
                    `
                    : ""
                }

                ${
                    prof.teaching
                    ? `
                    <div class="section">
                        <h3>Teaching</h3>
                        <p>${prof.teaching}</p>
                    </div>
                    `
                    : ""
                }

                ${
                    prof.biography
                    ? `
                    <div class="section">
                        <h3>About</h3>
                        <p>${prof.biography}</p>
                    </div>
                    `
                    : ""
                }

                <div class="bottom">

                    ${
                        prof.email
                        ? `
                        <span class="email">
                            📧 ${prof.email}
                        </span>
                        `
                        : ""
                    }

                    ${
                        prof.phone
                        ? `
                        <span class="phone">
                            📞 ${prof.phone}
                        </span>
                        `
                        : ""
                    }

                </div>

                ${
                    prof.source_url
                    ? `
                    <a
                        href="${prof.source_url}"
                        target="_blank"
                        class="profile-btn"
                    >
                        View Full Profile
                    </a>
                    `
                    : ""
                }

            </div>

            `;
        });

    } catch (error) {

        console.error(error);

        resultsDiv.innerHTML = `
            <div class="no-results">
                Backend connection failed.
            </div>
        `;
    }
}

document
    .getElementById("query")
    .addEventListener(
        "keypress",
        function(event) {

            if (event.key === "Enter") {

                searchFaculty();
            }
        }
    );