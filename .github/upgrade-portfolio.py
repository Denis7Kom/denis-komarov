#!/usr/bin/env python3
"""Upgrade the existing single-file portfolio without touching embedded assets."""
from pathlib import Path

file = Path("index.html")
html = file.read_bytes().decode("utf-8")
tag = "portfolio-refresh-v2"
if tag in html:
    print("Upgrade already present")
    raise SystemExit(0)

css = r'''
    /* portfolio-refresh-v2: refined visual system */
    :root { --fx-ease: cubic-bezier(.22,.8,.2,1); }
    ::selection { background:rgba(255,184,77,.35); color:#fff; }
    :where(section[id]) { scroll-margin-top:110px; }
    :where(a,button,summary,input):focus-visible { outline:2px solid #ffd166; outline-offset:3px; }
    .skip-main {
      position:fixed;top:9px;left:12px;z-index:2000;padding:11px 16px;
      background:#ffd166;color:#160a00;border-radius:12px;font-weight:850;
      transform:translateY(-150%);
    }
    .skip-main:focus { transform:translateY(0); }
    .site-header {
      background:rgba(7,6,5,.83);-webkit-backdrop-filter:blur(24px) saturate(140%);
      backdrop-filter:blur(24px) saturate(140%);
      transition:background .25s ease,box-shadow .25s ease;
    }
    .site-header.is-scrolled {
      background:rgba(7,6,5,.94);box-shadow:0 14px 42px rgba(0,0,0,.28);
    }
    .site-header .container.nav {
      width:min(calc(100% - 36px),1450px); min-height:66px;
      gap:clamp(10px,1.15vw,18px);
    }
    .site-header .header-brand { flex-shrink:1;min-width:0; }
    .site-header .nav-links {
      flex-shrink:0;gap:2px;padding:5px;
      background:rgba(255,255,255,.035);
      border-color:rgba(255,184,77,.12);
    }
    .site-header .nav-links a {
      display:inline-flex;align-items:center;justify-content:center;
      padding:9px 10px;line-height:1.15;white-space:nowrap;
      font-size:.82rem;font-weight:740;
    }
    .site-header .nav-links a.active {
      background:linear-gradient(135deg,rgba(255,184,77,.2),rgba(255,106,0,.09));
      box-shadow:inset 0 0 0 1px rgba(255,184,77,.14);
    }
    .site-header .lang-switch {
      flex:0 0 auto;padding:4px;gap:2px;background:rgba(255,255,255,.035);
    }
    .site-header .lang-btn { min-width:34px;min-height:31px;padding:6px 8px; }
    .site-header .nav-cta {
      flex:0 0 auto;white-space:nowrap;padding:10px 14px;font-size:.86rem;
    }
    .command-open,.quick-menu > summary,.back-top {
      appearance:none;display:inline-grid;place-items:center;flex:0 0 auto;
      width:40px;height:40px;border:1px solid rgba(255,184,77,.23);
      background:rgba(255,255,255,.045);color:var(--text);
      border-radius:14px;cursor:pointer;
      transition:background .2s ease,border-color .2s ease,transform .2s ease;
    }
    .command-open:hover,.quick-menu > summary:hover,.back-top:hover {
      background:rgba(255,184,77,.14);border-color:rgba(255,184,77,.46);
      transform:translateY(-2px);
    }
    .command-open svg,.quick-menu svg { display:block;width:18px;height:18px; }
    .quick-menu { position:relative;display:none;flex:0 0 auto;z-index:12; }
    .quick-menu > summary { list-style:none; }
    .quick-menu > summary::-webkit-details-marker { display:none; }
    .quick-menu[open] > summary { background:rgba(255,184,77,.18); }
    .quick-menu-panel {
      position:absolute;z-index:15;top:calc(100% + 14px);right:0;
      display:grid;gap:4px;width:min(290px,calc(100vw - 28px));padding:10px;
      background:rgba(15,11,8,.97);border:1px solid rgba(255,184,77,.24);
      border-radius:22px;box-shadow:0 26px 70px rgba(0,0,0,.55);
      -webkit-backdrop-filter:blur(28px);backdrop-filter:blur(28px);
      animation:quick-appear .25s cubic-bezier(.22,.8,.2,1) both;
    }
    .quick-menu-panel a {
      display:flex;padding:12px 14px;white-space:nowrap;
      color:var(--muted);border-radius:12px;font-size:.94rem;
    }
    .quick-menu-panel a:hover,.quick-menu-panel a.active {
      color:var(--text);background:rgba(255,184,77,.13);
    }
    @keyframes quick-appear {
      from { opacity:0;transform:translateY(-8px) scale(.98); }
      to { opacity:1;transform:translateY(0) scale(1); }
    }
    .hero { isolation:isolate; }
    .hero::after {
      content:"";position:absolute;z-index:-1;top:0;right:0;
      width:min(680px,62vw);height:min(620px,65vh);pointer-events:none;
      background:radial-gradient(ellipse,rgba(255,178,87,.1),transparent 68%);
      filter:blur(36px);
    }
    .hero-content h1 { text-wrap:balance;text-shadow:0 16px 54px rgba(0,0,0,.18); }
    .hero .gradient-text {
      background-image:linear-gradient(113deg,#fffaf1 0%,#ffda96 27%,#ff9d4a 65%,#ffcd83 100%);
      background-size:200% 100%;animation:gradient-drift 12s ease-in-out infinite alternate;
    }
    @keyframes gradient-drift { to { background-position:100% 0; } }
    .eyebrow,.trusted-pill,.mini-tag {
      -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
    }
    .section-kicker { letter-spacing:.15em; }
    .section-head h2 { text-wrap:balance; }
    .card,.education-card,.creative-card,.direction-card {
      border-color:rgba(255,184,77,.16);
      box-shadow:0 15px 45px rgba(0,0,0,.19),inset 0 1px 0 rgba(255,255,255,.035);
    }
    .card {
      transition:transform .32s var(--fx-ease),background .32s ease,
                 border-color .32s ease,box-shadow .32s ease;
    }
    .card::before {
      background:radial-gradient(350px circle at var(--spot-x,50%) var(--spot-y,0%),
                                rgba(255,190,105,.15),transparent 72%);
    }
    .card:hover {
      transform:translateY(-7px);border-color:rgba(255,190,106,.42);
      box-shadow:0 28px 65px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.08);
    }
    .project-card { min-width:0;border-radius:28px; }
    .project-preview,.project-preview-placeholder {
      border-radius:16px;border-color:rgba(255,184,77,.17);
    }
    .project-preview img {
      transition:transform .7s var(--fx-ease),filter .5s ease,opacity .5s ease;
    }
    .project-card:hover .project-preview img {
      transform:scale(1.06);filter:saturate(1.1) contrast(1.06);
    }
    .contact-link,.copy-mail {
      transition:border-color .22s ease,background .22s ease,transform .22s ease;
    }
    .contact-link:hover,.copy-mail:hover {
      border-color:rgba(255,184,77,.48);
      background:rgba(255,184,77,.12);transform:translateY(-2px);
    }
    .back-top {
      position:fixed;z-index:70;right:23px;bottom:24px;
      width:47px;height:47px;border-radius:16px;
      box-shadow:0 18px 50px rgba(0,0,0,.36);
      opacity:0;visibility:hidden;pointer-events:none;transform:translateY(12px);
    }
    .back-top.is-visible {
      opacity:1;visibility:visible;pointer-events:auto;transform:translateY(0);
    }
    .command-dialog {
      width:min(570px,calc(100vw - 28px));max-height:min(620px,80vh);
      padding:0;color:var(--text);overflow:hidden;border-radius:26px;
      background:linear-gradient(155deg,rgba(31,22,16,.99),rgba(9,8,7,.99));
      border:1px solid rgba(255,184,77,.28);
      box-shadow:0 40px 120px rgba(0,0,0,.72);
    }
    .command-dialog[open] { animation:quick-appear .25s var(--fx-ease); }
    .command-dialog::backdrop {
      background:rgba(0,0,0,.7);-webkit-backdrop-filter:blur(9px);
      backdrop-filter:blur(9px);
    }
    .command-search-row {
      display:flex;align-items:center;gap:12px;padding:18px 20px;
      border-bottom:1px solid rgba(255,184,77,.18);
    }
    .command-search-icon { font-size:22px;color:var(--accent); }
    .command-query {
      width:100%;min-width:0;border:0;outline:0;background:transparent;
      color:var(--text);font:600 1.02rem var(--font);
    }
    .command-query::placeholder { color:var(--muted-2); }
    .command-close {
      flex:0 0 auto;padding:7px 9px;border:1px solid rgba(255,184,77,.2);
      border-radius:9px;background:rgba(255,255,255,.04);
      color:var(--muted);cursor:pointer;
    }
    .command-results {
      display:grid;gap:5px;padding:11px;max-height:min(450px,56vh);overflow-y:auto;
    }
    .command-result {
      display:flex;align-items:center;justify-content:space-between;
      gap:12px;width:100%;padding:14px 16px;border:0;border-radius:12px;
      color:var(--text);background:transparent;text-align:left;cursor:pointer;
      font:700 .95rem var(--font);
    }
    .command-result:hover,.command-result:focus-visible {
      background:rgba(255,184,77,.13);
    }
    .command-result span:last-child { color:var(--accent); }
    .command-empty { padding:18px;color:var(--muted); }
    .command-hint {
      padding:11px 20px 15px;color:var(--muted-2);font-size:.78rem;
      border-top:1px solid rgba(255,184,77,.11);
    }
    @media (max-width:1399px) {
      .site-header .nav-links { display:none; }
      .quick-menu { display:block; }
    }
    @media (max-width:720px) {
      .site-header .container.nav {
        display:grid;grid-template-columns:minmax(0,1fr) 40px 40px;
        grid-template-areas:"brand search menu" "langs langs langs";
        justify-content:stretch;align-items:center;gap:9px;
        width:min(calc(100% - 24px),1450px);padding:9px 0;
      }
      .site-header .header-brand {
        grid-area:brand;width:auto;justify-content:flex-start;
        min-height:40px;overflow:hidden;
      }
      .site-header .header-signature-svg { width:min(39vw,172px);height:36px; }
      .site-header .lang-switch {
        grid-area:langs;order:initial;width:min(100%,340px);
        justify-self:center;margin:0;gap:5px;
      }
      .site-header .lang-btn { min-height:32px; }
      .command-open { grid-area:search; }
      .quick-menu { grid-area:menu; }
      .site-header .nav-cta,.site-header .nav-links { display:none; }
      :where(section[id]) { scroll-margin-top:142px; }
      .hero .gradient-text { animation:none; }
      .back-top { right:14px;bottom:14px; }
      .card:hover { transform:none; }
    }
    @media (prefers-reduced-motion:reduce) {
      .hero .gradient-text,.quick-menu-panel,.command-dialog[open] {
        animation:none!important;
      }
      .card:hover,.contact-link:hover,.copy-mail:hover { transform:none; }
      .back-top { transition:none; }
    }
'''

menu = r'''
      <details class="quick-menu">
        <summary aria-label="Open navigation menu" title="Navigation">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
        </summary>
        <nav class="quick-menu-panel" aria-label="Compact navigation">
          <a href="#about">About</a><a href="#services">Build</a><a href="#stack">Stack</a>
          <a href="#work">Work</a><a href="#aviation">Aviation</a><a href="#contact">Contact</a>
        </nav>
      </details>
      <button class="command-open" type="button" aria-label="Quick navigation" title="Quick navigation (Ctrl+K)">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/></svg>
      </button>
'''

js = r'''
    /* portfolio-refresh-v2: navigation, search and subtle effects */
    (() => {
      const reduced = matchMedia('(prefers-reduced-motion: reduce)');
      const finePointer = matchMedia('(hover:hover) and (pointer:fine)');
      const header = document.querySelector('.site-header');
      const details = document.querySelector('.quick-menu');
      const mobileLinks = [...document.querySelectorAll('.quick-menu-panel a')];
      const links = [...document.querySelectorAll('.nav-links a')];
      const commandButton = document.querySelector('.command-open');
      const copy = {
        en: {search:'Find a section…',empty:'No matching sections',hint:'Enter to open · Esc to close',menu:'Open navigation menu',quick:'Quick navigation (Ctrl+K)',top:'Back to top',skip:'Skip to content'},
        ru: {search:'Найти раздел…',empty:'Разделы не найдены',hint:'Enter — открыть · Esc — закрыть',menu:'Открыть меню',quick:'Быстрая навигация (Ctrl+K)',top:'Наверх',skip:'К содержимому'},
        it: {search:'Cerca una sezione…',empty:'Nessuna sezione trovata',hint:'Invio per aprire · Esc per chiudere',menu:'Apri il menu',quick:'Navigazione rapida (Ctrl+K)',top:'Torna su',skip:'Vai al contenuto'},
        de: {search:'Abschnitt suchen…',empty:'Keine passenden Abschnitte',hint:'Enter zum Öffnen · Esc zum Schließen',menu:'Menü öffnen',quick:'Schnellnavigation (Ctrl+K)',top:'Nach oben',skip:'Zum Inhalt'}
      };
      const local = () => copy[document.documentElement.lang] || copy.en;
      const dialog = document.createElement('dialog');
      dialog.className = 'command-dialog';
      dialog.setAttribute('aria-label', 'Quick navigation');
      dialog.innerHTML = '<div class="command-search-row"><span class="command-search-icon" aria-hidden="true">⌕</span><input class="command-query" type="search" autocomplete="off" aria-label="Find a section"><button class="command-close" type="button" aria-label="Close">Esc</button></div><div class="command-results"></div><div class="command-hint"></div>';
      document.body.append(dialog);
      const input = dialog.querySelector('.command-query');
      const results = dialog.querySelector('.command-results');
      const hint = dialog.querySelector('.command-hint');
      dialog.querySelector('.command-close').addEventListener('click', () => dialog.close());
      dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
      const topButton = document.createElement('button');
      topButton.className = 'back-top';
      topButton.type = 'button';
      topButton.textContent = '↑';
      document.body.append(topButton);

      function render() {
        const query = input.value.trim().toLocaleLowerCase();
        const found = links.filter(link => link.textContent.toLocaleLowerCase().includes(query));
        results.replaceChildren();
        if (!found.length) {
          const empty = document.createElement('p');
          empty.className = 'command-empty';
          empty.textContent = local().empty;
          results.append(empty);
        }
        found.forEach(link => {
          const row = document.createElement('button');
          row.type = 'button';
          row.className = 'command-result';
          const title = document.createElement('span');
          title.textContent = link.textContent.trim();
          const arrow = document.createElement('span');
          arrow.textContent = '↗'; arrow.setAttribute('aria-hidden','true');
          row.append(title,arrow);
          row.addEventListener('click', () => {
            const anchor = link.getAttribute('href');
            dialog.close();
            if (anchor) {
              history.pushState(null,'',anchor);
              document.querySelector(anchor)?.scrollIntoView({
                behavior: reduced.matches ? 'auto':'smooth'
              });
            }
          });
          results.append(row);
        });
      }

      function updateUI() {
        const c = local();
        input.placeholder = c.search;
        input.setAttribute('aria-label',c.search);
        hint.textContent = c.hint;
        details.querySelector('summary').setAttribute('aria-label',c.menu);
        commandButton.setAttribute('aria-label',c.quick);
        commandButton.title = c.quick;
        topButton.setAttribute('aria-label',c.top);
        topButton.title = c.top;
        const skip = document.querySelector('.skip-main');
        if(skip)skip.textContent = c.skip;
        if(dialog.open)render();
      }
      function openPalette() {
        if (dialog.open || typeof dialog.showModal !== 'function') return;
        details.open = false;
        input.value = '';
        updateUI(); render(); dialog.showModal(); input.focus();
      }
      commandButton.addEventListener('click',openPalette);
      input.addEventListener('input',render);
      input.addEventListener('keydown',e => {
        if (e.key==='ArrowDown') {
          const first=results.querySelector('button');
          if(first){e.preventDefault();first.focus();}
        } else if(e.key==='Enter') {
          const first=results.querySelector('button');
          if(first){e.preventDefault();first.click();}
        }
      });
      results.addEventListener('keydown',e => {
        if (e.key!=='ArrowDown'&&e.key!=='ArrowUp') return;
        const buttons=[...results.querySelectorAll('button')];
        const n=buttons.indexOf(document.activeElement);
        const next=e.key==='ArrowDown' ? buttons[(n+1)%buttons.length] :
          buttons[(n-1+buttons.length)%buttons.length];
        if(next){e.preventDefault();next.focus();}
      });
      window.addEventListener('keydown',e => {
        if ((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k') {
          e.preventDefault();
          if(dialog.open)dialog.close();else openPalette();
        } else if(e.key==='Escape'&&details.open){details.open=false;}
      });
      mobileLinks.forEach(link=>link.addEventListener('click',()=>{details.open=false;}));
      document.addEventListener('click',e => {
        if(details.open&&!details.contains(e.target))details.open=false;
      });
      const sync = () => {
        const active=links.find(link=>link.classList.contains('active'))?.getAttribute('href');
        mobileLinks.forEach(link=>link.classList.toggle('active',link.getAttribute('href')===active));
      };
      let ticking=false;
      window.addEventListener('scroll',()=>{
        if(ticking)return;
        ticking=true;
        requestAnimationFrame(()=>{
          header.classList.toggle('is-scrolled',window.scrollY>35);
          topButton.classList.toggle('is-visible',window.scrollY>620);
          sync();
          ticking=false;
        });
      },{passive:true});
      header.classList.toggle('is-scrolled',window.scrollY>35);
      topButton.classList.toggle('is-visible',window.scrollY>620);
      topButton.addEventListener('click',()=>scrollTo({
        top:0,behavior:reduced.matches?'auto':'smooth'
      }));
      document.querySelectorAll('.lang-btn').forEach(button=>{
        button.addEventListener('click',()=>requestAnimationFrame(updateUI));
      });
      updateUI();
      if(finePointer.matches&&!reduced.matches){
        document.querySelectorAll('.card').forEach(card=>{
          card.addEventListener('pointermove',e=>{
            const rect=card.getBoundingClientRect();
            card.style.setProperty('--spot-x',(e.clientX-rect.left)+'px');
            card.style.setProperty('--spot-y',(e.clientY-rect.top)+'px');
          },{passive:true});
        });
      }
    })();
'''

def normalise(snippet):
    newline = "\r\n" if "\r\n" in html else "\n"
    return snippet.strip("\n").replace("\n",newline)

target = '</nav>' + ('\r\n' if '\r\n' in html else '\n') * 2 + '      <div class="lang-switch"'
if target not in html:
    raise SystemExit("Navigation insertion anchor not found")
if html.count("</style>") != 1 or html.count("</script>") != 1:
    raise SystemExit("Unexpected HTML structure")
html = html.replace(target, '</nav>' + normalise("\n"+menu+"\n\n") + ("\r\n" if "\r\n" in html else "\n") * 2 + '      <div class="lang-switch"',1)
html = html.replace("</style>",normalise(css) + ("\r\n" if "\r\n" in html else "\n") + "  </style>",1)
html = html.replace("</script>",normalise(js) + ("\r\n" if "\r\n" in html else "\n") + "  </script>",1)
html = html.replace('<body>','<body>' + ("\r\n" if "\r\n" in html else "\n") + '  <a class="skip-main" href="#top">Skip to content</a>',1)
assert html.count("portfolio-refresh-v2") == 2
assert html.count('data-lang="de"') == 1
assert html.count('<script>') == 1 and html.count('<style>') == 1
file.write_bytes(html.encode("utf-8"))
print("Upgraded",file,len(html),"characters")
