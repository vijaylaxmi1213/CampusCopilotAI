let searchHistory = [];
async function sendMessage() {

    let input =
    document.getElementById("userInput").value;

    let output =
    document.getElementById("output");

    output.innerHTML = `
        <div class="result-item">
           <div class="loader"></div>

<p>
    AI Agent is searching the web...
</p>
        </div>
    `;
searchHistory.push(input);

updateHistory();
    try {

        let response = await fetch(
            "http://127.0.0.1:5000/chat",
            {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    message:input
                })
            }
        );

        let data = await response.json();

        console.log(data);

        output.innerHTML = "";

        if(data.summary){

            output.innerHTML += `
                <div class="result-item">
                    <h3>AI Summary</h3>
                    <p>${data.summary}</p>
                </div>
            `;
        }

        if(data.results){

            data.results.forEach(item => {

                output.innerHTML += `

                    <div class="result-item">

                        <a href="${item.link}"
                           target="_blank">

                            ${item.title}

                        </a>

                        <p>
                            ${item.description}
                        </p>

                    </div>
                `;
            });
        }

    } catch(error){

        console.log(error);

        output.innerHTML = `
            <div class="result-item">
                Error connecting to backend
            </div>
        `;
    }
}

function quickSearch(text){

    document.getElementById("userInput").value = text;

    sendMessage();
}
function updateHistory(){

    let historyDiv =
    document.getElementById("history");

    historyDiv.innerHTML = "";

    searchHistory.forEach(item => {

        historyDiv.innerHTML += `

            <div class="history-item"
                 onclick="quickSearch('${item}')">

                ${item}

            </div>
        `;
    });
}