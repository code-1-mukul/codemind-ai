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

        localStorage.setItem(
            "repositoryName",
            data.repository_name
        );

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

    document.getElementById("summary-imports").textContent =
        data.imports;

}

const savedRepository =
    localStorage.getItem("repositoryName");

if (savedRepository) {

    document.getElementById("repository-name").textContent =
        savedRepository;

    loadRepository(savedRepository);
}

function showSection(sectionId) {

    // Hide everything first
    document.getElementById("repository-summary").style.display =
        "none";

    document.querySelector(".upload-card").style.display =
        "none";

    document.getElementById("project-tree").style.display =
        "none";

    document.getElementById("architecture").style.display =
        "none";

    document.getElementById("semantic-search").style.display =
        "none";


    // Show requested section
    if (sectionId === "repository-summary") {

        document.getElementById("repository-summary").style.display =
            "block";

    } else if (sectionId === "upload-card") {

        document.querySelector(".upload-card").style.display =
            "block";

    } else {

        document.getElementById(sectionId).style.display =
            "block";
    }
}

document
    .getElementById("nav-summary")
    .addEventListener("click", function () {

        showSection("repository-summary");

    });

    function renderTree(node) {

        const container = document.createElement("div");

        container.classList.add("tree-node");

        const item = document.createElement("div");

        item.classList.add("tree-item");

        const hasChildren =
            node.children && node.children.length > 0;

        const icon = node.is_directory ? "📁" : "📄";

        const arrow = node.is_directory && hasChildren
            ? "▶ "
            : "";

        item.textContent =
            `${arrow}${icon} ${node.name}`;

        container.appendChild(item);

        if (hasChildren) {

            const childrenContainer =
                document.createElement("div");

            childrenContainer.classList.add(
                "tree-children"
            );

            childrenContainer.style.display = "none";

            node.children.forEach(child => {

                childrenContainer.appendChild(
                    renderTree(child)
                );

            });

            container.appendChild(childrenContainer);

            item.addEventListener("click", function () {

                const isHidden =
                    childrenContainer.style.display === "none";

                childrenContainer.style.display =
                    isHidden ? "block" : "none";

                const newArrow =
                    isHidden ? "▼ " : "▶ ";

                item.textContent =
                    `${newArrow}${icon} ${node.name}`;

            });
        }

        return container;
    }

document
    .getElementById("nav-tree")
    .addEventListener("click", async function () {

        showSection("project-tree");

        const repositoryName =
            localStorage.getItem("repositoryName");

        if (!repositoryName) {
            console.log("No repository loaded.");
            return;
        }

        const response = await fetch(
            `/api/v1/repositories/${repositoryName}/tree`
        );

        const data = await response.json();

        const treeContainer =
            document.getElementById("tree-container");

        treeContainer.innerHTML = "";

        treeContainer.appendChild(
            renderTree(data)
        );
    });

function renderArchitecture(graph) {

            const elements = [];

            graph.nodes.forEach(node => {

                elements.push({
                    data: {
                        id: node.id,
                        label: node.label,
                    }
                });

            });

            graph.edges.forEach(edge => {

                elements.push({
                    data: {
                        id: `${edge.source}-${edge.target}`,
                        source: edge.source,
                        target: edge.target,
                        label: edge.relation,
                    }
                });

            });

            const container =
                document.getElementById(
                    "architecture-graph"
                );

            container.innerHTML = "";

            cytoscape({

                container: container,

                elements: elements,

                style: [
                    {
                        selector: "node",

                        style: {
                            "label": "data(label)",
                            "text-valign": "center",
                            "text-halign": "center",
                            "background-color": "#374151",
                            "color": "#ffffff",
                            "padding": "15px",
                            "shape": "roundrectangle",
                        }
                    },

                    {
                        selector: "edge",

                        style: {
                            "width": 2,
                            "line-color": "#6b7280",
                            "target-arrow-color": "#6b7280",
                            "target-arrow-shape": "triangle",
                            "curve-style": "bezier",
                            "label": "data(label)",
                            "color": "#9ca3af",
                            "font-size": 10,
                        }
                    }
                ],

                layout: {
                    name: "breadthfirst",
                    directed: true,
                    padding: 30,
                    spacingFactor: 1.5,
                }

            });
        }


document
    .getElementById("nav-architecture")
    .addEventListener("click", async function () {

        showSection("architecture");

        const repositoryName =
            localStorage.getItem("repositoryName");

        if (!repositoryName) {
            console.log("No repository loaded.");
            return;
        }

        try {

            const response = await fetch(
                `/api/v1/architecture/repositories/${encodeURIComponent(repositoryName)}/architecture`
            );

            if (!response.ok) {
                throw new Error(
                    `Architecture request failed: ${response.status}`
                );
            }

            const data = await response.json();

            console.log("Architecture:", data);

            // Show Components by default
            renderArchitecture(data.module_graph);


            // Components button
            document
                .getElementById("components-tab")
                .onclick = function () {

                    renderArchitecture(
                        data.module_graph
                    );
                };


            // Data Flow button
            document
                .getElementById("dataflow-tab")
                .onclick = function () {

                    renderArchitecture(
                        data.data_flow
                    );
                };

        } catch (error) {

            console.error(
                "Failed to load architecture:",
                error
            );
        }
    });

document
    .getElementById("nav-search")
    .addEventListener("click", function () {
        showSection("semantic-search");
    });

document
    .getElementById("search-btn")
    .addEventListener("click", async function () {

        const query = document
            .getElementById("search-query")
            .value
            .trim();

        if (!query) {
            alert("Please enter a search query.");
            return;
        }

        const repositoryName =
            localStorage.getItem("repositoryName");

        if (!repositoryName) {
            alert("No repository loaded.");
            return;
        }

        const response = await fetch(
            `/api/v1/repository/${encodeURIComponent(repositoryName)}/search`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    query: query,
                    top_k: 5
                })
            }
        );

        const data = await response.json();

        const resultsContainer =
            document.getElementById("search-results");

        resultsContainer.innerHTML = "";

        if (data.results.length === 0) {
            resultsContainer.innerHTML =
                "<p>No relevant code found.</p>";
            return;
        }

        data.results.forEach((result, index) => {

            const resultCard = document.createElement("div");

            resultCard.classList.add("search-result");

            resultCard.innerHTML = `
                <div class="search-result-header">
                    <div>
                        <strong>${result.file_path}</strong>
                        <span>${result.chunk_name}</span>
                    </div>

                    <span class="search-score">
                        Score: ${result.score.toFixed(3)}
                    </span>
                </div>

                <pre><code>${result.content}</code></pre>
            `;

            resultsContainer.appendChild(resultCard);
        });
    });


