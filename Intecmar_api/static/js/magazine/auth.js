(function () {
  const TOKEN_KEY = 'auth_token';
  function getToken() { try { return localStorage.getItem(TOKEN_KEY) || ''; } catch { return ''; } }
  function setToken(t) { try { if (t) localStorage.setItem(TOKEN_KEY, t); else localStorage.removeItem(TOKEN_KEY); } catch { } }
  function isAuthed() { return !!getToken(); }

  // Override global fetch to inject Authorization and handle 401s
  const _fetch = window.fetch.bind(window);
  window.fetch = async function (input, init) {
    const token = getToken();
    init = init || {};
    init.headers = init.headers || {};
    try {
      const h = new Headers(init.headers);
      if (token && !h.has('Authorization')) h.set('Authorization', `Bearer ${token}`);
      init.headers = h;
    } catch {
      if (token && !init.headers['Authorization']) init.headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await _fetch(input, init);

    // Global session expiry handler
    if (response.status === 401) {
      const isLoginRequest = typeof input === 'string' && input.includes('/api/auth/login');
      if (!isLoginRequest) {
        setToken('');
        // Avoid infinite loop if we're already on /login
        if (!window.location.pathname.includes('/login')) {
          window.location.href = '/login?reason=expired';
        }
      }
    }

    return response;
  };

  async function apiLogin(baseUrl, email, password) {
    const res = await _fetch(`${baseUrl}/api/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
    if (!res.ok) throw new Error('Credenciales inválidas');
    const data = await res.json();
    setToken(data.access_token || '');
    return data;
  }
  async function apiRegister(baseUrl, email, password, name) {
    const res = await _fetch(`${baseUrl}/api/auth/register`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password, name: name || null }) });
    if (!res.ok) throw new Error((await res.json()).detail || 'No se pudo registrar');
    return res.json();
  }
  async function apiMe(baseUrl) {
    const res = await fetch(`${baseUrl}/api/auth/me`);
    if (!res.ok) throw new Error('No autenticado');
    return res.json();
  }

  // Minimal UI wiring if elements exist
  document.addEventListener('DOMContentLoaded', () => {
    const API_URL = document.body?.dataset?.api || window.location.origin;
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const authModal = document.getElementById('authModal');
    const closeAuthModal = document.getElementById('closeAuthModal');
    const authEmail = document.getElementById('authEmail');
    const authPass = document.getElementById('authPass');
    const authName = document.getElementById('authName');
    const doLogin = document.getElementById('doLogin');
    const doRegister = document.getElementById('doRegister');
    const authError = document.getElementById('authError');
    const userBadge = document.getElementById('userBadge');
    const authSuccess = document.getElementById('authSuccess');

    function setAuthedUI(user) {
      const email = user ? user.email : '';
      const name = user ? user.name : '';
      const pic = user ? user.profile_picture : null;

      if (userBadge) userBadge.textContent = email ? `Conectado: ${email}` : 'Sin sesión';
      if (loginBtn) loginBtn.classList.toggle('hidden', !!email);
      if (logoutBtn) logoutBtn.classList.toggle('hidden', !email);

      // Update Magazine Header
      const headerUserName = document.getElementById('headerUserName');
      const dropdownName = document.getElementById('dropdownName');
      const dropdownEmail = document.getElementById('dropdownEmail');
      const avatarCircle = document.querySelector('.avatar-circle');

      if (headerUserName) headerUserName.textContent = (name || email || 'Usuario').split(' ')[0];
      if (dropdownName) dropdownName.textContent = name || email || 'Usuario';
      if (dropdownEmail) dropdownEmail.textContent = email;

      if (avatarCircle) {
        if (pic) {
          avatarCircle.innerHTML = `<img src="${pic}" style="width:100%; height:100%; object-fit:cover; border-radius:50%;" onerror="this.src='/img/default-avatar.png'">`;
        } else {
          avatarCircle.innerHTML = `<i class="fa-solid fa-user"></i>`;
        }
      }

      // Update Agent Sidebar
      const agentUserAvatar = document.getElementById('user-avatar');
      const agentUserName = document.getElementById('user-name');
      const agentUserRole = document.getElementById('user-role');

      if (agentUserName) agentUserName.textContent = name || email || 'Usuario';
      // User requested to show email instead of role below the name in the agent
      if (agentUserRole) agentUserRole.textContent = email || (user && user.role) || 'Usuario';

      if (agentUserAvatar) {
        if (pic) {
          agentUserAvatar.innerHTML = `<img src="${pic}" class="w-full h-full object-cover rounded-full" onerror="this.src='/img/default-avatar.png'">`;
          agentUserAvatar.classList.remove('bg-gradient-to-tr', 'from-blue-500', 'to-cyan-400');
        } else {
          const initials = (name || email || 'U').charAt(0).toUpperCase();
          agentUserAvatar.textContent = initials;
          agentUserAvatar.classList.add('bg-gradient-to-tr', 'from-blue-500', 'to-cyan-400');
        }
      }

      // Initialize Agent User Menu (Three Dots)
      const agentMenuBtn = document.getElementById('agentUserMenuBtn');
      const agentDropdown = document.getElementById('agentUserDropdown');
      const agentLogout = document.getElementById('agentLogoutBtn');

      if (agentMenuBtn && agentDropdown) {
        agentMenuBtn.onclick = (e) => {
          e.stopPropagation();
          agentDropdown.classList.toggle('hidden');
        };
        document.addEventListener('click', () => agentDropdown.classList.add('hidden'));
      }

      if (agentLogout) {
        agentLogout.onclick = () => {
          setToken('');
          window.location.href = '/login';
        };
      }
    }

    async function refreshMe() {
      try {
        const me = await apiMe(API_URL);
        setAuthedUI(me);
        try {
          if (me?.email) localStorage.setItem('user_email', me.email);
          if (me?.name) localStorage.setItem('user_name', me.name);
          if (me?.profile_picture) localStorage.setItem('user_pic', me.profile_picture);
        } catch { }
      }
      catch {
        setAuthedUI(null);
      }
    }

    if (loginBtn) loginBtn.addEventListener('click', () => { if (authModal) { authModal.classList.remove('hidden'); authModal.setAttribute('aria-hidden', 'false'); authError.textContent = ''; } });
    if (closeAuthModal) closeAuthModal.addEventListener('click', () => { if (authModal) { authModal.classList.add('hidden'); authModal.setAttribute('aria-hidden', 'true'); } });
    if (logoutBtn) logoutBtn.addEventListener('click', () => {
      setToken('');
      refreshMe();
      try {
        const onIndex = window.location.pathname.includes('/magazine');
        if (onIndex) window.location.href = '/login';
      } catch { }
    });
    if (doLogin) doLogin.addEventListener('click', async () => {
      if (doLogin.disabled) return;
      doLogin.disabled = true;
      try {
        authError.textContent = '';
        if (authError && authError.style) authError.style.display = 'none';
        await apiLogin(API_URL, authEmail.value.trim(), authPass.value);
        // Persist basic user info after login
        try {
          const me = await apiMe(API_URL);
          if (me?.email) localStorage.setItem('user_email', me.email);
          if (me?.name) localStorage.setItem('user_name', me.name);
        } catch { }
        if (authModal) { authModal.classList.add('hidden'); authModal.setAttribute('aria-hidden', 'true'); }
        await refreshMe();
        // Redirect to app after successful login from login page
        try {
          const onLoginPage = window.location.pathname.includes('/login');
          if (onLoginPage) window.location.href = '/magazine';
        } catch { }
      } catch (e) {
        authError.textContent = e.message || String(e);
        if (authError && authError.style) authError.style.display = 'block';
      } finally { doLogin.disabled = false; }
    });
    if (doRegister) doRegister.addEventListener('click', async () => {
      if (doRegister.disabled) return;
      doRegister.disabled = true;
      try {
        authError.textContent = '';
        if (authError && authError.style) authError.style.display = 'none';
        await apiRegister(API_URL, authEmail.value.trim(), authPass.value, authName?.value?.trim() || null);
        // Show green success, switch to login mode (if login.html provides UI)
        if (authSuccess) { authSuccess.textContent = 'Usuario registrado. Ahora inicia sesión.'; authSuccess.style.display = 'block'; }
        if (typeof window.toggleToLoginMode === 'function') {
          try { window.toggleToLoginMode(); } catch { }
        } else {
          // Fallback: simulate clicking the toggle if exists
          const toggleLink = document.getElementById('toggleMode');
          if (toggleLink) try { toggleLink.click(); } catch { }
        }
      } catch (e) {
        authError.textContent = e.message || String(e);
        if (authError && authError.style) authError.style.display = 'block';
      } finally { doRegister.disabled = false; }
    });

    refreshMe();
  });

  window.__auth__ = { getToken, setToken, isAuthed };
})();
