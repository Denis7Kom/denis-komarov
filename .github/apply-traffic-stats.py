from pathlib import Path

page = Path("index.html")
source = page.read_bytes().decode("utf-8")
marker = "goatcounter-stats-v1"
if marker in source:
    print("Already installed")
    raise SystemExit(0)
assert '<footer class="site-footer">' in source
assert "</style>" in source
assert "</body>" in source

css = """
    /* goatcounter-stats-v1 - public traffic widget */
    .traffic-stats {
      width:min(100% - 36px,1200px); margin:0 auto 28px; padding:21px 25px;
      border:1px solid rgba(255,184,77,.20); border-radius:22px;
      background:linear-gradient(130deg,rgba(255,179,71,.075),rgba(255,255,255,.025));
    }
    .traffic-stats__top {display:flex;gap:12px;align-items:center;justify-content:space-between;margin-bottom:14px}
    .traffic-stats__name {font-size:.74rem;font-weight:800;color:var(--accent-3);letter-spacing:.13em}
    .traffic-stats__tag {font:600 .7rem var(--mono);color:var(--muted);letter-spacing:.04em}
    .traffic-stats__grid {display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
    .traffic-stats__item {
      min-width:0;padding:15px 18px;border-radius:14px;
      background:rgba(5,4,3,.45);border:1px solid rgba(255,184,77,.10)
    }
    .traffic-stats__label {display:block;font-size:.78rem;color:var(--muted);font-weight:600}
    .traffic-stats__value {
      display:block;margin-top:6px;font:800 clamp(1.55rem,3vw,2.2rem)/1.15 var(--font);
      color:var(--text);letter-spacing:-.055em;font-variant-numeric:tabular-nums
    }
    .traffic-stats__note {margin-top:12px;font-size:.72rem;line-height:1.6;color:var(--muted-2)}
    @media(max-width:530px){
      .traffic-stats {padding:15px;margin-bottom:20px;border-radius:17px}
      .traffic-stats__item {padding:13px}
      .traffic-stats__top {flex-wrap:wrap}
    }
"""

html = """
  <section class="traffic-stats" aria-label="Site traffic statistics">
    <div class="traffic-stats__top">
      <span class="traffic-stats__name" data-traffic-label="heading">SITE TRAFFIC</span>
      <span class="traffic-stats__tag" data-traffic-label="tag">ANALYTICS</span>
    </div>
    <div class="traffic-stats__grid">
      <div class="traffic-stats__item">
        <span class="traffic-stats__label" data-traffic-label="views">Page views</span>
        <strong class="traffic-stats__value" id="traffic-pageviews" aria-live="polite">—</strong>
      </div>
      <div class="traffic-stats__item">
        <span class="traffic-stats__label" data-traffic-label="visits">Unique visits</span>
        <strong class="traffic-stats__value" id="traffic-visits" aria-live="polite">—</strong>
      </div>
    </div>
    <p class="traffic-stats__note" data-traffic-label="note">Unique visits are session estimates (around 8 hours), not distinct people. Counters update periodically.</p>
  </section>
"""

scripts = """
  <script data-goatcounter="https://denis-komarov.goatcounter.com/count"
          data-goatcounter-settings='{"path":"/denis-komarov/"}'
          async src="https://gc.zgo.at/count.js"></script>
  <script>
    (() => {
      /* goatcounter-stats-v1 - two separate counters, same GoatCounter account */
      const widget = document.querySelector('.traffic-stats');
      if (!widget) return;
      const locales = {
        en:{heading:'SITE TRAFFIC',tag:'ANALYTICS',views:'Page views',visits:'Unique visits',
          note:'Unique visits are session estimates (around 8 hours), not distinct people. Counters update periodically.'},
        ru:{heading:'СТАТИСТИКА САЙТА',tag:'АНАЛИТИКА',views:'Просмотры',visits:'Уникальные визиты',
          note:'Уникальные визиты — оценка по сеансам (около 8 часов), не число разных людей. Данные обновляются с задержкой.'},
        it:{heading:'STATISTICHE DEL SITO',tag:'ANALISI',views:'Visualizzazioni',visits:'Visite uniche',
          note:'Le visite uniche sono stime delle sessioni (circa 8 ore), non persone distinte. I dati si aggiornano con ritardo.'},
        de:{heading:'WEBSITE-STATISTIK',tag:'ANALYSE',views:'Seitenaufrufe',visits:'Einzelne Besuche',
          note:'Einzelne Besuche sind Sitzungs-Schätzungen (etwa 8 Stunden), keine verschiedenen Personen. Daten können verzögert sein.'}
      };
      const totals = {};
      function paint() {
        const lang = document.documentElement.lang;
        const dict = locales[lang] || locales.en;
        widget.querySelectorAll('[data-traffic-label]').forEach(el => {
          el.textContent = dict[el.dataset.trafficLabel];
        });
        for (const [id, value] of Object.entries(totals)) {
          document.getElementById(id).textContent = new Intl.NumberFormat(lang).format(value);
        }
      }
      async function load(path, id) {
        try {
          const endpoint='https://denis-komarov.goatcounter.com/counter/'+encodeURIComponent(path)+'.json';
          const response=await fetch(endpoint,{credentials:'omit',mode:'cors',cache:'no-store'});
          if(!response.ok) return;
          const result=await response.json();
          const digits=String(result.count??'').replace(/[^0-9]/g,'');
          if(digits) { totals[id]=Number(digits); paint(); }
        } catch (_) {
          /* Public counters may be disabled in GoatCounter settings. */
        }
      }
      let registered=false,attempts=0;
      function init() {
        if(registered || !window.goatcounter || typeof window.goatcounter.count!=='function') return false;
        registered=true;
        const gc=window.goatcounter;
        // The automatic hit records a session-counted visit at /denis-komarov/.
        // This event separately records *every* page load, including refreshes.
        if(!gc.filter || !gc.filter()) gc.count({
          path:'/__portfolio_pageviews',title:'Portfolio page loads',
          event:true,no_session:true
        });
        setTimeout(()=>{
          load('/__portfolio_pageviews','traffic-pageviews');
          load('/denis-komarov/','traffic-visits');
        },1100);
        return true;
      }
      document.querySelectorAll('.lang-btn').forEach(btn=>{
        btn.addEventListener('click',()=>requestAnimationFrame(paint));
      });
      paint();
      if(!init()){
        const poll=setInterval(()=>{
          attempts++;
          if(init() || attempts>=100) clearInterval(poll);
        },120);
      }
    })();
  </script>
"""

nl = "\r\n" if "\r\n" in source else "\n"
source = source.replace("</style>", css.replace("\n",nl) + nl + "  </style>", 1)
source = source.replace('<footer class="site-footer">', html.replace("\n",nl) + nl + '  <footer class="site-footer">', 1)
source = source.replace("</body>", scripts.replace("\n",nl) + nl + "</body>", 1)
page.write_bytes(source.encode("utf-8"))
print("Patched index.html, bytes:", page.stat().st_size)
