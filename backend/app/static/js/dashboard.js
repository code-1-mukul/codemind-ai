console.log("Dashboard JS Loaded");

const analyzeButton = document.getElementById("analyze-btn");

analyzeButton.addEventListener("click", cloneRepository);

async function cloneRepository() {

    const repositoryUrl =
        document.getElementById("repo-url").value.trim();

    if (repositoryUrl === "") {

        alert("Please enter a GitHub repository URL.");

        return;
    }

    const response = await fetch(
        "/api/v1/repositories/clone",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                repo_url: repositoryUrl
            })
        }
    );

    const data = await response.json();

    if (data.success) {

        document.getElementById("repository-name").textContent =
            data.repository_name;

        alert(data.message);

        await analyzeRepository(data.repository_name);
        await loadRepository(data.repository_name);

    }
    else {

        alert(data.message);
    }

}

async function analyzeRepository(repositoryName) {

    const response = await fetch(
        `/api/v1/repository/${repositoryName}/analyze`,
        {
            method: "POST"
        }
    );
 
    const data = await response.json();

    console.log(data);
}

async function loadRepository(repositoryName) {

    const response = await fetch(
        `/api/v1/dashboard/${repositoryName}/summary`
    );

    const data = await response.json();

    document.getElementById("summary-repository-name").textContent =
        data.repository_name;

    document.getElementById("summary-status").textContent =
        data.status;

    document.getElementById("summary-python-files").textContent =
        data.python_files;

    document.getElementById("summary-classes").textContent =
        data.classes;

    document.getElementById("summary-functions").textContent =
        data.functions;

    document.getElementById("summary-chunks").textContent =
        data.chunks;

}