const columns = [
  ["Backlog", "Backlog", "#8591a7"],
  ["To Do", "Por hacer", "#7897bb"],
  ["In Progress", "En curso", "#487fcc"],
  ["In QA", "En QA", "#8c70c4"],
  ["Waiting For", "En espera", "#d59b41"],
  ["Done", "Terminadas", "#39a995"],
];

const board = document.querySelector("#board");
const areaFilter = document.querySelector("#area");
const search = document.querySelector("#search");
const dialog = document.querySelector("#detail-dialog");
const historySelect = document.querySelector("#history-select");
const milestoneGrid = document.querySelector("#milestone-grid");
let appState;
let currentState;
let view = "current";
let historyId = "";

function element(tag, className, content) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (content !== undefined) node.textContent = content;
  return node;
}

function setText(selector, text) {
  document.querySelector(selector).textContent = text;
}

function renderAreas(areas) {
  const previous = areaFilter.value;
  areaFilter.replaceChildren(new Option("Todas las áreas", ""));
  for (const area of areas) areaFilter.add(new Option(area, area));
  areaFilter.value = areas.includes(previous) ? previous : "";
}

function showDetail(item) {
  setText("#detail-id", `${item.id} · ${item.status}`);
  setText("#detail-story", item.story);
  setText("#detail-meta", item.areas ? `Áreas: ${item.areas}` : "Sin áreas definidas");
  setText("#detail-next", item.nextAction ? `Siguiente paso: ${item.nextAction}` : "");
  setText("#detail-plan", item.plan.path ? `Plan: ${item.plan.path}` : "Sin plan enlazado");
  for (const [selector, entries] of [
    ["#detail-criteria", item.plan.criteria],
    ["#detail-verification", item.plan.verification],
  ]) {
    const list = document.querySelector(selector);
    list.replaceChildren();
    for (const entry of entries) list.append(element("li", "", entry));
    if (!entries.length) list.append(element("li", "", "No disponible en el plan."));
  }
  dialog.showModal();
}

function renderBoard() {
  if (!currentState) return;
  const query = search.value.trim().toLocaleLowerCase();
  const area = areaFilter.value;
  const items = currentState.items.filter((item) => {
    const matchesArea = !area || item.areas.split(",").map((part) => part.trim()).includes(area);
    const matchesText = !query || `${item.id} ${item.story} ${item.nextAction}`.toLocaleLowerCase().includes(query);
    return matchesArea && matchesText;
  });
  board.replaceChildren();

  const visibleColumns = view === "history" ? columns.slice(1) : columns;
  const known = new Set(visibleColumns.map(([status]) => status));
  const extra = [...new Set(items.map((item) => item.status))]
    .filter((status) => !known.has(status))
    .map((status) => [status, `Estado: ${status}`, "#bd6274"]);
  for (const [status, label, color] of [...visibleColumns, ...extra]) {
    const lane = element("section", "lane");
    lane.dataset.status = status;
    lane.style.setProperty("--lane-color", color);
    const matching = items.filter((item) => item.status === status);
    const head = element("div", "lane-head");
    const title = element("div", "lane-title");
    title.append(element("span", "lane-dot"), element("span", "", label));
    head.append(title, element("span", "lane-count", matching.length));
    lane.append(head);
    const cards = element("div", "lane-cards");
    if (!matching.length) cards.append(element("p", "empty", "Sin historias"));
    for (const item of matching) {
      const card = element("button", "card");
      card.type = "button";
      card.append(element("span", "card-id", item.id), element("span", "card-story", item.story));
      if (item.areas) {
        const tags = element("span", "tags");
        for (const areaName of item.areas.split(",").map((part) => part.trim()).filter(Boolean)) {
          tags.append(element("span", "tag", areaName));
        }
        card.append(tags);
      }
      if (item.nextAction) card.append(element("span", "next-action", item.nextAction));
      card.addEventListener("click", () => showDetail(item));
      cards.append(card);
    }
    lane.append(cards);
    board.append(lane);
  }
}

function renderSprint() {
  const selected = view === "history"
    ? appState.history.find((sprint) => sprint.id === historyId)
    : appState;
  const state = selected || {
    sprint: "Sin sprints pasados", goal: "Cuando cierres un sprint, aparecerá aquí.",
    dates: "", hasSprint: false, items: [], counts: {}, areas: [], milestone: "",
  };
  currentState = state;
  setText("#project-name", appState.project.toLocaleUpperCase());
  setText("#sprint-name", state.sprint);
  setText("#sprint-goal", state.goal || (state.hasSprint ? "Sin objetivo escrito." : "Crea un sprint con /sprint para seguir el trabajo activo."));
  setText("#sprint-dates", [state.dates, state.milestone && `Milestone: ${state.milestone}`].filter(Boolean).join(" · "));
  const total = state.items.filter((item) => item.status !== "Backlog").length;
  const done = state.counts.Done || 0;
  const percent = total ? Math.round((done / total) * 100) : 0;
  setText("#progress-value", `${percent}%`);
  document.querySelector("#progress-fill").style.width = `${percent}%`;
  setText("#progress-caption", `${done} de ${total} historias del sprint terminadas`);
  for (const [selector, status] of [
    ["#count-todo", "To Do"], ["#count-progress", "In Progress"],
    ["#count-qa", "In QA"], ["#count-waiting", "Waiting For"], ["#count-done", "Done"],
  ]) setText(selector, state.counts[status] || 0);
  setText("#board-subtitle", `${state.items.length} historias · se actualiza cada 5 segundos`);
  renderAreas(state.areas);
  renderBoard();
}

function renderHistoryPicker() {
  const previous = historyId;
  historySelect.replaceChildren();
  for (const sprint of appState.history) {
    historySelect.add(new Option(`${sprint.id} · ${sprint.sprint}`, sprint.id));
  }
  historyId = appState.history.some((sprint) => sprint.id === previous)
    ? previous : (appState.history[0]?.id || "");
  historySelect.value = historyId;
  setText("#history-count", appState.history.length);
}

function renderMilestones() {
  milestoneGrid.replaceChildren();
  if (!appState.milestones.length) {
    milestoneGrid.append(element("p", "no-data", "Aún no hay milestones en MILESTONES.md."));
    return;
  }
  const labels = { Planned: "Planificado", Active: "Activo", Done: "Terminado" };
  for (const milestone of appState.milestones) {
    const card = element("article", "milestone-card");
    const top = element("div", "milestone-top");
    const status = element("span", "milestone-status", labels[milestone.status] || milestone.status);
    status.dataset.status = milestone.status;
    top.append(element("span", "milestone-id", milestone.id), status);
    card.append(top, element("h2", "", milestone.name), element("p", "milestone-goal", milestone.goal));
    const progress = element("div", "milestone-progress");
    progress.append(element("span", "", "Historias terminadas"), element("strong", "", `${milestone.done} / ${milestone.total}`));
    card.append(progress);
    const track = element("div", "milestone-track");
    const fill = element("div", "");
    fill.style.width = `${milestone.total ? Math.round(milestone.done / milestone.total * 100) : 0}%`;
    track.append(fill);
    card.append(track);
    const bottom = element("div", "milestone-bottom");
    bottom.append(element("span", "milestone-target", milestone.target ? `Objetivo: ${milestone.target}` : "Sin fecha objetivo"));
    const sprintLinks = element("div", "milestone-sprints");
    if (!milestone.sprintIds.length) sprintLinks.append(element("span", "milestone-target", "Sin sprints"));
    for (const sprintId of milestone.sprintIds) {
      const link = element("button", "sprint-link", sprintId);
      link.type = "button";
      const exists = sprintId === appState.id || appState.history.some((sprint) => sprint.id === sprintId);
      link.disabled = !exists;
      if (exists) link.addEventListener("click", () => {
        historyId = sprintId;
        setView(sprintId === appState.id ? "current" : "history");
      });
      sprintLinks.append(link);
    }
    bottom.append(sprintLinks);
    card.append(bottom);
    milestoneGrid.append(card);
  }
}

function setView(next) {
  const changed = view !== next;
  view = next;
  if (changed && dialog.open) dialog.close();
  document.querySelector("#sprint-view").hidden = view === "milestones";
  document.querySelector("#milestones-view").hidden = view !== "milestones";
  document.querySelector("#history-picker").hidden = view !== "history";
  for (const button of document.querySelectorAll(".view-tabs button")) {
    const active = button.dataset.view === view;
    button.classList.toggle("active", active);
    if (active) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  }
  if (view === "milestones") renderMilestones();
  else renderSprint();
}

function render(state) {
  appState = state;
  renderHistoryPicker();
  setText("#milestone-count", state.milestones.length);
  setText("#last-read", `Última lectura: ${new Date(state.updated).toLocaleTimeString("es-ES")}`);
  setView(view);
}

async function refresh() {
  try {
    const response = await fetch("/api/state", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    render(await response.json());
  } catch (error) {
    setText("#last-read", `No se pudo actualizar el tablero: ${error.message}`);
  }
}

search.addEventListener("input", renderBoard);
areaFilter.addEventListener("change", renderBoard);
historySelect.addEventListener("change", () => { historyId = historySelect.value; renderSprint(); });
for (const button of document.querySelectorAll(".view-tabs button")) {
  button.addEventListener("click", () => setView(button.dataset.view));
}
document.querySelector("#close-detail").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
refresh();
setInterval(refresh, 5000);
