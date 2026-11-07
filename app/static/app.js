const STATUSES = ["PENDING", "CONFIRMED", "PREPARING", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"];
const NEXT_STATUSES = {
  PENDING: ["CONFIRMED", "CANCELLED"],
  CONFIRMED: ["PREPARING", "CANCELLED"],
  PREPARING: ["OUT_FOR_DELIVERY", "CANCELLED"],
  OUT_FOR_DELIVERY: ["DELIVERED"],
  DELIVERED: [],
  CANCELLED: [],
};
const state = { customers: [], menuItems: [], orders: [] };
const currency = new Intl.NumberFormat(undefined, { style: "currency", currency: "INR" });
let noticeTimer;

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  const data = response.status === 204 ? null : await response.json();
  if (!response.ok) throw new Error(data?.error || "The request could not be completed.");
  return data;
}

function showNotice(message, isError = false) {
  const notice = document.querySelector("#notice");
  notice.textContent = message;
  notice.classList.toggle("error", isError);
  notice.hidden = false;
  clearTimeout(noticeTimer);
  noticeTimer = setTimeout(() => { notice.hidden = true; }, 4500);
}

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function button(text, action, className = "text-button") {
  const node = element("button", text, className);
  node.type = "button";
  node.addEventListener("click", action);
  return node;
}

function emptyRow(body, columns, message) {
  const row = element("tr");
  const cell = element("td", message, "empty");
  cell.colSpan = columns;
  row.append(cell);
  body.replaceChildren(row);
}

function money(value) {
  return currency.format(Number(value) || 0);
}

async function loadDashboard() {
  const dashboard = await api("/api/dashboard");
  const summary = dashboard.summary;
  const cards = [
    ["Customers", summary.customers],
    ["Menu items", summary.menu_items],
    ["Available today", summary.available_menu_items],
    ["Total orders", summary.orders],
    ["Delivered value", money(summary.delivered_order_value)],
  ];
  const cardHost = document.querySelector("#summary-cards");
  cardHost.replaceChildren(...cards.map(([label, value]) => {
    const card = element("article", undefined, "metric");
    card.append(element("span", label), element("strong", value));
    return card;
  }));

  const statusHost = document.querySelector("#status-summary");
  statusHost.replaceChildren(...Object.entries(dashboard.orders_by_status).map(([status, count]) => {
    const row = element("div", undefined, "status-row");
    row.append(element("span", status.replaceAll("_", " ")), element("strong", count));
    return row;
  }));

  const recentHost = document.querySelector("#recent-orders");
  if (!dashboard.recent_orders.length) {
    emptyRow(recentHost, 3, "No orders yet.");
    return;
  }
  recentHost.replaceChildren(...dashboard.recent_orders.map((order) => {
    const row = element("tr");
    row.append(element("td", `#${order.id}`), element("td", order.status), element("td", money(order.total_amount)));
    return row;
  }));
}

async function loadCustomers() {
  const search = document.querySelector("#customer-search").value.trim();
  const query = search ? `?search=${encodeURIComponent(search)}` : "";
  state.customers = await api(`/api/customers${query}`);
  const body = document.querySelector("#customers-list");
  document.querySelector("#customer-count").textContent = `${state.customers.length} shown`;
  if (!state.customers.length) {
    emptyRow(body, 4, "No customers found.");
  } else {
    body.replaceChildren(...state.customers.map((customer) => {
      const row = element("tr");
      row.append(element("td", customer.name), element("td", customer.phone), element("td", customer.address));
      const actions = element("td");
      const actionGroup = element("div", undefined, "actions");
      actionGroup.append(
        button("Edit", () => editCustomer(customer)),
        button("Delete", () => deleteCustomer(customer.id), "text-button delete"),
      );
      actions.append(actionGroup);
      row.append(actions);
      return row;
    }));
  }
  const select = document.querySelector("#order-customer");
  const currentValue = select.value;
  select.replaceChildren(new Option("Choose a customer", ""));
  state.customers.forEach((customer) => select.add(new Option(`${customer.name} · ${customer.phone}`, customer.id)));
  if (state.customers.some((customer) => String(customer.id) === currentValue)) select.value = currentValue;
}

function resetCustomerForm() {
  document.querySelector("#customer-form").reset();
  document.querySelector("#customer-id").value = "";
  document.querySelector("#customer-form-title").textContent = "Add a customer";
  document.querySelector("#customer-cancel").hidden = true;
}

function editCustomer(customer) {
  document.querySelector("#customer-id").value = customer.id;
  document.querySelector("#customer-name").value = customer.name;
  document.querySelector("#customer-phone").value = customer.phone;
  document.querySelector("#customer-address").value = customer.address;
  document.querySelector("#customer-form-title").textContent = "Edit customer";
  document.querySelector("#customer-cancel").hidden = false;
  document.querySelector("#customer-name").focus();
}

async function deleteCustomer(id) {
  if (!confirm("Delete this customer? Customers with existing orders cannot be deleted.")) return;
  try {
    await api(`/api/customers/${id}`, { method: "DELETE" });
    showNotice("Customer deleted.");
    await refreshData();
  } catch (error) {
    showNotice(error.message, true);
  }
}

async function submitCustomer(event) {
  event.preventDefault();
  const id = document.querySelector("#customer-id").value;
  const payload = {
    name: document.querySelector("#customer-name").value.trim(),
    phone: document.querySelector("#customer-phone").value.trim(),
    address: document.querySelector("#customer-address").value.trim(),
  };
  try {
    await api(id ? `/api/customers/${id}` : "/api/customers", {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(payload),
    });
    resetCustomerForm();
    showNotice(id ? "Customer updated." : "Customer added.");
    await refreshData();
  } catch (error) {
    showNotice(error.message, true);
  }
}

async function loadMenu() {
  const search = document.querySelector("#menu-search").value.trim();
  const query = search ? `?search=${encodeURIComponent(search)}` : "";
  state.menuItems = await api(`/api/menu-items${query}`);
  const body = document.querySelector("#menu-list");
  document.querySelector("#menu-count").textContent = `${state.menuItems.length} shown`;
  if (!state.menuItems.length) {
    emptyRow(body, 4, "No menu items found.");
  } else {
    body.replaceChildren(...state.menuItems.map((item) => {
      const row = element("tr");
      const title = element("td");
      title.append(element("strong", item.name), element("div", item.description || "", "muted"));
      row.append(title, element("td", money(item.price)));
      const availability = element("td");
      availability.append(element("span", item.available ? "Available" : "Unavailable", `badge${item.available ? " available" : ""}`));
      row.append(availability);
      const actions = element("td");
      const actionGroup = element("div", undefined, "actions");
      actionGroup.append(
        button("Edit", () => editMenuItem(item)),
        button("Delete", () => deleteMenuItem(item.id), "text-button delete"),
      );
      actions.append(actionGroup);
      row.append(actions);
      return row;
    }));
  }
  updateOrderItemOptions();
}

function resetMenuForm() {
  document.querySelector("#menu-form").reset();
  document.querySelector("#menu-id").value = "";
  document.querySelector("#menu-available").checked = true;
  document.querySelector("#menu-form-title").textContent = "Add a menu item";
  document.querySelector("#menu-cancel").hidden = true;
}

function editMenuItem(item) {
  document.querySelector("#menu-id").value = item.id;
  document.querySelector("#menu-name").value = item.name;
  document.querySelector("#menu-description").value = item.description || "";
  document.querySelector("#menu-price").value = item.price;
  document.querySelector("#menu-available").checked = item.available;
  document.querySelector("#menu-form-title").textContent = "Edit menu item";
  document.querySelector("#menu-cancel").hidden = false;
  document.querySelector("#menu-name").focus();
}

async function deleteMenuItem(id) {
  if (!confirm("Delete this menu item? Items used in orders cannot be deleted.")) return;
  try {
    await api(`/api/menu-items/${id}`, { method: "DELETE" });
    showNotice("Menu item deleted.");
    await refreshData();
  } catch (error) {
    showNotice(error.message, true);
  }
}

async function submitMenuItem(event) {
  event.preventDefault();
  const id = document.querySelector("#menu-id").value;
  const payload = {
    name: document.querySelector("#menu-name").value.trim(),
    description: document.querySelector("#menu-description").value.trim(),
    price: Number(document.querySelector("#menu-price").value),
    available: document.querySelector("#menu-available").checked,
  };
  try {
    await api(id ? `/api/menu-items/${id}` : "/api/menu-items", {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(payload),
    });
    resetMenuForm();
    showNotice(id ? "Menu item updated." : "Menu item added.");
    await refreshData();
  } catch (error) {
    showNotice(error.message, true);
  }
}

function updateOrderItemOptions() {
  document.querySelectorAll(".order-item-menu").forEach((select) => {
    const currentValue = select.value;
    select.replaceChildren(new Option("Choose a menu item", ""));
    state.menuItems.filter((item) => item.available).forEach((item) => {
      select.add(new Option(`${item.name} · ${money(item.price)}`, item.id));
    });
    if ([...select.options].some((option) => option.value === currentValue)) select.value = currentValue;
  });
}

function addOrderItem() {
  const row = element("div", undefined, "order-item-row");
  const itemLabel = element("label", "Menu item");
  const itemSelect = element("select", undefined, "order-item-menu");
  itemSelect.required = true;
  itemLabel.append(itemSelect);
  const quantityLabel = element("label", "Qty");
  const quantity = element("input");
  quantity.type = "number";
  quantity.min = "1";
  quantity.step = "1";
  quantity.value = "1";
  quantity.required = true;
  quantityLabel.append(quantity);
  row.append(itemLabel, quantityLabel, button("×", () => row.remove(), "text-button delete"));
  document.querySelector("#order-items").append(row);
  updateOrderItemOptions();
}

async function submitOrder(event) {
  event.preventDefault();
  const rows = [...document.querySelectorAll(".order-item-row")];
  if (!rows.length) {
    showNotice("Add at least one menu item to the order.", true);
    return;
  }
  const payload = {
    customer_id: Number(document.querySelector("#order-customer").value),
    items: rows.map((row) => ({
      menu_item_id: Number(row.querySelector(".order-item-menu").value),
      quantity: Number(row.querySelector('input[type="number"]').value),
    })),
  };
  if (!payload.customer_id || payload.items.some((item) => !item.menu_item_id || item.quantity < 1)) {
    showNotice("Choose a customer and valid menu items and quantities.", true);
    return;
  }
  try {
    await api("/orders", { method: "POST", body: JSON.stringify(payload) });
    document.querySelector("#order-form").reset();
    document.querySelector("#order-items").replaceChildren();
    addOrderItem();
    showNotice("Order placed.");
    await refreshData();
  } catch (error) {
    showNotice(error.message, true);
  }
}

async function loadOrders() {
  const status = document.querySelector("#order-filter").value;
  const query = status ? `?status=${encodeURIComponent(status)}` : "";
  state.orders = (await api(`/orders${query}`)).orders;
  const body = document.querySelector("#orders-list");
  if (!state.orders.length) {
    emptyRow(body, 5, "No orders found.");
    return;
  }
  body.replaceChildren(...state.orders.map((order) => {
    const customer = state.customers.find((item) => item.id === order.customer_id);
    const row = element("tr");
    row.append(
      element("td", `#${order.id}`),
      element("td", customer?.name || `Customer #${order.customer_id}`),
      element("td", money(order.total_amount)),
    );
    const statusCell = element("td");
    statusCell.append(element("span", order.status.replaceAll("_", " "), "badge"));
    row.append(statusCell);
    const updateCell = element("td");
    const select = element("select");
    select.setAttribute("aria-label", `New status for order ${order.id}`);
    select.add(new Option("Update status", ""));
    NEXT_STATUSES[order.status].forEach((status) => select.add(new Option(status.replaceAll("_", " "), status)));
    updateCell.append(select, button("Save", () => updateOrderStatus(order.id, select.value)));
    row.append(updateCell);
    return row;
  }));
}

async function updateOrderStatus(id, status) {
  if (!status) {
    showNotice("Choose a new order status.", true);
    return;
  }
  try {
    await api(`/orders/${id}/status`, { method: "PATCH", body: JSON.stringify({ status }) });
    showNotice(`Order #${id} updated.`);
    await refreshData();
  } catch (error) {
    showNotice(error.message, true);
  }
}

async function refreshData() {
  try {
    await Promise.all([loadDashboard(), loadCustomers(), loadMenu()]);
    populateStatusFilter();
    await loadOrders();
  } catch (error) {
    showNotice(error.message, true);
  }
}

function populateStatusFilter() {
  const filter = document.querySelector("#order-filter");
  const currentValue = filter.value;
  filter.replaceChildren(new Option("All statuses", ""));
  STATUSES.forEach((status) => filter.add(new Option(status.replaceAll("_", " "), status)));
  filter.value = currentValue;
}

document.querySelector("#customer-form").addEventListener("submit", submitCustomer);
document.querySelector("#customer-cancel").addEventListener("click", resetCustomerForm);
document.querySelector("#menu-form").addEventListener("submit", submitMenuItem);
document.querySelector("#menu-cancel").addEventListener("click", resetMenuForm);
document.querySelector("#order-form").addEventListener("submit", submitOrder);
document.querySelector("#add-order-item").addEventListener("click", addOrderItem);
document.querySelector("#customer-search").addEventListener("input", () => loadCustomers().catch((error) => showNotice(error.message, true)));
document.querySelector("#menu-search").addEventListener("input", () => loadMenu().catch((error) => showNotice(error.message, true)));
document.querySelector("#order-filter").addEventListener("change", () => loadOrders().catch((error) => showNotice(error.message, true)));
document.querySelector("#refresh-button").addEventListener("click", refreshData);

populateStatusFilter();
addOrderItem();
refreshData();
