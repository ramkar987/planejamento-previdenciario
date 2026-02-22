import streamlit as st
from config import APP_CONFIG

st.set_page_config(
    page_title="PrevPlan | Planejamento Previdenciário",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  section[data-testid="stSidebar"] { display: none; }
  .block-container { padding-top: 1rem; max-width: 1100px; }

  .hero {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
    color: white; padding: 70px 30px; border-radius: 16px;
    text-align: center; margin-bottom: 32px;
  }
  .hero h1 { font-size: clamp(26px, 5vw, 52px); font-weight: 800; margin-bottom: 14px; }
  .hero p  { font-size: clamp(14px, 2vw, 19px); opacity: 0.9; max-width: 660px; margin: 0 auto 10px; }
  .hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    border: 1px solid rgba(255,255,255,0.4);
    padding: 4px 16px; border-radius: 20px;
    font-size: 13px; margin-bottom: 22px;
  }

  .stat-card {
    background: white; padding: 22px 14px; border-radius: 12px;
    text-align: center; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    border-top: 4px solid #667eea; height: 100%;
  }
  .stat-number { font-size: 34px; font-weight: 800; color: #1e3c72; line-height: 1.1; }
  .stat-label  { color: #555; font-size: 13px; margin-top: 6px; }

  .card {
    background: #f5f7ff; padding: 20px; border-radius: 12px;
    border-left: 4px solid #667eea; margin-bottom: 14px;
  }
  .card h4 { color: #1e3c72; margin: 0 0 6px 0; }
  .card p  { color: #555; font-size: 14px; margin: 0; }

  .step-card {
    background: white; padding: 22px; border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07); text-align: center;
  }
  .step-card .step-num {
    font-size: 38px; font-weight: 800; color: #667eea; line-height: 1;
  }

  .testimonial {
    background: white; padding: 24px; border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    font-size: 14px; color: #444; position: relative; height: 100%;
  }
  .testimonial::before {
    content: '"'; font-size: 72px; color: #667eea; opacity: 0.2;
    position: absolute; top: -4px; left: 12px; line-height: 1;
  }
  .testimonial .author { font-weight: 700; color: #1e3c72; margin-top: 14px; font-size: 13px; }

  .cta-banner {
    background: linear-gradient(90deg, #1e3c72 0%, #667eea 100%);
    color: white; padding: 48px 30px; border-radius: 16px;
    text-align: center; margin: 40px 0;
  }
  .cta-banner h2 { font-size: clamp(20px, 3vw, 30px); margin-bottom: 10px; }
  .cta-banner p  { opacity: 0.88; font-size: 16px; margin: 0; }

  div[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border: none !important; color: white !important;
    font-size: 17px !important; font-weight: 700 !important;
    border-radius: 10px !important; width: 100% !important;
    padding: 14px 0 !important; letter-spacing: 0.2px;
    transition: opacity 0.2s;
  }
  div[data-testid="stButton"] > button:hover { opacity: 0.9; }

  .footer {
    text-align: center; color: #999; padding: 28px 0 8px;
    font-size: 12px; border-top: 1px solid #eee; margin-top: 40px;
  }
</style>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="badge">✅ Gratuito &nbsp;•&nbsp; Sem Cadastro &nbsp;•&nbsp; Resultado em 2 minutos</div>
  <h1>🎯 Sua Aposentadoria Merece um Plano de Verdade</h1>
  <p>Descubra quanto você precisa acumular, se está no caminho certo e o que fazer se não estiver.</p>
  <p style="font-size:15px; opacity:0.75; margin-top:8px;">
    Inteligência financeira acessível para todos os brasileiros
  </p>
</div>
""", unsafe_allow_html=True)

_, col_btn, _ = st.columns([1, 2, 1])
with col_btn:
    if st.button("🚀 Simular Minha Aposentadoria Grátis", key="hero_cta"):
        st.switch_page("pages/simulator.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── ESTATÍSTICAS ─────────────────────────────────────────────────────────────
st.markdown("### 📊 Por que planejar é urgente?")

stats_data = [
    ("73%",     "dos brasileiros não têm reserva suficiente para aposentadoria"),
    ("R$ 1.412","teto médio do INSS — menos do que 1 salário mínimo para a maioria"),
    ("30+ anos","de aposentadoria que você vai precisar financiar"),
    ("10×",     "mais patrimônio acumulando aos 25 vs. aos 45 anos"),
]
for col, (num, lbl) in zip(st.columns(4), stats_data):
    col.markdown(
        f'<div class="stat-card"><div class="stat-number">{num}</div>'
        f'<div class="stat-label">{lbl}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── COMO FUNCIONA ─────────────────────────────────────────────────────────────
st.markdown("### ⚙️ Como funciona em 3 passos")

steps = [
    ("1", "Informe seus dados",
     "Idade, patrimônio atual, quanto pode poupar por mês e sua estimativa de INSS."),
    ("2", "Receba sua projeção",
     "Calculamos o capital-alvo com fórmula de anuidade, projeção gráfica e análise de cenários."),
    ("3", "Ajuste e descubra",
     "Veja o impacto de aumentar os aportes e baixe seu relatório personalizado."),
]
for col, (n, title, desc) in zip(st.columns(3), steps):
    col.markdown(
        f'<div class="step-card"><div class="step-num">{n}</div>'
        f'<h4 style="color:#1e3c72;margin:10px 0 6px">{title}</h4>'
        f'<p style="color:#555;font-size:14px">{desc}</p></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── BENEFÍCIOS ────────────────────────────────────────────────────────────────
st.markdown("### ✨ O que você vai descobrir")

benefits = [
    [
        ("💰 Otimização Fiscal",
         "Entenda como PGBL e VGBL podem reduzir seu IR legalmente."),
        ("🎯 Sua Meta Real",
         "Capital-alvo ajustado por inflação e expectativa de vida."),
        ("🛡️ Status do Plano",
         "Saiba se sua poupança atual é suficiente ou há déficit."),
    ],
    [
        ("📈 Juros Compostos Visualizados",
         "Gráfico interativo mostrando o crescimento do patrimônio."),
        ("🔀 Análise de Cenários",
         "Compare o impacto de aportar +R$ 200, +R$ 500 e +R$ 1.000/mês."),
        ("📥 Relatório para Download",
         "Baixe um resumo completo da simulação para referência futura."),
    ],
]
for col, benefit_list in zip(st.columns(2), benefits):
    for title, desc in benefit_list:
        col.markdown(
            f'<div class="card"><h4>{title}</h4><p>{desc}</p></div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ── DEPOIMENTOS ───────────────────────────────────────────────────────────────
st.markdown("### 💬 Quem já planejou conta")

testimonials = [
    ("Finalmente entendi que o INSS não seria suficiente. Aumentei os aportes e hoje durmo tranquilo.",
     "Carlos M., 42 anos — Engenheiro Civil"),
    ("Descobri que com R$ 600/mês consigo me aposentar aos 60. Simples, rápido e muito revelador.",
     "Fernanda R., 34 anos — Professora"),
    ("Sempre achei que planejamento era coisa de rico. Esse simulador provou que eu estava errado.",
     "Roberto S., 51 anos — Autônomo"),
]
for col, (quote, author) in zip(st.columns(3), testimonials):
    col.markdown(
        f'<div class="testimonial"><p style="padding-top:20px">{quote}</p>'
        f'<div class="author">— {author}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ── CTA BANNER ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cta-banner">
  <h2>⏰ Cada Mês de Atraso Custa Muito Caro</h2>
  <p>Quem começa 10 anos antes acumula o dobro — mesmo com os mesmos aportes.<br>
     Não deixe para depois o que pode transformar seu futuro hoje.</p>
</div>
""", unsafe_allow_html=True)

_, col_cta2, _ = st.columns([1, 2, 1])
with col_cta2:
    if st.button("📊 Calcular Minha Aposentadoria Agora", key="mid_cta"):
        st.switch_page("pages/simulator.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── FAQ ───────────────────────────────────────────────────────────────────────
st.markdown("### ❓ Perguntas Frequentes")

faqs = [
    ("Com que idade devo começar a planejar?",
     "O quanto antes, melhor. Começar aos 25 em vez de aos 40 pode gerar 3× mais patrimônio graças aos juros compostos. "
     "Mas nunca é tarde demais — qualquer poupança agora é melhor do que nenhuma."),
    ("O INSS é suficiente para me aposentar?",
     "Na maioria dos casos, não. O teto do INSS em 2024 é de ~R$ 7.786, mas a média de benefício pago é muito menor. "
     "Uma previdência privada complementar (PGBL ou VGBL) é altamente recomendada."),
    ("PGBL ou VGBL — qual escolher?",
     "PGBL é ideal para quem faz declaração completa do IR (deduz até 12% da renda tributável). "
     "VGBL é indicado para quem usa declaração simplificada ou já atingiu o limite do PGBL. "
     "O simulador ajuda você a entender qual faz mais sentido no seu perfil."),
    ("Quanto preciso poupar por mês?",
     "Depende da sua idade, patrimônio atual, meta de aposentadoria e retorno esperado. "
     "Use o simulador para calcular seu número exato — o resultado costuma surpreender (para cima ou para baixo)."),
    ("Posso começar com pouco dinheiro?",
     "Sim! Muitos fundos aceitam aportes a partir de R$ 50–100/mês. "
     "Consistência é mais importante do que valor: aportes regulares pequenos superam aportes grandes e esporádicos."),
    ("Meus dados ficam armazenados?",
     "Não. Todos os cálculos são feitos localmente no seu navegador. "
     "Nenhum dado pessoal é enviado ou armazenado em servidores."),
]
for question, answer in faqs:
    with st.expander(f"❓ {question}"):
        st.write(answer)

st.markdown("<br>", unsafe_allow_html=True)

# ── CONTATO ───────────────────────────────────────────────────────────────────
st.markdown("### 📞 Fale com um Especialista")

col_info, col_form = st.columns([1, 1])

with col_info:
    st.markdown("""
**Atendimento Personalizado**

Nossa equipe de especialistas em previdência está pronta para ajudá-lo a traçar a estratégia ideal para o seu perfil.

📧 **E-mail:** contato@prevplan.com.br  
📱 **WhatsApp:** [(11) 99999-9999](https://wa.me/5511999999999)  
⏰ **Horário:** Segunda a Sexta, 9h–18h  

---

> ⚠️ *As informações desta plataforma têm caráter educativo e não constituem recomendação de investimento. Consulte um planejador financeiro certificado (CFP®) para orientação personalizada.*
""")

with col_form:
    with st.form("contact_form", clear_on_submit=True):
        st.markdown("**Envie uma mensagem:**")
        name    = st.text_input("Nome *", placeholder="Maria da Silva")
        email   = st.text_input("E-mail *", placeholder="maria@email.com")
        phone   = st.text_input("WhatsApp (opcional)", placeholder="(11) 9xxxx-xxxx")
        topic   = st.selectbox("Assunto", [
            "Dúvida sobre o simulador",
            "Planejamento personalizado",
            "Consultoria previdenciária",
            "Outro",
        ])
        message = st.text_area("Mensagem *", placeholder="Descreva sua dúvida...", height=100)
        if st.form_submit_button("Enviar Mensagem 📨"):
            if name and email and message:
                st.success("✅ Mensagem enviada! Responderemos em até 1 dia útil.")
            else:
                st.error("Preencha os campos obrigatórios marcados com *.")

# ── RODAPÉ ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <p>© {APP_CONFIG['year']} {APP_CONFIG['app_name']}. Todos os direitos reservados.</p>
  <p>⚠️ Simulador informativo. Não constitui recomendação de investimento ou assessoria financeira.</p>
</div>
""", unsafe_allow_html=True)
