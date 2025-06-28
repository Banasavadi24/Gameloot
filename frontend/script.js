const API_URL = 'http://127.0.0.1:5000/items';

async function loadItems() {
  const res = await fetch(API_URL);
  const data = await res.json();
  const list = document.getElementById('itemList');
  list.innerHTML = '';
  data.forEach((item, index) => {
    const li = document.createElement('li');
    li.innerHTML = `${item.title} (${item.type}) - €${item.price} - ${item.status}
      <button onclick="deleteItem(${index})">Delete</button>`;
    list.appendChild(li);
  });
}

async function addItem() {
  const title = document.getElementById('title').value;
  const type = document.getElementById('type').value;
  const price = parseFloat(document.getElementById('price').value);
  const status = document.getElementById('status').value;

  await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, type, price, status })
  });
  loadItems();
}

async function deleteItem(index) {
  await fetch(`${API_URL}/${index}`, { method: 'DELETE' });
  loadItems();
}

loadItems();