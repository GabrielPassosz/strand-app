let lang = "en",
  page = "login",
  tab = "profile",
  selected = null,
  query = "",
  currency = "USD",
  zone = "America/New_York",
  user = null,
  showArchived = false,
  authMode = "login";
const T = {
  en: {
    workspace: "Your workspace",
    clients: "Clients",
    settings: "Settings",
    plan: "Subscription",
    folio: "CLIENT FOLIO",
    professional: "Independent stylist",
    title: "Every client. Every detail.",
    subtitle: "Your craft, beautifully remembered.",
    newClient: "Add client",
    total: "Total clients",
    visits: "Recorded visits",
    formulas: "Color formulas",
    yourClients: "Your clients",
    search: "Search by name or phone…",
    all: "All clients",
    profile: "Hair profile",
    history: "Visit history",
    photos: "Photos",
    edit: "Edit profile",
    newVisit: "New visit",
    overview: "Client details",
    email: "Email",
    phone: "Phone",
    birthday: "Birthday",
    lastVisit: "Last visit",
    hair: "Hair characteristics",
    texture: "Strand thickness",
    pattern: "Curl pattern",
    length: "Length",
    porosity: "Porosity",
    elasticity: "Elasticity",
    notes: "Preferences & care notes",
    lastFormula: "Latest color formula",
    seeHistory: "View history",
    noVisit: "No visits yet",
    memory: "Good hair starts with knowing your client.",
    memoryText: "Keep their formulas, preferences and progress in one place.",
    name: "Full name",
    save: "Save changes",
    cancel: "Cancel",
    close: "Close",
    saved: "Changes saved.",
    created: "Client added.",
    required: "Complete the required fields.",
    consult: "Consultation",
    service: "Service",
    date: "Date",
    price: "Price",
    desired: "Desired result",
    budget: "Budget",
    time: "Available time (minutes)",
    home: "At-home products & tools",
    challenges: "Hair & scalp concerns",
    cut: "Cut & styling",
    desiredLength: "Desired length",
    elevation: "Elevation",
    direction: "Over-direction",
    styling: "Styling goal",
    predry: "Pre-dry method",
    finish: "Finishing method",
    tools: "Styling tools & brushes",
    chemical: "Color & chemical services",
    frequency: "Chemical service frequency",
    natural: "Natural level",
    base: "Current base level",
    target: "Desired level",
    pigment: "Dominant pigment",
    tone: "Desired tonal result",
    formula: "Formulas, developer & technique",
    perm: "Perm: wrap, rods & product",
    relaxer: "Relaxer: strength & application",
    processing: "Processing time (minutes)",
    bowls: "Number of color bowls",
    follow: "Finish & follow-up",
    recommend: "Recommended products",
    returnDate: "Suggested return",
    observation: "Service notes",
    visitSaved: "Visit recorded.",
    empty: "No clients found.",
    emptyHelp: "Try another search or add a client.",
    choose: "Select a client to open their folio.",
    noPhotos: "Their story, in pictures.",
    photoHelp:
      "Upload a photo up to 3 MB. Images are stored privately in your account.",
    addPhoto: "Add photo",
    photoError: "Choose a JPEG, PNG or WebP image up to 3 MB.",
    locale: "Make it yours",
    localeSub: "Language, currency and time zone are independent settings.",
    language: "Interface language",
    money: "Service currency",
    timezone: "Time zone",
    account: "Your account",
    signout: "Sign out",
    planSub: "Your account access",
    pro: "Strand Professional",
    feature1: "Client profiles and technical records",
    feature2: "Color formulas and visit history",
    feature3: "English and Brazilian Portuguese",
    feature4: "Before & after photos",
    billingNote:
      "Automatic subscriptions are not enabled. No payment method is collected and no charge is made.",
    loginTitle: "Welcome back.",
    loginSub: "Your next great appointment starts here.",
    password: "Password",
    login: "Sign in",
    forgot: "Forgot password?",
    reset: "Password recovery",
    back: "Back",
    loginQuote: "A little more detail. A lot more care.",
    loginTag: "A personal folio for the way you work.",
    new: "New client",
    editClient: "Edit client",
    technical: "Technical profile",
    intact: "Each visit stays in the history.",
    arch: "Archive client",
    archText:
      "Archive this client? Their records will be preserved and can be restored.",
    archived: "Client archived.",
    fine: "Fine",
    medium: "Medium",
    coarse: "Coarse",
    straight: "Straight",
    wavy: "Wavy",
    curly: "Curly",
    coily: "Coily",
    short: "Short",
    shoulder: "Shoulder-length",
    long: "Long",
    low: "Low",
    normal: "Normal",
    high: "High",
    good: "Good",
    reduced: "Reduced",
    cutService: "Haircut & styling",
    colorService: "Color & gloss",
    highlightService: "Highlights",
    treatmentService: "Treatment",
    permService: "Perm / relaxer",
    privateWorkspace: "Your private workspace",
    privateText:
      "Client records and photos are available only in your account.",
    showArchived: "View archived clients",
    showActive: "View active clients",
    restore: "Restore client",
    deletePhoto: "Delete photo",
    deletePhotoConfirm: "Permanently delete this photo?",
    linkVisit: "Link to a visit",
    generalPhoto: "General client photo",
    changePassword: "Change password",
    currentPassword: "Current password",
    newPassword: "New password",
    exportData: "Export records (JSON)",
    earlyAccess: "Early access · no automated billing",
    createAccount: "Create account",
    passwordHelp:
      "Use at least 12 characters. Avoid common passwords and personal information.",
    backLogin: "Back to sign in",
    sendRecovery: "Send recovery link",
    resendTitle: "Resend verification email",
    checkEmail:
      "If this address is eligible, an email will arrive with the next steps. Check your spam folder.",
    verified: "Email verified. You can now sign in.",
    passwordSaved: "Password updated. Sign in with your new password.",
    passwordChanged: "Password updated.",
    invalid_credentials: "Incorrect credentials or email not verified.",
    rate_limited: "Too many attempts. Wait before trying again.",
    unauthorized: "Your session expired. Please sign in again.",
    csrf: "Refresh the page and try again.",
    invalid: "Check the entered information.",
    validation: "Review the highlighted information.",
    conflict:
      "This record was updated elsewhere. Close the form, reload the list and try again.",
    email_unavailable:
      "Email could not be delivered. Try resending verification or contact support.",
    invalid_link: "This link is invalid, expired or already used.",
    invalid_photo:
      "Choose a valid JPEG, PNG or WebP image up to 3 MB and 20 megapixels.",
    networkError:
      "The server could not be reached. Check your connection and try again.",
    serverError: "The operation could not be completed. Try again.",
    confirmPhoto: "Delete photo",
    refresh: "Reload",
    loading: "Loading…",
  },
  pt: {
    workspace: "Seu espaço",
    clients: "Clientes",
    settings: "Configurações",
    plan: "Assinatura",
    folio: "FICHA DO CLIENTE",
    professional: "Profissional independente",
    title: "Cada cliente. Cada detalhe.",
    subtitle: "Seu trabalho, registrado com cuidado.",
    newClient: "Novo cliente",
    total: "Total de clientes",
    visits: "Atendimentos registrados",
    formulas: "Fórmulas de coloração",
    yourClients: "Seus clientes",
    search: "Buscar por nome ou telefone…",
    all: "Todos os clientes",
    profile: "Ficha capilar",
    history: "Atendimentos",
    photos: "Fotos",
    edit: "Editar ficha",
    newVisit: "Novo atendimento",
    overview: "Dados do cliente",
    email: "E-mail",
    phone: "Telefone",
    birthday: "Aniversário",
    lastVisit: "Último atendimento",
    hair: "Características do cabelo",
    texture: "Espessura dos fios",
    pattern: "Curvatura",
    length: "Comprimento",
    porosity: "Porosidade",
    elasticity: "Elasticidade",
    notes: "Preferências e cuidados",
    lastFormula: "Última fórmula de coloração",
    seeHistory: "Ver histórico",
    noVisit: "Nenhum atendimento",
    memory: "Um bom resultado começa por conhecer seu cliente.",
    memoryText: "Fórmulas, preferências e evolução reunidas em um só lugar.",
    name: "Nome completo",
    save: "Salvar alterações",
    cancel: "Cancelar",
    close: "Fechar",
    saved: "Alterações salvas.",
    created: "Cliente cadastrado.",
    required: "Preencha os campos obrigatórios.",
    consult: "Consulta inicial",
    service: "Serviço",
    date: "Data",
    price: "Valor",
    desired: "Resultado desejado",
    budget: "Orçamento",
    time: "Tempo disponível (minutos)",
    home: "Produtos e ferramentas usados em casa",
    challenges: "Dificuldades com o cabelo e couro cabeludo",
    cut: "Corte e finalização",
    desiredLength: "Comprimento desejado",
    elevation: "Elevação",
    direction: "Direcionamento das mechas",
    styling: "Objetivo da finalização",
    predry: "Método de pré-secagem",
    finish: "Método de acabamento",
    tools: "Ferramentas e escovas",
    chemical: "Coloração e serviços químicos",
    frequency: "Frequência dos procedimentos químicos",
    natural: "Altura de tom natural",
    base: "Altura de tom atual",
    target: "Altura de tom desejada",
    pigment: "Pigmento predominante",
    tone: "Resultado tonal desejado",
    formula: "Fórmulas, oxidante e técnica",
    perm: "Permanente: montagem, bigudis e produto",
    relaxer: "Relaxante: intensidade e aplicação",
    processing: "Tempo de processamento (minutos)",
    bowls: "Quantidade de preparações",
    follow: "Conclusão e acompanhamento",
    recommend: "Produtos recomendados",
    returnDate: "Retorno sugerido",
    observation: "Observações do atendimento",
    visitSaved: "Atendimento registrado.",
    empty: "Nenhum cliente encontrado.",
    emptyHelp: "Tente outra busca ou cadastre um cliente.",
    choose: "Selecione um cliente para abrir a ficha.",
    noPhotos: "Uma história em imagens.",
    photoHelp:
      "Envie uma foto de até 3 MB. As imagens ficam armazenadas de forma privada na sua conta.",
    addPhoto: "Adicionar foto",
    photoError: "Escolha uma imagem JPEG, PNG ou WebP de até 3 MB.",
    locale: "Do seu jeito",
    localeSub: "Idioma, moeda e fuso horário são configurações independentes.",
    language: "Idioma da interface",
    money: "Moeda dos serviços",
    timezone: "Fuso horário",
    account: "Sua conta",
    signout: "Sair da conta",
    planSub: "Acesso da sua conta",
    pro: "Strand Professional",
    feature1: "Cadastros e fichas técnicas",
    feature2: "Fórmulas e histórico de atendimentos",
    feature3: "Inglês e português do Brasil",
    feature4: "Fotos de antes e depois",
    billingNote:
      "As assinaturas automáticas não estão habilitadas. Nenhum meio de pagamento é coletado e nenhuma cobrança é realizada.",
    loginTitle: "Boas-vindas de volta.",
    loginSub: "Seu próximo grande atendimento começa aqui.",
    password: "Senha",
    login: "Entrar",
    forgot: "Esqueceu a senha?",
    reset: "Recuperação de senha",
    back: "Voltar",
    loginQuote: "Mais detalhes. Muito mais cuidado.",
    loginTag: "Uma ficha pessoal para o seu jeito de trabalhar.",
    new: "Novo cliente",
    editClient: "Editar cliente",
    technical: "Ficha técnica",
    intact: "Cada atendimento fica no histórico.",
    arch: "Arquivar cliente",
    archText:
      "Arquivar este cliente? Os registros serão preservados e poderão ser restaurados.",
    archived: "Cliente arquivado.",
    fine: "Fino",
    medium: "Médio",
    coarse: "Grosso",
    straight: "Liso",
    wavy: "Ondulado",
    curly: "Cacheado",
    coily: "Crespo",
    short: "Curto",
    shoulder: "Na altura dos ombros",
    long: "Longo",
    low: "Baixa",
    normal: "Normal",
    high: "Alta",
    good: "Boa",
    reduced: "Reduzida",
    cutService: "Corte e finalização",
    colorService: "Coloração e tonalização",
    highlightService: "Mechas",
    treatmentService: "Tratamento",
    permService: "Permanente / relaxamento",
    privateWorkspace: "Seu espaço privado",
    privateText:
      "Fichas e fotos de clientes ficam disponíveis apenas na sua conta.",
    showArchived: "Ver clientes arquivados",
    showActive: "Ver clientes ativos",
    restore: "Restaurar cliente",
    deletePhoto: "Excluir foto",
    deletePhotoConfirm: "Excluir esta foto permanentemente?",
    linkVisit: "Vincular a um atendimento",
    generalPhoto: "Foto geral do cliente",
    changePassword: "Alterar senha",
    currentPassword: "Senha atual",
    newPassword: "Nova senha",
    exportData: "Exportar registros (JSON)",
    earlyAccess: "Acesso inicial · sem cobrança automática",
    createAccount: "Criar conta",
    passwordHelp:
      "Use pelo menos 12 caracteres. Evite senhas comuns e informações pessoais.",
    backLogin: "Voltar para o login",
    sendRecovery: "Enviar link de recuperação",
    resendTitle: "Reenviar confirmação de e-mail",
    checkEmail:
      "Se este endereço estiver apto, um e-mail chegará com os próximos passos. Verifique também a pasta de spam.",
    verified: "E-mail confirmado. Você já pode entrar.",
    passwordSaved: "Senha atualizada. Entre com a nova senha.",
    passwordChanged: "Senha atualizada.",
    invalid_credentials: "Credenciais incorretas ou e-mail não confirmado.",
    rate_limited: "Muitas tentativas. Aguarde antes de tentar novamente.",
    unauthorized: "Sua sessão expirou. Entre novamente.",
    csrf: "Atualize a página e tente novamente.",
    invalid: "Confira as informações preenchidas.",
    validation: "Confira as informações do formulário.",
    conflict:
      "Este registro foi atualizado em outra sessão. Feche o formulário, recarregue a lista e tente novamente.",
    email_unavailable:
      "Não foi possível entregar o e-mail. Tente reenviar a confirmação ou contate o suporte.",
    invalid_link: "Este link é inválido, expirou ou já foi utilizado.",
    invalid_photo:
      "Escolha uma imagem JPEG, PNG ou WebP válida de até 3 MB e 20 megapixels.",
    networkError:
      "Não foi possível acessar o servidor. Confira sua conexão e tente novamente.",
    serverError: "Não foi possível concluir a operação. Tente novamente.",
    confirmPhoto: "Excluir foto",
    refresh: "Recarregar",
    loading: "Carregando…",
  },
};
const t = (k) => T[lang][k] || k,
  esc = (x) =>
    String(x ?? "").replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
const icons = {
  clients:
    '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
  settings:
    '<g stroke-width="1.8"><path d="M9.56 4.91L10.26 2.15L13.74 2.15L14.44 4.91L15.29 5.26L17.74 3.81L20.19 6.26L18.74 8.71L19.09 9.56L21.85 10.26L21.85 13.74L19.09 14.44L18.74 15.29L20.19 17.74L17.74 20.19L15.29 18.74L14.44 19.09L13.74 21.85L10.26 21.85L9.56 19.09L8.71 18.74L6.26 20.19L3.81 17.74L5.26 15.29L4.91 14.44L2.15 13.74L2.15 10.26L4.91 9.56L5.26 8.71L3.81 6.26L6.26 3.81L8.71 5.26Z"/><circle cx="12" cy="12" r="3.25"/></g>',
  plan: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/>',
  search: '<circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/>',
  visits:
    '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M16 3v4M8 3v4M4 11h16m-12 5 3 2 5-4"/>',
  formulas: '<path d="M9 3h6M10 3v7L4 20h16l-6-10V3M7 15h10"/>',
  leaf: '<path d="M20 4C7 2 1 12 8 18c7 6 15-1 12-14ZM5 21 16 9"/>',
};
const icon = (k) =>
  `<svg viewBox="0 0 24 24" aria-hidden="true">${icons[k] || icons.leaf}</svg>`;
const clients = [];
const current = () => clients.find((c) => c.id === selected);
const initials = (n) =>
  n
    .split(" ")
    .map((x) => x[0])
    .slice(0, 2)
    .join("");
const date = (d) =>
  d
    ? new Intl.DateTimeFormat(lang === "en" ? "en-US" : "pt-BR", {
        day: "numeric",
        month: "short",
        year: "numeric",
        timeZone: "UTC",
      }).format(new Date(d + "T12:00:00Z"))
    : "—";
const money = (v, c) =>
  new Intl.NumberFormat(lang === "en" ? "en-US" : "pt-BR", {
    style: "currency",
    currency: c || currency,
  }).format(Number(v) || 0);
const attr = (k, v) =>
  `<div><span class="label">${t(k)}</span>${esc(v || "—")}</div>`;
const langSelect = () =>
  `<select aria-label="Language / Idioma" onchange="setLang(this.value)"><option value="en" ${lang === "en" ? "selected" : ""}>EN · English</option><option value="pt" ${lang === "pt" ? "selected" : ""}>PT · Português</option></select>`;
async function setLang(v) {
  if (!["en", "pt"].includes(v)) throw Error("Invalid language");
  const old = lang;
  lang = v;
  render();
  if (user) {
    try {
      const r = await api("/api/preferences/", {
        method: "PATCH",
        data: { language: v, currency, timezone: zone },
      });
      user = r.user;
    } catch (e) {
      lang = old;
      render();
      showError(e);
    }
  }
}
function navigate(p) {
  if (!user) {
    authMode = "login";
    renderLogin();
    return;
  }
  page = p;
  render();
}
function render() {
  document.documentElement.lang = lang === "en" ? "en" : "pt-BR";
  if (!user) return renderLogin();
  document.getElementById("app").innerHTML =
    `<div class="app"><aside class="sidebar"><div><div class="brand">strand<em>.</em></div><div class="brandline">${t("folio")}</div></div><nav><p class="navlabel">${t("workspace").toUpperCase()}</p>${["clients", "plan", "settings"].map((p) => `<button class="nav ${page === p ? "active" : ""}" onclick="navigate('${p}')">${icon(p)}${t(p)}</button>`).join("")}</nav><div class="sidebarbottom"><div class="demo-card"><strong>${t("privateWorkspace")}</strong>${t("privateText")}</div><div class="profile"><div class="avatar">${esc(initials(user?.name || ""))}</div><div>${esc(user?.name || "")}<small>${t("professional")}</small></div></div></div></aside><main class="main"><header class="topbar"><div>${t("workspace")} <small> / ${t(page)}</small></div><div class="topright">${langSelect()}</div></header><div class="content">${page === "clients" ? clientPage() : page === "settings" ? settingsPage() : planPage()}</div></main></div>`;
}
function clientPage() {
  const visits = clients.filter((c) => !c.archived).flatMap((c) => c.visits);
  return `<div class="heading"><div><h1>${t("title")}</h1><p class="sub">${t("subtitle")}</p></div><button class="primary" onclick="clientModal()">＋ ${t("newClient")}</button></div><div class="stats">${[
    ["total", clients.filter((c) => !c.archived).length, "clients"],
    ["visits", visits.length, "visits"],
    ["formulas", visits.filter((v) => v.formula).length, "formulas"],
  ]
    .map(
      ([key, n, i]) =>
        `<div class="stat"><div><span>${t(key)}</span><strong>${String(n).padStart(2, "0")}</strong></div><div class="iconbox">${icon(i)}</div></div>`,
    )
    .join(
      "",
    )}</div><div class="workspace"><section class="panel"><div class="panelhead"><h2>${t("yourClients")} <span class="counter">${clients.filter(c => c.archived === showArchived).length}</span></h2></div><div class="search">${icon("search")}<input value="${esc(query)}" placeholder="${t("search")}" aria-label="${t("search")}" oninput="query=this.value;renderList()"></div><div class="clientslist" id="clientlist">${clientList()}</div><div class="listfoot"><button class="quiet small" onclick="toggleArchived()">${showArchived ? t("showActive") : t("showArchived")}</button></div></section><section class="panel" id="detail">${detail()}</section></div><div class="banner">${icon("leaf")}<div><strong>${t("memory")}</strong><p>${t("memoryText")}</p></div></div>`;
}
function clientList() {
  const list = clients
    .filter((c) => c.archived === showArchived)
    .filter((c) =>
      (c.name + " " + c.phone).toLowerCase().includes(query.toLowerCase()),
    );
  return list.length
    ? list
        .map(
          (c) =>
            `<button class="client ${selected === c.id ? "selected" : ""}" onclick="selectClient('${c.id}')"><span class="avatar" style="background:${c.color || "#e5ece3"}">${esc(initials(c.name))}</span><span class="clientinfo"><strong>${esc(c.name)}</strong><small>${c.visits.length ? date(c.visits[0].date) : t("new")}</small></span><span class="chev">›</span></button>`,
        )
        .join("")
    : `<div class="empty">${t("empty")}<br><small>${t("emptyHelp")}</small></div>`;
}
function renderList() {
  document.getElementById("clientlist").innerHTML = clientList();
}
function selectClient(id) {
  selected = id;
  tab = "profile";
  renderList();
  document.getElementById("detail").innerHTML = detail();
}
function setTab(v) {
  tab = v;
  document.getElementById("detail").innerHTML = detail();
}
function detail() {
  const c = current();
  if (!c) return `<div class="empty">${t("choose")}</div>`;
  return `<div class="detailtop"><div class="avatar" style="background:${c.color || "#e5ece3"}">${esc(initials(c.name))}</div><div><h2>${esc(c.name)}</h2><span class="sub">${esc(c.phone || c.email || "—")}</span></div><button class="quiet small" onclick="clientModal(true)" aria-label="${t("edit")}">✎</button></div><div class="tabs">${["profile", "history", "photos"].map((p) => `<button class="tab ${tab === p ? "active" : ""}" onclick="setTab('${p}')">${t(p)}${p === "history" ? ` (${c.visits.length})` : ""}</button>`).join("")}</div><div class="detailbody">${tab === "profile" ? profile(c) : tab === "history" ? visitHistory(c) : photos(c)}</div><div class="detailfooter"><span>${t("intact")}</span>${c.archived ? `<button class="small" onclick="restoreClient()">${t("restore")}</button>` : `<button class="primary small" onclick="visitModal()">＋ ${t("newVisit")}</button>`}</div>`;
}
function profile(c) {
  let v = c.visits.find((v) => v.formula);
  return `<div class="sectionrow"><h3 style="margin:0">${t("overview")}</h3><button class="quiet small" onclick="clientModal(true)">${t("edit")}</button></div><div class="info-grid">${attr("email", c.email)}${attr("birthday", date(c.birthday))}${attr("phone", c.phone)}${attr("lastVisit", c.visits[0] ? date(c.visits[0].date) : t("noVisit"))}</div><hr class="rule"><h3>${t("hair")}</h3><div class="info-grid">${["texture", "pattern", "length", "porosity", "elasticity"].map((k) => attr(k, c[k] ? t(c[k]) : "—")).join("")}</div>${c.notes ? `<hr class="rule"><div class="note"><strong>${t("notes")}</strong>${esc(c.notes)}</div>` : ""}${v ? `<hr class="rule"><div class="sectionrow"><h3 style="margin:0">${t("lastFormula")}</h3><button class="quiet small" onclick="setTab('history')">${t("seeHistory")} →</button></div><div class="formula">${esc(v.formula).replace(/\n/g, "<br>")}</div>` : ""}`;
}
function visitHistory(c) {
  return c.visits.length
    ? c.visits
        .map(
          (v, i) =>
            `<article class="visit"><div class="visithead"><strong>${t(v.service)}</strong><strong>${money(v.price, v.currency)}</strong></div><div class="date">${date(v.date)} · ${esc(user?.name || "")}</div>${v.formula ? `<p class="formula">${esc(v.formula).replace(/\n/g, "<br>")}</p>` : ""}${v.observation ? `<p>${esc(v.observation)}</p>` : ""}<button class="quiet small" onclick="viewVisit(${i})">${t("technical")} →</button></article>`,
        )
        .join("")
    : `<div class="empty">${t("noVisit")}</div>`;
}
function photos(c) {
  return `${c.photos.length ? `<div class="gallery">${c.photos.map((p, i) => `<figure style="margin:0"><img src="${esc(p.url)}" alt="${t("photos")} ${i + 1}" loading="lazy"><button class="quiet small" onclick="deletePhoto('${p.id}')">${t("deletePhoto")}</button></figure>`).join("")}</div>` : `<div class="empty">${icon("leaf")}<h3 style="margin:14px 0 8px">${t("noPhotos")}</h3></div>`}<p class="sub" style="margin:20px 0">${t("photoHelp")}</p>${c.archived ? "" : `<label class="field">${t("linkVisit")}<select id="photoVisit"><option value="">${t("generalPhoto")}</option>${c.visits.map((v) => `<option value="${v.id}">${date(v.date)} · ${t(v.service)}</option>`).join("")}</select></label><button style="margin-top:15px" onclick="document.getElementById('photoInput').click()">＋ ${t("addPhoto")}</button><input id="photoInput" type="file" accept="image/jpeg,image/png,image/webp" hidden onchange="addPhoto(this)">`}`;
}
async function addPhoto(input) {
  const f = input.files[0];
  if (!f) return;
  if (
    !["image/jpeg", "image/png", "image/webp"].includes(f.type) ||
    f.size > 3 * 1024 * 1024
  )
    return toast(t("photoError"));
  const data = new FormData();
  data.append("photo", f);
  data.append("visit_id", document.getElementById("photoVisit").value);
  input.disabled = true;
  try {
    await api(`/api/clients/${selected}/photos/`, {
      method: "POST",
      form: data,
    });
    await refresh();
    toast(t("saved"));
  } catch (e) {
    showError(e);
    input.disabled = false;
  }
}
const field = (key, value = "", type = "text", full = false) =>
  `<label class="field ${full ? "full" : ""}">${t(key)}${key === "name" ? " *" : ""}${type === "textarea" ? `<textarea name="${key}" maxlength="4000">${esc(value)}</textarea>` : `<input name="${key}" type="${type}" value="${esc(value)}" ${key === "name" ? 'required maxlength="100"' : ""} ${type === "number" ? 'min="0" step="0.01"' : ""}>`}</label>`;
const selectField = (key, opts, value) =>
  `<label class="field">${t(key)}<select name="${key}"><option value="">—</option>${opts.map((x) => `<option value="${x}" ${value === x ? "selected" : ""}>${t(x)}</option>`).join("")}</select></label>`;
function modal(title, body) {
  let m = document.getElementById("modal");
  m.innerHTML = `<div class="modalhead"><h2>${title}</h2><button class="quiet" onclick="closeModal()" aria-label="${t("close")}">×</button></div><div class="modalbody">${body}</div>`;
  m.showModal();
}
function closeModal() {
  document.getElementById("modal").close();
}
const formActions = () =>
  `<div class="actions"><button type="button" onclick="closeModal()">${t("cancel")}</button><button class="primary">${t("save")}</button></div>`;
function clientModal(edit = false) {
  const c = edit ? current() : {};
  modal(
    t(edit ? "editClient" : "new"),
    `<form data-client="${c.id || ""}" data-version="${c.version || ""}" onsubmit="saveClient(event,${edit})"><div class="fields">${field("name", c.name)}${field("phone", c.phone, "tel")}${field("email", c.email, "email")}${field("birthday", c.birthday, "date")}${selectField("texture", ["fine", "medium", "coarse"], c.texture)}${selectField("pattern", ["straight", "wavy", "curly", "coily"], c.pattern)}${selectField("length", ["short", "shoulder", "long"], c.length)}${selectField("porosity", ["low", "medium", "normal", "high"], c.porosity)}${selectField("elasticity", ["good", "normal", "reduced"], c.elasticity)}${field("notes", c.notes, "textarea", true)}</div>${formActions()}${edit && !c.archived ? `<button type="button" class="quiet small" style="color:#9c4b39;margin-top:10px" onclick="archiveConfirm()">${t("arch")}</button>` : ""}</form>`,
  );
}
async function saveClient(e, edit) {
  e.preventDefault();
  const form = e.target;
  await submit(form, async () => {
    const data = Object.fromEntries(new FormData(form));
    if (edit) data.version = Number(form.dataset.version);
    await api(edit ? `/api/clients/${form.dataset.client}/` : "/api/clients/", {
      method: edit ? "PATCH" : "POST",
      data,
    }).then((r) => {
      selected = r.client.id;
      if (!edit) showArchived = false;
    });
    closeModal();
    await refresh();
    toast(t("saved"));
  });
}
function archiveConfirm() {
  closeModal();
  modal(
    t("arch"),
    `<p>${t("archText")}</p><div class="actions"><button onclick="closeModal()">${t("cancel")}</button><button class="primary" onclick="archiveClient()">${t("arch")}</button></div>`,
  );
}
async function archiveClient() {
  const c = current();
  try {
    await api(`/api/clients/${c.id}/`, {
      method: "PATCH",
      data: { archived: true, version: c.version },
    });
    closeModal();
    selected = null;
    await refresh();
    toast(t("archived"));
  } catch (e) {
    showError(e);
  }
}
function visitModal() {
  modal(
    t("newVisit"),
    `<form data-client="${current().id}" data-request-id="${crypto.randomUUID()}" onsubmit="saveVisit(event)"><div class="fields">${selectField("service", ["cutService", "colorService", "highlightService", "treatmentService", "permService"], "colorService")}${field("date", new Date().toLocaleDateString("en-CA", { timeZone: zone }), "date")}${field("price", "0", "number")}<label class="field">${t("money")}<select name="currency"><option ${currency === "USD" ? "selected" : ""}>USD</option><option ${currency === "BRL" ? "selected" : ""}>BRL</option><option ${currency === "EUR" ? "selected" : ""}>EUR</option><option ${currency === "GBP" ? "selected" : ""}>GBP</option></select></label></div><h3 class="formgroup">${t("consult")}</h3><div class="fields">${field("desired", "", "textarea", true)}${field("budget", "", "number")}${field("time", "", "number")}${field("home")}${field("challenges")}</div><div id="servicefields"></div><h3 class="formgroup">${t("follow")}</h3><div class="fields">${field("recommend")}${field("returnDate", "", "date")}${field("observation", "", "textarea", true)}</div>${formActions()}</form>`,
  );
  let f = document.querySelector("[name=service]");
  f.required = true;
  document.querySelector("[name=date]").required = true;
  document.querySelector("[name=price]").required = true;
  f.onchange = () => serviceFields(f.value);
  serviceFields(f.value);
}
function serviceFields(s) {
  let keys =
    s === "cutService"
      ? [
          "desiredLength",
          "elevation",
          "direction",
          "styling",
          "predry",
          "finish",
          "tools",
        ]
      : s === "permService"
        ? ["frequency", "perm", "relaxer", "processing"]
        : ["colorService", "highlightService"].includes(s)
          ? [
              "frequency",
              "natural",
              "base",
              "target",
              "pigment",
              "tone",
              "formula",
              "processing",
              "bowls",
            ]
          : ["styling", "tools"];
  document.getElementById("servicefields").innerHTML =
    `<h3 class="formgroup">${t(s === "cutService" ? "cut" : s === "treatmentService" ? "technical" : "chemical")}</h3><div class="fields">${keys.map((k) => field(k, "", k === "formula" ? "textarea" : ["processing", "bowls"].includes(k) ? "number" : "text", k === "formula")).join("")}</div>`;
}
async function saveVisit(e) {
  e.preventDefault();
  const form = e.target;
  await submit(form, async () => {
    const data = {
      ...Object.fromEntries(new FormData(form)),
      request_id: form.dataset.requestId,
    };
    await api(`/api/clients/${form.dataset.client}/visits/`, {
      method: "POST",
      data,
    });
    closeModal();
    tab = "history";
    await refresh();
    toast(t("visitSaved"));
  });
}
function viewVisit(i) {
  const v = current().visits[i];
  modal(
    t(v.service),
    `<p class="sub" style="margin-bottom:25px">${date(v.date)} · ${money(v.price, v.currency)}</p><div class="info-grid">${Object.entries(
      v,
    )
      .filter(
        ([k, val]) =>
          !["service", "date", "price", "currency"].includes(k) && val,
      )
      .map(([k, val]) => attr(k, val))
      .join(
        "",
      )}</div><div class="actions"><button onclick="closeModal()">${t("close")}</button></div>`,
  );
}
function settingsPage() {
  return `<div class="heading"><div><h1>${t("locale")}</h1><p class="sub">${t("localeSub")}</p></div></div><div class="panel settings"><h3>${t("settings")}</h3><form onsubmit="saveSettings(event)"><div class="fields"><label class="field">${t("language")}<select name="language"><option value="en" ${lang === "en" ? "selected" : ""}>English</option><option value="pt" ${lang === "pt" ? "selected" : ""}>Português (Brasil)</option></select></label><label class="field">${t("money")}<select name="currency">${["USD", "BRL", "EUR", "GBP"].map((c) => `<option ${currency === c ? "selected" : ""}>${c}</option>`).join("")}</select></label><label class="field full">${t("timezone")}<select name="zone">${["America/New_York", "America/Sao_Paulo", "America/Los_Angeles", "Europe/London", "Europe/Lisbon", "Australia/Sydney"].map((z) => `<option ${zone === z ? "selected" : ""}>${z}</option>`).join("")}</select></label></div><div class="actions"><button class="primary">${t("save")}</button></div></form><hr class="rule"><h3>${t("account")}</h3><p class="sub">${esc(user?.name || "")} · ${esc(user?.email || "")}</p><button style="margin-top:20px" onclick="signOut()">${t("signout")} →</button><div class="actions"><button onclick="changePasswordModal()">${t("changePassword")}</button><a href="/api/export/" class="download">${t("exportData")}</a></div></div>`;
}
async function saveSettings(e) {
  e.preventDefault();
  await submit(e.target, async () => {
    const d = new FormData(e.target);
    const r = await api("/api/preferences/", {
      method: "PATCH",
      data: {
        language: d.get("language"),
        currency: d.get("currency"),
        timezone: d.get("zone"),
      },
    });
    applyUser(r.user);
    render();
    toast(t("saved"));
  });
}
function planPage() {
  return `<div class="heading"><div><h1>${t("pro")}</h1><p class="sub">${t("planSub")}</p></div></div><div class="panel settings"><h2>${t("earlyAccess")}</h2><p class="sub" style="margin-top:20px">${t("billingNote")}</p><ul class="checks">${[1, 2, 3, 4].map((i) => `<li>${t("feature" + i)}</li>`).join("")}</ul></div>`;
}
function billing() {
  navigate("plan");
}
function renderLogin() {
  document.documentElement.lang = lang === "en" ? "en" : "pt-BR";
  const signup = authMode === "register";
  const reset = authMode === "reset";
  const confirm = authMode === "confirm";
  const resend = authMode === "resend";
  const title = signup
    ? "createAccount"
    : confirm
      ? "newPassword"
      : reset
        ? "reset"
        : resend
          ? "resendTitle"
          : "loginTitle";
  document.getElementById("app").innerHTML =
    `<div class="login"><div class="loginart"><div class="brand">strand<em>.</em></div><h1>${t("loginQuote")}</h1><p>${t("loginTag")}</p></div><div class="loginform"><div class="logininner"><div style="margin-bottom:35px">${langSelect()}</div><h1>${t(title)}</h1><p class="sub">${t("loginSub")}</p><form onsubmit="authSubmit(event)">${signup ? field("name") : ""}${confirm ? "" : field("email", "", "email")}${reset || resend ? "" : field("password", "", "password")}${signup || confirm ? `<p class="sub" style="font-size:13px;margin-top:10px">${t("passwordHelp")}</p>` : ""}<p id="authError" role="alert" class="error"></p><button class="primary">${t(signup ? "createAccount" : reset ? "sendRecovery" : resend ? "resendTitle" : confirm ? "save" : "login")}</button></form><div class="authlinks">${authMode === "login" ? `<button class="quiet small" onclick="authView('register')">${t("createAccount")}</button><button class="quiet small" onclick="authView('reset')">${t("forgot")}</button><button class="quiet small" onclick="authView('resend')">${t("resendTitle")}</button>` : `<button class="quiet small" onclick="authView('login')">${t("backLogin")}</button>`}</div></div></div></div>`;
  document.querySelectorAll(".logininner input").forEach((i) => {
    i.required = true;
    i.maxLength = i.type === "password" ? 256 : 254;
    i.autocomplete =
      i.type === "password"
        ? signup || confirm
          ? "new-password"
          : "current-password"
        : i.type === "email"
          ? "email"
          : "name";
  });
}
function resetPreview() {
  authView("reset");
}
function toast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.style.display = "block";
  clearTimeout(window.toastTimer);
  window.toastTimer = setTimeout(() => (el.style.display = "none"), 3300);
}
Object.assign(T.en, {
  privateWorkspace: "Your private workspace",
  privateText: "Client records and photos are available only in your account.",
  showArchived: "View archived clients",
  showActive: "View active clients",
  restore: "Restore client",
  saved: "Changes saved.",
  created: "Client added.",
  archText:
    "Archive this client? Their records will be preserved and can be restored.",
  archived: "Client archived.",
  photoHelp:
    "Upload a photo up to 3 MB. Images are stored privately in your account.",
  addPhoto: "Add photo",
  deletePhoto: "Delete photo",
  deletePhotoConfirm: "Permanently delete this photo?",
  linkVisit: "Link to a visit",
  generalPhoto: "General client photo",
  account: "Your account",
  signout: "Sign out",
  changePassword: "Change password",
  currentPassword: "Current password",
  newPassword: "New password",
  exportData: "Export records (JSON)",
  planSub: "Your account access",
  earlyAccess: "Early access · no automated billing",
  billingNote:
    "Automatic subscriptions are not enabled. No payment method is collected and no charge is made.",
  login: "Sign in",
  createAccount: "Create account",
  passwordHelp:
    "Use at least 12 characters. Avoid common passwords and personal information.",
  backLogin: "Back to sign in",
  sendRecovery: "Send recovery link",
  resendTitle: "Resend verification email",
  checkEmail:
    "If this address is eligible, an email will arrive with the next steps. Check your spam folder.",
  verified: "Email verified. You can now sign in.",
  passwordSaved: "Password updated. Sign in with your new password.",
  passwordChanged: "Password updated.",
  invalid_credentials: "Incorrect credentials or email not verified.",
  rate_limited: "Too many attempts. Wait before trying again.",
  unauthorized: "Your session expired. Please sign in again.",
  csrf: "Refresh the page and try again.",
  invalid: "Check the entered information.",
  validation: "Review the highlighted information.",
  conflict:
    "This record was updated elsewhere. Close the form, reload the list and try again.",
  email_unavailable:
    "Email could not be delivered. Try resending verification or contact support.",
  invalid_link: "This link is invalid, expired or already used.",
  invalid_photo:
    "Choose a valid JPEG, PNG or WebP image up to 3 MB and 20 megapixels.",
  networkError:
    "The server could not be reached. Check your connection and try again.",
  serverError: "The operation could not be completed. Try again.",
  confirmPhoto: "Delete photo",
  refresh: "Reload",
  loading: "Loading…",
});

const resetParams = {};
function errorText(e) {
  let text = t(e.code || "serverError");
  if (e.details) text += " " + e.details.join(" ");
  if (e.fields)
    text +=
      " " +
      Object.entries(e.fields)
        .map(([k, v]) => `${t(k)}: ${v.map((x) => x.message).join(" ")}`)
        .join(" · ");
  return text;
}
function showError(e) {
  toast(errorText(e));
  if (e.code === "unauthorized") {
    user = null;
    clients.splice(0);
    selected = null;
    authMode = "login";
    closeModal();
    render();
  }
}
async function api(url, { method = "GET", data, form } = {}) {
  const csrf =
    document.cookie
      .split("; ")
      .find((c) => c.startsWith("csrftoken="))
      ?.split("=")
      .slice(1)
      .join("=") || "";
  const headers = {
    "X-CSRFToken": decodeURIComponent(csrf),
    "X-Language": lang,
    Accept: "application/json",
  };
  if (data) headers["Content-Type"] = "application/json";
  let response;
  try {
    response = await fetch(url, {
      method,
      headers,
      credentials: "same-origin",
      cache: "no-store",
      body: form || (data ? JSON.stringify(data) : undefined),
    });
  } catch {
    throw { code: "networkError" };
  }
  let result;
  try {
    result = await response.json();
  } catch {
    throw { code: "serverError" };
  }
  if (!response.ok)
    throw {
      code: result.error || "serverError",
      details: result.details,
      fields: result.fields,
    };
  return result;
}
async function submit(form, fn) {
  if (form.dataset.busy) return;
  form.dataset.busy = "1";
  const buttons = [...form.querySelectorAll("button")];
  buttons.forEach((b) => (b.disabled = true));
  try {
    await fn();
  } catch (e) {
    showError(e);
  } finally {
    delete form.dataset.busy;
    buttons.forEach((b) => (b.disabled = false));
  }
}
function applyUser(u) {
  user = u;
  lang = u.language;
  currency = u.currency;
  zone = u.timezone;
}
async function refresh() {
  const r = await api("/api/clients/");
  clients.splice(0, clients.length, ...r.clients);
  if (!clients.some((c) => c.id === selected && c.archived === showArchived))
    selected = clients.find((c) => c.archived === showArchived)?.id || null;
  render();
}
function toggleArchived() {
  showArchived = !showArchived;
  selected = clients.find((c) => c.archived === showArchived)?.id || null;
  query = "";
  render();
}
async function restoreClient() {
  const c = current();
  try {
    await api(`/api/clients/${c.id}/`, {
      method: "PATCH",
      data: { archived: false, version: c.version },
    });
    showArchived = false;
    await refresh();
    toast(t("saved"));
  } catch (e) {
    showError(e);
  }
}
function authView(mode) {
  authMode = mode;
  renderLogin();
}
async function authSubmit(e) {
  e.preventDefault();
  const form = e.target;
  if (form.dataset.busy) return;
  form.dataset.busy = "1";
  const btn = form.querySelector("button");
  btn.disabled = true;
  const data = { ...Object.fromEntries(new FormData(form)), language: lang };
  try {
    if (authMode === "login") {
      const r = await api("/api/auth/login/", { method: "POST", data });
      applyUser(r.user);
      page = "clients";
      await refresh();
    } else if (authMode === "confirm") {
      await api("/api/auth/reset-confirm/", {
        method: "POST",
        data: { ...data, ...resetParams },
      });
      authView("login");
      toast(t("passwordSaved"));
    } else {
      await api(
        `/api/auth/${authMode === "register" ? "register" : authMode === "resend" ? "resend" : "reset"}/`,
        { method: "POST", data },
      );
      authView("login");
      modal(
        t("email"),
        `<p class="sub">${t("checkEmail")}</p><div class="actions"><button onclick="closeModal()">${t("close")}</button></div>`,
      );
    }
  } catch (err) {
    const el = document.getElementById("authError");
    if (el) el.textContent = errorText(err);
    else showError(err);
  } finally {
    delete form.dataset.busy;
    btn.disabled = false;
  }
}
async function signOut() {
  try {
    await api("/api/auth/logout/", { method: "POST" });
    user = null;
    clients.splice(0);
    selected = null;
    query = "";
    showArchived = false;
    authMode = "login";
    render();
  } catch (e) {
    showError(e);
  }
}
function changePasswordModal() {
  modal(
    t("changePassword"),
    `<form onsubmit="changePassword(event)"><label class="field">${t("currentPassword")}<input name="current_password" type="password" autocomplete="current-password" required maxlength="256"></label><label class="field" style="margin-top:18px">${t("newPassword")}<input name="password" type="password" autocomplete="new-password" required minlength="12" maxlength="256"></label><p class="sub">${t("passwordHelp")}</p>${formActions()}</form>`,
  );
}
async function changePassword(e) {
  e.preventDefault();
  await submit(e.target, async () => {
    await api("/api/auth/password/", {
      method: "POST",
      data: Object.fromEntries(new FormData(e.target)),
    });
    closeModal();
    toast(t("passwordChanged"));
  });
}
function deletePhoto(id) {
  modal(
    t("confirmPhoto"),
    `<p>${t("deletePhotoConfirm")}</p><div class="actions"><button onclick="closeModal()">${t("cancel")}</button><button class="primary" onclick="confirmDeletePhoto('${id}',this)">${t("deletePhoto")}</button></div>`,
  );
}
async function confirmDeletePhoto(id, button) {
  button.disabled = true;
  try {
    await api(`/api/photos/${id}/`, { method: "DELETE" });
    closeModal();
    await refresh();
    toast(t("saved"));
  } catch (e) {
    showError(e);
    button.disabled = false;
  }
}
async function boot() {
  const params = new URLSearchParams(location.search);
  const verify = params.get("verify"),
    reset = params.get("reset"),
    uid = params.get("uid");
  if (verify || reset) window.history.replaceState({}, "", location.pathname);
  try {
    const r = await api("/api/session/");
    if (r.user) applyUser(r.user);
    if (verify) {
      await api("/api/auth/verify/", {
        method: "POST",
        data: { token: verify },
      });
      render();
      toast(t("verified"));
    } else if (reset && uid) {
      user = null;
      resetParams.token = reset;
      resetParams.uid = uid;
      authView("confirm");
    } else if (user) {
      page = "clients";
      await refresh();
    } else render();
  } catch (e) {
    render();
    showError(e);
  }
}
boot();
