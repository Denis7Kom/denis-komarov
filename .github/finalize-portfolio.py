from pathlib import Path
p=Path('index.html')
s=p.read_bytes().decode('utf-8')
nl='\r\n' if '\r\n' in s else '\n'
s=s.replace('</nav>      <details class="quick-menu">','</nav>'+nl+nl+'      <details class="quick-menu">',1)
marker='/* portfolio-medium-width-fix */'
if marker not in s:
  css='''
    /* portfolio-medium-width-fix */
    @media (min-width:721px) and (max-width:1000px) {
      .site-header .nav-cta { display:none; }
    }
'''.strip('\n').replace('\n',nl)
  s=s.replace('</style>',css+nl+'  </style>',1)
p.write_bytes(s.encode('utf-8'))
