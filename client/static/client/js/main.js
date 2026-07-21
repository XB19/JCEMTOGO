const PRODUCTS = {
  'c20-25': { name: 'Béton C20/25', short: 'C20', category: 'BPE', unit: 'm³', price: 65000 },
  'c25-30': { name: 'Béton C25/30', short: 'C25', category: 'BPE', unit: 'm³', price: 75000 },
  'c30-37': { name: 'Béton C30/37', short: 'C30', category: 'BPE', unit: 'm³', price: 85000 },
  'c35-45': { name: 'Béton C35/45', short: 'C35', category: 'BPE', unit: 'm³', price: 98000 },
  'mortier-m10': { name: 'Mortier M10', short: 'M10', category: 'Mortier', unit: 'sac', price: 4200 },
  'gravillon-5-15': { name: 'Gravillon 5/15', short: 'GR5', category: 'Agrégat', unit: 't', price: 28000 },
};

let cart = [];

function fmt(n) {
  return Math.round(n).toLocaleString('fr-FR');
}

function minQtyFor(id) {
  return PRODUCTS[id].unit === 'm³' ? 0.5 : 1;
}

function cartLineTotal(item) {
  return Math.round(item.qty * PRODUCTS[item.id].price);
}

function cartSubtotal() {
  return cart.reduce((sum, item) => sum + cartLineTotal(item), 0);
}

function addToCart(id, qty) {
  const product = PRODUCTS[id];
  if (!product) return;
  qty = qty && qty > 0 ? qty : minQtyFor(id);
  const existing = cart.find((item) => item.id === id);
  if (existing) {
    existing.qty = Math.round((existing.qty + qty) * 100) / 100;
  } else {
    cart.push({ id, qty });
  }
  renderCart();
}

function removeFromCart(id) {
  cart = cart.filter((item) => item.id !== id);
  renderCart();
}

function changeCartQty(id, delta) {
  const item = cart.find((i) => i.id === id);
  if (!item) return;
  item.qty = Math.max(minQtyFor(id), Math.round((item.qty + delta) * 100) / 100);
  renderCart();
}

function setCartQty(id, value) {
  const item = cart.find((i) => i.id === id);
  if (!item) return;
  let v = parseFloat(value);
  if (isNaN(v) || v < minQtyFor(id)) v = minQtyFor(id);
  item.qty = v;
  renderCart();
}

function showNotice(message) {
  let el = document.getElementById('site-toast');
  if (!el) {
    el = document.createElement('div');
    el.id = 'site-toast';
    document.body.appendChild(el);
  }
  el.textContent = message;
  el.classList.add('show');
  clearTimeout(showNotice._timer);
  showNotice._timer = setTimeout(() => el.classList.remove('show'), 3200);
}

function updateCartBadge() {
  document.querySelectorAll('.cart-count').forEach((el) => {
    el.textContent = cart.length;
    const badge = el.closest('button') || el;
    badge.classList.remove('badge-pulse');
    void badge.offsetWidth;
    badge.classList.add('badge-pulse');
  });
}

function createRipple(event, target) {
  const rect = target.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  const ripple = document.createElement('span');
  ripple.className = 'btn-ripple';
  ripple.style.width = ripple.style.height = size + 'px';
  ripple.style.left = (event.clientX - rect.left - size / 2) + 'px';
  ripple.style.top = (event.clientY - rect.top - size / 2) + 'px';
  target.appendChild(ripple);
  ripple.addEventListener('animationend', () => ripple.remove());
}

function initRipples() {
  document.addEventListener('click', (event) => {
    const target = event.target.closest('.btn, .pay-opt, .ptab, .tab, .slot:not(.full)');
    if (!target) return;
    createRipple(event, target);
  });
}

function initReveal() {
  const els = document.querySelectorAll('.reveal, .reveal-stagger');
  if (!els.length) return;
  if (!('IntersectionObserver' in window)) {
    els.forEach((el) => el.classList.add('is-visible'));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );
  els.forEach((el) => observer.observe(el));
}

function initCountUp() {
  const stats = document.querySelectorAll('.hero-stat-val');
  if (!stats.length || !('IntersectionObserver' in window)) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const match = el.textContent.trim().match(/^(\d+)(.*)$/);
        observer.unobserve(el);
        if (!match) return;
        const target = parseInt(match[1], 10);
        const suffix = match[2];
        const step = Math.max(1, Math.round(target / 30));
        let current = 0;
        const timer = setInterval(() => {
          current += step;
          if (current >= target) {
            current = target;
            clearInterval(timer);
          }
          el.textContent = current + suffix;
        }, 25);
      });
    },
    { threshold: 0.5 }
  );
  stats.forEach((el) => observer.observe(el));
}

function renderCart() {
  updateCartBadge();
  renderPanier();
  renderCheckoutSummary();
}

function renderPanier() {
  const container = document.getElementById('cart-items-container');
  if (!container) return;

  const emptyState = document.getElementById('cart-empty-state');
  const summaryLines = document.getElementById('panier-summary-lines');
  const countLabel = document.getElementById('panier-count');

  if (countLabel) {
    countLabel.textContent = cart.length + (cart.length > 1 ? ' articles' : ' article');
  }

  if (cart.length === 0) {
    container.innerHTML = '';
    if (emptyState) emptyState.style.display = 'block';
  } else {
    if (emptyState) emptyState.style.display = 'none';
    container.innerHTML = cart
      .map((item) => {
        const p = PRODUCTS[item.id];
        const step = minQtyFor(item.id);
        return `
        <div class="cart-item">
          <div class="cart-item-img"><span>${p.short}</span></div>
          <div><div class="citem-name">${p.name}</div><div class="citem-sub">${p.category} · ${p.unit}</div></div>
          <div class="cart-qty">
            <button onclick="changeCartQty('${item.id}', -${step})">−</button>
            <input type="number" value="${item.qty}" min="${step}" step="${step}" onchange="setCartQty('${item.id}', this.value)" />
            <button onclick="changeCartQty('${item.id}', ${step})">+</button>
          </div>
          <div class="citem-price">${fmt(cartLineTotal(item))} FCFA</div>
          <button type="button" class="cart-remove" onclick="removeFromCart('${item.id}')" aria-label="Retirer ${p.name}">✕</button>
        </div>`;
      })
      .join('');
  }

  if (summaryLines) {
    summaryLines.innerHTML = cart
      .map((item) => {
        const p = PRODUCTS[item.id];
        return `<div class="sum-line"><span>${p.name} × ${item.qty} ${p.unit}</span><span>${fmt(cartLineTotal(item))}</span></div>`;
      })
      .join('');
  }

  const subtotal = cartSubtotal();
  const subtotEl = document.getElementById('subtot');
  const totEl = document.getElementById('tot-ht');
  if (subtotEl) subtotEl.textContent = fmt(subtotal);
  if (totEl) totEl.textContent = fmt(subtotal) + ' FCFA';
}

function renderCheckoutSummary() {
  const container = document.getElementById('checkout-summary-lines');
  if (!container) return;

  container.innerHTML =
    cart
      .map((item) => {
        const p = PRODUCTS[item.id];
        return `<div class="sum-line"><span>${p.name} × ${item.qty} ${p.unit}</span><span>${fmt(cartLineTotal(item))}</span></div>`;
      })
      .join('') || '<div class="sum-line"><span>Panier vide</span><span>0</span></div>';

  const subtotal = cartSubtotal();
  const subEl = document.getElementById('summary-subtotal');
  const totEl = document.getElementById('summary-total');
  if (subEl) subEl.textContent = fmt(subtotal);
  if (totEl) totEl.textContent = fmt(subtotal) + ' FCFA';
}

function goToCheckout(el) {
  if (cart.length === 0) {
    showNotice('Votre panier est vide — choisissez un produit avant de passer commande.');
    showPage('produits', null);
    return;
  }
  showPage('checkout', el || null);
}

function showPage(id, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const pg = document.getElementById('page-' + id);
  if (pg) {
    pg.classList.add('active');
    window.scrollTo(0, 0);
  }
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
  if (el) el.classList.add('active');
}

function calcVol() {
  const lEl = document.getElementById('c-l');
  if (!lEl) return;
  const l = parseFloat(lEl.value) || 0;
  const w = parseFloat(document.getElementById('c-w').value) || 0;
  const h = parseFloat(document.getElementById('c-h').value) || 0;
  const productId = document.getElementById('c-type').value;
  const product = PRODUCTS[productId];
  const price = product ? product.price : 85000;
  const vol = l * w * h;
  document.getElementById('c-vol').textContent = vol.toFixed(2) + ' m³';
  document.getElementById('c-price').textContent = fmt(vol * price) + ' FCFA';
}

function orderFromCalc() {
  const l = parseFloat(document.getElementById('c-l').value) || 0;
  const w = parseFloat(document.getElementById('c-w').value) || 0;
  const h = parseFloat(document.getElementById('c-h').value) || 0;
  const vol = Math.round(l * w * h * 100) / 100;
  if (vol < 0.5) {
    showNotice('Le volume minimum de commande est 0,5 m³.');
    return;
  }
  const productId = document.getElementById('c-type').value;
  addToCart(productId, vol);
  goToCheckout();
}

function chgQty(d) {
  const inp = document.getElementById('det-qty');
  let v = parseFloat(inp.value) + d;
  if (v < 0.5) v = 0.5;
  inp.value = v.toFixed(1);
  updDetTotal();
}

function updDetTotal() {
  const qtyEl = document.getElementById('det-qty');
  if (!qtyEl) return;
  const v = parseFloat(qtyEl.value) || 0;
  document.getElementById('det-total').textContent = fmt(v * PRODUCTS['c30-37'].price) + ' FCFA';
}

function addToCartFromDetail() {
  const qty = parseFloat(document.getElementById('det-qty').value) || 1;
  addToCart('c30-37', qty);
  showPage('panier', null);
}

function orderFromDetail() {
  const qty = parseFloat(document.getElementById('det-qty').value) || 1;
  addToCart('c30-37', qty);
  goToCheckout();
}

function selPay(el) {
  document.querySelectorAll('.pay-opt').forEach(o => o.classList.remove('selected'));
  el.classList.add('selected');
  const label = document.getElementById('pay-note-label');
  const text = document.getElementById('pay-note-text');
  if (label) label.textContent = el.dataset.label || '';
  if (text) text.textContent = el.dataset.note || '';
}

function getSelectedSlot() {
  const slot = document.querySelector('#order-slot-grid .slot.selected');
  return slot ? slot.dataset.slot : '';
}

function getSelectedPaymentMethod() {
  const pay = document.querySelector('.pay-opt.selected');
  return pay ? pay.dataset.method : 'tmoney';
}

function submitOrder(event) {
  event.preventDefault();

  if (cart.length === 0) {
    showNotice('Votre panier est vide — sélectionnez au moins un produit avant de commander.');
    showPage('produits', null);
    return;
  }

  const products = cart.map((item) => {
    const p = PRODUCTS[item.id];
    return {
      product: p.name,
      quantity: item.qty,
      unit_price: p.price,
      total_price: cartLineTotal(item),
    };
  });

  const total = products.reduce((sum, item) => sum + item.total_price, 0);

  const payload = {
    first_name: document.getElementById('order-first-name').value,
    last_name: document.getElementById('order-last-name').value,
    phone: document.getElementById('order-phone').value,
    email: document.getElementById('order-email').value,
    company: document.getElementById('order-company').value,
    address: document.getElementById('order-address').value,
    instructions: document.getElementById('order-instructions').value,
    delivery_slot: getSelectedSlot(),
    payment_method: getSelectedPaymentMethod(),
    products,
    total_amount: total,
  };

  fetch('/submit-order/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify(payload),
  })
    .then(response => response.json())
    .then(data => {
      if (data.redirect_url) {
        cart = [];
        window.location.href = data.redirect_url;
        return;
      }
      throw new Error('Réponse invalide du serveur');
    })
    .catch(error => {
      console.error('Erreur de soumission:', error);
      showNotice('Une erreur est survenue lors de l’envoi de la commande.');
    });
}

function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta) return meta.content;
  const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
  return cookie ? cookie.trim().split('=')[1] : '';
}

function filterProd(cat, el) {
  document.querySelectorAll('.page-tabs-inner .ptab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('#prod-grid .pcard').forEach(c => {
    c.style.display = cat === 'all' || c.dataset.cat === cat ? 'block' : 'none';
  });
}

function switchTab(el, id) {
  document.querySelectorAll('.tabs-nav .tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.tab-panel').forEach(p => {
    p.classList.remove('active');
    p.style.display = 'none';
  });
  const panel = document.getElementById('tab-' + id);
  if (panel) {
    panel.classList.add('active');
    panel.style.display = 'block';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  calcVol();
  updDetTotal();
  renderCart();
  initRipples();
  initReveal();
  initCountUp();
  document.querySelectorAll('.slot:not(.full)').forEach(s => {
    s.addEventListener('click', () => {
      const parent = s.closest('.slot-grid');
      if (!parent) return;
      parent.querySelectorAll('.slot').forEach(x => x.classList.remove('selected'));
      s.classList.add('selected');
    });
  });
});
