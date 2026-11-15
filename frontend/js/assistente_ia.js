const chatBox = document.getElementById("chat-box");
const inputPergunta = document.getElementById("input-pergunta");
const btnEnviar = document.getElementById("btn-enviar");

// Permite enviar apertando a tecla Enter
function verificarEnter(event) {
    if (event.key === "Enter") {
        enviarPergunta();
    }
}

// Adiciona balões de mensagem na tela
function adicionarMensagem(remetente, texto, isUsuario = false) {
    const wrapper = document.createElement("div");
    wrapper.className = `d-flex flex-column ${isUsuario ? "align-items-end" : "align-items-start"} mb-3`;

    const badge = document.createElement("span");
    badge.className = `badge ${isUsuario ? "bg-primary" : "bg-secondary"} mb-1`;
    badge.innerText = remetente;

    const bolha = document.createElement("div");
    bolha.className = `p-3 rounded ${isUsuario ? "bg-primary text-white" : "bg-body-tertiary border border-secondary text-light"}`;
    bolha.style.maxWidth = "80%";
    bolha.style.whiteSpace = "pre-wrap"; // Mantém quebras de linha da resposta da IA
    bolha.innerText = texto;

    wrapper.appendChild(badge);
    wrapper.appendChild(bolha);
    chatBox.appendChild(wrapper);

    // Rola automaticamente para a última mensagem
    chatBox.scrollTop = chatBox.scrollHeight;
    return wrapper;
}

async function enviarPergunta() {
    const pergunta = inputPergunta.value.trim();
    if (!pergunta) return;

    // Mostra a pergunta do usuário na tela e limpa o input
    adicionarMensagem("Você", pergunta, true);
    inputPergunta.value = "";
    inputPergunta.disabled = true;
    btnEnviar.disabled = true;

    // Mostra uma mensagem enquanto a IA processa os dados
    const loadingMsg = adicionarMensagem("Gabrielzinho IA", "⏳ Analisando dados da oficina...", false);

    try {
        // Faz a requisição POST
        const response = await fetch("http://127.0.0.1:8000/perguntar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ pergunta: pergunta })
        });

        const data = await response.json();

        // Remove o aviso de carregamento e mostra a resposta real
        chatBox.removeChild(loadingMsg);
        
        if (response.ok) {
            adicionarMensagem("Gabrielzinho IA", data.resposta, false);
        } else {
            adicionarMensagem("Gabrielzinho IA", "❌ Erro ao processar a pergunta no servidor.", false);
        }

    } catch (error) {
        chatBox.removeChild(loadingMsg);
        adicionarMensagem("Gabrielzinho IA", "❌ Não foi possível conectar ao servidor FastAPI (porta 8000).", false);
        console.error(error);
    } finally {
        inputPergunta.disabled = false;
        btnEnviar.disabled = false;
        inputPergunta.focus();
    }
}