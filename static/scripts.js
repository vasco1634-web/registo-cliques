function clicar(botao) {
    fetch('/clique', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ botao: botao })
    })
    .then(response => response.json())
    .then(dados => {
        document.getElementById('resultado').innerText =
            `Clique nº ${dados.contador} | Data: ${dados.data} | Hora: ${dados.hora}`;
    });
}
