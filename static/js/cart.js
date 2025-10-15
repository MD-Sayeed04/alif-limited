// static/js/cart.js
(function(){
  // Simple localStorage cart
  const CART_KEY = 'alif_cart';
  function loadCart(){ return JSON.parse(localStorage.getItem(CART_KEY) || '[]'); }
  function saveCart(c){ localStorage.setItem(CART_KEY, JSON.stringify(c)); }
  function addToCart(item){
    const cart = loadCart();
    const found = cart.find(i => i.id === item.id);
    if(found) found.qty += 1;
    else cart.push({...item, qty:1});
    saveCart(cart);
    alert(item.name + ' added to cart');
  }

  document.addEventListener('click', e => {
    if(e.target.matches('.add-to-cart')){
      const el = e.target.closest('.product') || e.target;
      const id = parseInt(el.dataset.id || e.target.dataset.id);
      const name = el.dataset.name || e.target.dataset.name;
      const price = parseFloat(el.dataset.price || e.target.dataset.price);
      addToCart({id, name, price});
    }
    if(e.target.matches('#view-cart')){
      e.preventDefault();
      showCart();
    }
  });

  function showCart(){
    const cart = loadCart();
    if(cart.length === 0) return alert('Cart is empty');
    let html = 'Cart:\\n';
    let total = 0;
    cart.forEach(i => {
      html += `${i.name} x${i.qty} - $${(i.price*i.qty).toFixed(2)}\\n`;
      total += i.price*i.qty;
    });
    html += `Total: $${total.toFixed(2)}\\n\\nEnter details to place order.`;
    // simple prompt-based checkout (replace with a proper form later)
    const name = prompt('Your name:');
    if(!name) return;
    const phone = prompt('Phone:');
    if(!phone) return;
    const address = prompt('Address:');
    if(!address) return;

    fetch('/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, phone, address, items: cart, total })
    })
    .then(r => r.json())
    .then(res => {
      alert(res.message || 'Order placed');
      localStorage.removeItem(CART_KEY);
    })
    .catch(err => alert('Order failed: ' + err));
  }
})();
