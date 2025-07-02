async function fetchData() {
    const res = await fetch('/api/events');
    const events = await res.json();
    const container = document.getElementById("output");
    container.innerHTML = "";

    events.forEach(ev => {
        const div = document.createElement("div");
        div.textContent = ev;
        container.appendChild(div);
    });
}

fetchData();
setInterval(fetchData, 15000);
