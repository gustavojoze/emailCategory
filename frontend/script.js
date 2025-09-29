

  const qs = (sel, ctx = document) => ctx.querySelector(sel);
  const qsa = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];


  const form           = qs("#form-email");
  const inputArquivo   = qs("#email-arquivo");
  const inputTexto     = qs("#email-texto");
  const btnHistorico   = qs("#btn-historico");
  const btnUpload      = qs("#btn-upload");
  const modalResultado = qs(".container-modalResultado");
  const modalHistorico = qs(".container-modalHistorico");

  const API_BASE = "http://127.0.0.1:5000"; 

  function abrirModal(modal, content) {
    modal.innerHTML = `<div class="modal-content">${content}</div>`;
    modal.style.display = "flex";
    modal.addEventListener("click", e => { if (e.target === modal) fecharModal(modal); });
  }

  function fecharModal(modal) {
    modal.style.display = "none";
    modal.innerHTML = "";
  }



  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = inputArquivo.files[0];
    const texto = (inputTexto?.value || "").trim();

    if (!file && !texto) {
      alert("Digite um email ou selecione um arquivo .pdf/.txt.");
      return;
    }

    const formData = new FormData();
    if (file)  formData.append("email_arquivo", file);
    if (texto) formData.append("email_texto", texto);

    try {
      const resp = await fetch(`${API_BASE}/analisar`, {
        method: "POST",
        body: formData
      });
      const data = await resp.json();

      if (data.erro) {
        alert("Erro: " + data.erro);
        return;
      }

      mostrarModalResultado(data);
    } catch (err) {
      console.error(err);
      alert("Erro ao processar. Verifique se o backend está rodando.");
    } finally {
      inputArquivo.value = "";
      inputTexto.value = "";
    }
  });

  if (btnUpload) {
    btnUpload.addEventListener("click", () => form.requestSubmit());
  }

  function mostrarModalResultado({ email, resposta, categoria }) {
    const content = `
      <h1>Sucesso! ✅🎉</h1>
      <label>Email:</label>
      <p>${email}</p>

      <label>Resposta:</label>
      <p class="resultado-resposta">${resposta}</p>
      <button class="btn-copiar">Copiar Resposta</button>

      <label>Categoria:</label>
      <p>${categoria}</p>

      <button class="btn-fechar" type="button">Fechar</button>
    `;
    abrirModal(modalResultado, content);

    ativarCopiar(".resultado-resposta", modalResultado);
    modalResultado.querySelector(".btn-fechar").addEventListener("click", () => fecharModal(modalResultado));
  }

  async function carregarHistorico() {
    try {
      const resp = await fetch(`${API_BASE}/historico`);
      const data = await resp.json();

      if (!data.length) {
        abrirModal(modalHistorico, `
          <h1>Histórico</h1>
          <p style="margin:.5rem 0 1rem; color:#555">Nenhum item no histórico ainda.</p>
          <button class="btn-fechar">Fechar</button>
        `);
        modalHistorico.querySelector(".btn-fechar").addEventListener("click", () => fecharModal(modalHistorico));
        return;
      }

      const itens = data
        .filter(item => item && item.email && item.categoria && item.resposta)
        .reverse()
        .map(item => `
          <li class="historicoEmail">
            <details>
              <summary>
                <span class="titulo">
                  ${item.email.length > 40 
                    ? item.email.slice(0,40) + "…" 
                    : item.email}
                </span>
                <span class="categoria-badge ${item.categoria === "Produtivo" ? "ok" : "warn"}">
                  ${item.categoria}
                </span>
              </summary>
              <div class="detalhes">
                <label>Email:</label>
                <p>${item.email}</p>
                <label>Resposta:</label>
                <p class="detalhe-resposta">${item.resposta}</p>
                <label>Categoria:</label>
                <p>${item.categoria}</p>
                <button class="detalhe-btnCopiar">Copiar Resposta</button>
              </div>
            </details>
          </li>
        `).join("");

      abrirModal(modalHistorico, `
        <h1>Histórico</h1>
        <ul class="lista-historico">${itens}</ul>
        <button class="btn-fechar">Fechar</button>
      `);

      modalHistorico.querySelector(".btn-fechar").addEventListener("click", () => fecharModal(modalHistorico));
      ativarCopiar(".detalhe-resposta", modalHistorico, ".detalhe-btnCopiar");
    } catch (err) {
      console.error(err);
      alert("Erro ao carregar histórico.");
    }
  }

  if (btnHistorico) {
    btnHistorico.addEventListener("click", e => {
      e.preventDefault();
      carregarHistorico();
    });
  }

  function ativarCopiar(selectorTexto, ctx, btnSelector = ".btn-copiar") {
    qsa(btnSelector, ctx).forEach(btn => {
      btn.addEventListener("click", () => {
        const texto = btn.closest(ctx.className ? `.${ctx.className}` : "body").querySelector(selectorTexto).innerText;
        navigator.clipboard.writeText(texto).then(() => {
          btn.textContent = "Copiado! ✅";
          setTimeout(() => btn.textContent = "Copiar Resposta", 2000);
        }).catch(err => {
          console.error("Erro ao copiar:", err);
          alert("Não foi possível copiar.");
        });
      });
    });
  }
