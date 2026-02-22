import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Simulador de Aposentadoria | PrevPlan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  section[data-testid="stSidebar"] { display: none; }
  .block-container { max-width: 1100px; padding-top: 1.2rem; }
  .result-card {
    color: white; padding: 26px 16px; border-radius: 14px;
    text-align: center; margin: 6px 0;
  }
  .result-card .value { font-size: 36px; font-weight: 800; line-height: 1.1; }
  .result-card .label { font-size: 13px; opacity: 0.85; margin-top: 6px; }
  .alert-warning {
    background: #fff8e1; border-left: 4px solid #ffc107;
    padding: 16px; border-radius: 8px; margin: 10px 0;
  }
  .alert-success {
    background: #e8f5e9; border-left: 4px solid #4caf50;
    padding: 16px; border-radius: 8px; margin: 10px 0;
  }
  div[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #667eea, #764ba2) !important;
    border: none !important; color: white !important;
    font-weight: 700 !important; border-radius: 10px !important;
    width: 100% !important;
  }
</style>
""", unsafe_allow_html=True)

# ── NAVEGAÇÃO ─────────────────────────────────────────────────────────────────
if st.button("← Voltar à página inicial"):
    st.switch_page("app.py")

st.title("📊 Simulador de Aposentadoria")
st.caption("Preencha os dados abaixo para receber sua projeção — leva menos de 2 minutos.")
st.markdown("---")

# ── FORMULÁRIO ────────────────────────────────────────────────────────────────
with st.form("simulation_form"):

    st.subheader("👤 Dados Pessoais")
    c1, c2, c3 = st.columns(3)
    with c1:
        current_age = st.number_input("Idade atual", min_value=18, max_value=79, value=35)
    with c2:
        retirement_age = st.number_input("Idade para aposentar", min_value=40, max_value=99, value=65)
    with c3:
        life_expectancy = st.number_input(
            "Expectativa de vida", min_value=60, max_value=120, value=90,
            help="Use valor conservador. IBGE aponta ~80 anos; use 90 para mais segurança."
        )

    st.subheader("💵 Situação Financeira Atual")
    c4, c5, c6 = st.columns(3)
    with c4:
        current_savings = st.number_input(
            "Patrimônio atual (R$)", min_value=0.0, value=50_000.0, step=5_000.0, format="%.0f"
        )
    with c5:
        monthly_contribution = st.number_input(
            "Aporte mensal (R$)", min_value=0.0, value=1_000.0, step=100.0, format="%.0f"
        )
    with c6:
        monthly_expenses = st.number_input(
            "Despesa mensal atual (R$)", min_value=500.0, value=5_000.0, step=500.0, format="%.0f"
        )

    st.subheader("📐 Premissas Econômicas")
    c7, c8, c9 = st.columns(3)
    with c7:
        retirement_pct = st.slider("Custo de vida na aposentadoria (%)", 50, 100, 80)
    with c8:
        inflation_rate = st.number_input("Inflação anual estimada (%)", 1.0, 20.0, 4.5, step=0.1)
    with c9:
        investment_return = st.number_input("Retorno nominal anual (%)", 1.0, 30.0, 9.0, step=0.5)

    st.subheader("🏛️ INSS / Previdência Pública")
    c10, c11 = st.columns(2)
    with c10:
        has_inss = st.checkbox("Contribuo ao INSS ou regime próprio", value=True)
    with c11:
        inss_benefit = st.number_input(
            "Benefício estimado INSS (R$/mês)",
            min_value=0.0, max_value=15_000.0, value=2_500.0, step=100.0,
            disabled=not has_inss,
            help="Consulte em meu.inss.gov.br. Se não souber, use R$ 1.412 (média 2024)."
        )
    if not has_inss:
        inss_benefit = 0.0

    submitted = st.form_submit_button("🔍 Calcular Minha Simulação", type="primary")

# ── CÁLCULOS ──────────────────────────────────────────────────────────────────
if submitted:

    if retirement_age <= current_age:
        st.error("❌ A idade de aposentadoria deve ser maior que a idade atual.")
        st.stop()
    if life_expectancy <= retirement_age:
        st.error("❌ A expectativa de vida deve ser maior que a idade de aposentadoria.")
        st.stop()

    years_to_ret  = retirement_age - current_age
    years_in_ret  = life_expectancy - retirement_age
    months_to_ret = years_to_ret * 12
    months_in_ret = years_in_ret * 12

    r_annual     = investment_return / 100
    inf_annual   = inflation_rate / 100
    r_monthly    = (1 + r_annual) ** (1 / 12) - 1
    real_annual  = (1 + r_annual) / (1 + inf_annual) - 1
    real_monthly = (1 + real_annual) ** (1 / 12) - 1

    monthly_gap_today  = max(0.0, monthly_expenses * retirement_pct / 100 - inss_benefit)
    monthly_gap_at_ret = monthly_gap_today * (1 + inf_annual) ** years_to_ret

    # Capital-alvo via VP de anuidade com retorno real durante aposentadoria
    if real_monthly > 1e-9:
        target_capital = (
            monthly_gap_at_ret
            * (1 - (1 + real_monthly) ** (-months_in_ret))
            / real_monthly
        )
    else:
        target_capital = monthly_gap_at_ret * months_in_ret

    fv_savings = current_savings * (1 + r_annual) ** years_to_ret

    if r_monthly > 1e-12:
        fv_contribs = (
            monthly_contribution
            * ((1 + r_monthly) ** months_to_ret - 1)
            / r_monthly
        )
    else:
        fv_contribs = monthly_contribution * months_to_ret

    total_accumulated = fv_savings + fv_contribs
    surplus   = total_accumulated - target_capital
    on_track  = surplus >= 0

    remaining_gap = max(0.0, target_capital - fv_savings)
    if r_monthly > 1e-12 and months_to_ret > 0:
        required_monthly = remaining_gap * r_monthly / ((1 + r_monthly) ** months_to_ret - 1)
    elif months_to_ret > 0:
        required_monthly = remaining_gap / months_to_ret
    else:
        required_monthly = 0.0

    # ── EXIBIÇÃO DOS RESULTADOS ───────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📊 Resultado da Sua Simulação")

    m1, m2, m3 = st.columns(3)
    m1.markdown(
        '<div class="result-card" style="background:linear-gradient(135deg,#1e3c72,#2a5298)">'
        f'<div class="value">R$ {target_capital/1e6:.2f}M</div>'
        '<div class="label">🎯 Capital-alvo na aposentadoria</div></div>',
        unsafe_allow_html=True,
    )
    m2.markdown(
        '<div class="result-card" style="background:linear-gradient(135deg,#667eea,#764ba2)">'
        f'<div class="value">R$ {total_accumulated/1e6:.2f}M</div>'
        '<div class="label">📈 Estimativa acumulada</div></div>',
        unsafe_allow_html=True,
    )
    color3 = "#388e3c" if on_track else "#c62828"
    icon3  = "✅" if on_track else "❌"
    m3.markdown(
        f'<div class="result-card" style="background:{color3}">'
        f'<div class="value">{icon3} R$ {abs(surplus)/1e6:.2f}M</div>'
        f'<div class="label">{"Superávit" if on_track else "Déficit"} estimado</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if on_track:
        st.markdown(
            '<div class="alert-success">'
            '<h4>✅ Você está no caminho certo!</h4>'
            f'<p>Com aportes de <strong>R$ {monthly_contribution:,.0f}/mês</strong> você acumulará '
            f'<strong>R$ {total_accumulated:,.0f}</strong> — acima da meta de '
            f'<strong>R$ {target_capital:,.0f}</strong>.</p></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="alert-warning">'
            f'<h4>⚠️ Déficit projetado de R$ {abs(surplus):,.0f}</h4>'
            f'<p>Para atingir a meta, aumente o aporte para '
            f'<strong>R$ {required_monthly:,.0f}/mês</strong> '
            f'(+<strong>R$ {max(0, required_monthly - monthly_contribution):,.0f}/mês</strong>).</p>'
            '<p style="margin-top:8px">Alternativas: revisar a carteira para maior retorno, '
            'ou ajustar o custo de vida planejado na aposentadoria.</p></div>',
            unsafe_allow_html=True,
        )

    # Métricas
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Detalhes da Projeção")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Anos até aposentar",       f"{years_to_ret} anos")
    d2.metric("Duração da aposentadoria", f"{years_in_ret} anos")
    d3.metric("Gap mensal hoje",          f"R$ {monthly_gap_today:,.0f}")
    d4.metric("Gap mensal na aposentad.", f"R$ {monthly_gap_at_ret:,.0f}")

    # ── GRÁFICO ───────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📉 Projeção de Crescimento Patrimonial")

    ages = list(range(current_age, retirement_age + 1))
    acc, pure = [], []
    for age in ages:
        y = age - current_age
        m = y * 12
        fv_s = current_savings * (1 + r_annual) ** y
        fv_c = (
            monthly_contribution * ((1 + r_monthly) ** m - 1) / r_monthly
            if r_monthly > 1e-12 else monthly_contribution * m
        )
        acc.append(fv_s + fv_c)
        pure.append(current_savings + monthly_contribution * m)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ages, y=acc,
        mode="lines", name="Com rendimentos",
        line=dict(color="#667eea", width=3),
        fill="tozeroy", fillcolor="rgba(102,126,234,0.12)",
        hovertemplate="Idade %{x}: R$ %{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=ages, y=pure,
        mode="lines", name="Só aportes (sem rendimentos)",
        line=dict(color="#bbb", width=2, dash="dot"),
        hovertemplate="Idade %{x}: R$ %{y:,.0f}<extra></extra>",
    ))
    fig.add_hline(
        y=target_capital,
        line_color="#e53935", line_dash="dash", line_width=2,
        annotation_text=f"🎯 Meta: R$ {target_capital/1e6:.2f}M",
        annotation_position="top left",
        annotation_font_color="#e53935",
    )
    fig.update_layout(
        xaxis_title="Idade",
        yaxis_title="Patrimônio (R$)",
        yaxis=dict(tickformat=",.0f"),
        hovermode="x unified",
        legend=dict(orientation="h", y=1.06, x=0),
        height=420,
        margin=dict(l=20, r=20, t=60, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(showgrid=True, gridcolor="#f0f0f0")
    fig.update_yaxes(showgrid=True, gridcolor="#f0f0f0")
    st.plotly_chart(fig, use_container_width=True)

    # ── ANÁLISE DE CENÁRIOS ───────────────────────────────────────────────────
    st.subheader("🔀 Análise de Cenários — Impacto de Aportar Mais")

    scenarios = []
    for label, extra in [("Aporte atual (base)", 0), ("+R$ 200/mês", 200),
                          ("+R$ 500/mês", 500), ("+R$ 1.000/mês", 1_000)]:
        contrib = monthly_contribution + extra
        fv_c_s  = (
            contrib * ((1 + r_monthly) ** months_to_ret - 1) / r_monthly
            if r_monthly > 1e-12 else contrib * months_to_ret
        )
        total_s = fv_savings + fv_c_s
        diff    = total_s - target_capital
        scenarios.append({
            "Cenário":            label,
            "Aporte Mensal":      f"R$ {contrib:,.0f}",
            "Acumulado Estimado": f"R$ {total_s:,.0f}",
            "vs. Meta":           f"{'✅ +' if diff >= 0 else '❌ '}R$ {abs(diff):,.0f}",
        })
    st.dataframe(pd.DataFrame(scenarios), use_container_width=True, hide_index=True)

    # ── RECOMENDAÇÕES ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 Recomendações Personalizadas")

    recs = []
    if on_track:
        recs.append(("✅ Manter a disciplina",
            "Você está no caminho certo! Revise anualmente e após grandes mudanças de vida."))
    else:
        recs.append(("🔴 Aumentar aportes mensais",
            f"Você precisaria de **R$ {required_monthly:,.0f}/mês** para atingir a meta. "
            "Mesmo aumentos graduais de R$ 100–200/mês fazem diferença significativa."))
    if investment_return < 7.0:
        recs.append(("📈 Revisar a carteira",
            "Retorno abaixo de 7% a.a. pode estar muito conservador. "
            "Tesouro IPCA+, fundos multimercado e ETFs podem elevar o retorno."))
    if inss_benefit < monthly_expenses * retirement_pct / 100 * 0.5:
        recs.append(("🏛️ Previdência privada complementar",
            "O INSS cobre menos de 50% das suas despesas projetadas. "
            "PGBL (declaração completa) ou VGBL complementam de forma eficiente."))
    if years_to_ret > 25:
        recs.append(("⏳ O tempo é seu maior aliado",
            f"Com {years_to_ret} anos pela frente, pequenos ajustes agora evitam "
            "grandes esforços no futuro graças aos juros compostos."))
    for title, body in recs:
        st.info(f"**{title}**: {body}")

    # ── DOWNLOAD DO RELATÓRIO ─────────────────────────────────────────────────
    st.markdown("---")
    st.subheader("📥 Baixar Relatório Completo")

    status_txt = "SUPERÁVIT — NO CAMINHO CERTO" if on_track else "DÉFICIT — AÇÃO NECESSÁRIA"
    lines = [
        "=" * 58,
        "    RELATÓRIO DE SIMULAÇÃO DE APOSENTADORIA — PrevPlan",
        "=" * 58,
        f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        "",
        "DADOS PESSOAIS",
        "-" * 42,
        f"  Idade atual:               {current_age} anos",
        f"  Aposentadoria planejada:   {retirement_age} anos",
        f"  Expectativa de vida:       {life_expectancy} anos",
        f"  Anos até aposentar:        {years_to_ret} anos",
        f"  Anos em aposentadoria:     {years_in_ret} anos",
        "",
        "SITUAÇÃO FINANCEIRA",
        "-" * 42,
        f"  Patrimônio atual:          R$ {current_savings:,.2f}",
        f"  Aporte mensal:             R$ {monthly_contribution:,.2f}",
        f"  Despesa mensal atual:      R$ {monthly_expenses:,.2f}",
        f"  Benefício INSS estimado:   R$ {inss_benefit:,.2f}/mês",
        "",
        "PREMISSAS ECONÔMICAS",
        "-" * 42,
        f"  Inflação anual:            {inflation_rate:.1f}%",
        f"  Retorno nominal anual:     {investment_return:.1f}%",
        f"  Retorno real anual:        {real_annual*100:.2f}%",
        f"  Custo vida na aposentad.:  {retirement_pct}% do atual",
        "",
        "RESULTADOS",
        "-" * 42,
        f"  Capital-alvo:              R$ {target_capital:,.2f}",
        f"  Estimativa acumulada:      R$ {total_accumulated:,.2f}",
        f"  {'Superávit' if on_track else 'Déficit'}:                  R$ {abs(surplus):,.2f}",
        f"  Status:                    {status_txt}",
    ]
    if not on_track:
        lines += [
            "",
            f"  Aporte atual:              R$ {monthly_contribution:,.2f}/mês",
            f"  Aporte necessário:         R$ {required_monthly:,.2f}/mês",
            f"  Aumento necessário:        R$ {max(0,required_monthly-monthly_contribution):,.2f}/mês",
        ]
    lines += [
        "",
        "=" * 58,
        "  AVISO: Este relatório é informativo e não constitui",
        "  recomendação de investimento. Consulte um CFP(R).",
        "=" * 58,
    ]

    st.download_button(
        label="📥 Baixar Relatório (.txt)",
        data="\n".join(lines),
        file_name=f"simulacao_prevplan_{datetime.now().strftime('%d%m%Y_%H%M')}.txt",
        mime="text/plain",
        type="primary",
    )

    st.info(
        "📞 Quer uma análise personalizada? Fale com nossos especialistas via "
        "[WhatsApp](https://wa.me/5511999999999) ou volte à página inicial "
        "para preencher o formulário de contato."
    )
