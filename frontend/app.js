document.addEventListener('DOMContentLoaded', () => {
    const simulateBtn = document.getElementById('simulate-btn');
    const scenarioInput = document.getElementById('scenario-input');
    const categorySelect = document.getElementById('category-select');
    const backBtn = document.getElementById('back-btn');
    
    const landingSection = document.getElementById('landing-section');
    const resultsSection = document.getElementById('results-section');
    const loadingState = document.getElementById('loading-state');
    
    const elementsToUpdate = {
        scenarioText: document.getElementById('scenario-text-display'),
        scenarioCategory: document.getElementById('scenario-category-badge'),
        mostLikely: document.getElementById('result-most-likely'),
        bestCase: document.getElementById('result-best-case'),
        worstCase: document.getElementById('result-worst-case'),
        risksList: document.getElementById('result-risks'),
        recommendationsList: document.getElementById('result-recommendations')
    };

    // Assuming we are served from FastAPI so we can use relative paths
    // If not, point this to http://localhost:8000
    const API_BASE_URL = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost' 
        ? 'http://localhost:8000' 
        : ''; 

    simulateBtn.addEventListener('click', async () => {
        const scenario = scenarioInput.value.trim();
        const category = categorySelect.value;
        
        if (!scenario) {
            alert("Please enter a scenario.");
            return;
        }

        // Switch to loading state
        simulateBtn.disabled = true;
        simulateBtn.querySelector('.btn-text').textContent = 'Simulating...';
        simulateBtn.querySelector('.loader').classList.remove('hidden');
        loadingState.classList.remove('hidden');

        try {
            const response = await fetch(`${API_BASE_URL}/simulate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ scenario, category })
            });

            if (!response.ok) {
                throw new Error("Failed to fetch simulation results. Backend may be offline.");
            }

            const data = await response.json();
            
            // Populate UI
            elementsToUpdate.scenarioText.textContent = scenario;
            elementsToUpdate.scenarioCategory.textContent = category;
            elementsToUpdate.mostLikely.textContent = data.most_likely;
            elementsToUpdate.bestCase.textContent = data.best_case;
            elementsToUpdate.worstCase.textContent = data.worst_case;
            
            // Populate Lists
            populateList(elementsToUpdate.risksList, data.risks);
            populateList(elementsToUpdate.recommendationsList, data.recommendations);
            
            // Transition UI
            switchSection(landingSection, resultsSection);
            
        } catch (error) {
            console.error("Simulation error:", error);
            alert("An error occurred during simulation. Ensure the FastAPI backend is running and GEMINI_API_KEY is valid.");
        } finally {
            // Restore button state
            simulateBtn.disabled = false;
            simulateBtn.querySelector('.btn-text').textContent = 'Simulate Outcomes';
            simulateBtn.querySelector('.loader').classList.add('hidden');
            loadingState.classList.add('hidden');
        }
    });

    backBtn.addEventListener('click', () => {
        switchSection(resultsSection, landingSection);
    });

    function populateList(ulElement, items) {
        ulElement.innerHTML = '';
        if (!items || items.length === 0) {
            const li = document.createElement('li');
            li.textContent = "None identified.";
            ulElement.appendChild(li);
            return;
        }
        
        items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            ulElement.appendChild(li);
        });
    }

    function switchSection(hideSection, showSection) {
        hideSection.classList.remove('active');
        setTimeout(() => {
            hideSection.classList.add('hidden');
            showSection.classList.remove('hidden');
            
            // Allow display:none to be removed before adding active for transition
            setTimeout(() => {
                showSection.classList.add('active');
            }, 50);
        }, 300); // matches transition time in CSS
    }
});
