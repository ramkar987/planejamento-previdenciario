# Escreva o seu código aqui :-)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="Simulador de Aposentadoria",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 25px;
        border-radius: 10px;
        margin: 15px 0;
        text-align: center;
    }
    .result-number {
        font-size: 36px;
        font-weight: bold;
        margin: 10px 0;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Simulador de Aposentadoria")
st.write("Preencha os dados abaixo para calcular sua necessidade de poupança para aposentadoria")

# Create tabs for input and results
input_tab, results_tab = st.tabs(["📝 Dados Pessoais", "📈 Resultados"])

with input_tab:
    st.subheader("Informações Pessoais")

    col1, col2 = st.columns(2)

    with col1:
        current_age = st.number_input("Sua idade atual", min_value=18, max_value=80, value=35)
        retirement_age = st.number_input("Idade desejada para aposentar", min_value=current_age+1, max_value=100, value=65)
        life_expectancy = st.number_input("Expectativa de vida", min_value=retirement_age+1, max_value=120, value=90)

    with col2:
        current_salary = st.number_input("Renda mensal atual (R$)", min_value=0.0, value=5000.0, step=100.0)
        current_savings = st.number_input("Patrimônio atual (R$)", min_value=0.0, value=50000.0, step=1000.0)
        monthly_contribution = st.number_input("Quanto pode poupar por mês (R$)", min_value=0.0, value=1000.0, step=100.0)

    st.subheader("Despesas e Metas")

    col1, col2 = st.columns(2)

    with col1:
        monthly_expenses = st.number_input("Despesa mensal atual (R$)", min_value=0.0, value=3000.0, step=100.0)
        retirement_expenses_percent = st.slider("Despesa na aposentadoria (% da atual)", min_value=50, max_value=100, value=80)

    with col2:
        inflation_rate = st.number_input("Taxa de inflação anual (%)", min_value=0.0, max_value=20.0, value=4.5, step=0.1)
        investment_return = st.number_input("Retorno anual esperado (%)", min_value=0.0, max_value=30.0, value=8.0, step=0.1)

    st.subheader("Benefícios Públicos")

    col1, col2 = st.columns(2)

    with col1:
        has_public_pension = st.checkbox("Contribui ao INSS", value=True)
        if has_public_pension:
            estimated_pension = st.number_input("Estimativa de aposentadoria INSS (R$)", min_value=0.0, value=2000.0, step=100.0)
        else:
            estimated_pension = 0.0

    with col2:
        contribution_years = st.number_input("Anos de contribuição ao INSS", min_value=0, max_value=50, value=15)

    if st.button("🔍 Calcular Simulação", key="calculate"):
        st.session_state.simulation_data = {
            'current_age': current_age,
            'retirement_age': retirement_age,
            'life_expectancy': life_expectancy,
            'current_salary': current_salary,
            'current_savings': current_savings,
            'monthly_contribution': monthly_contribution,
            'monthly_expenses': monthly_expenses,
            'retirement_expenses_percent': retirement_expenses_percent,
            'inflation_rate': inflation_rate / 100,
            'investment_return': investment_return / 100,
            'estimated_pension': estimated_pension,
            'contribution_years': contribution_years
        }
        st.success("Simulação calculada! Veja os resultados na aba 'Resultados'")

with results_tab:
    if 'simulation_data' in st.session_state:
        data = st.session_state.simulation_data

        # Calculations
        years_to_retirement = data['retirement_age'] - data['current_age']
        years_in_retirement = data['life_expectancy'] - data['retirement_age']

        monthly_retirement_expenses = (data['monthly_expenses'] * data['retirement_expenses_percent'] / 100)
        adjusted_retirement_expenses = monthly_retirement_expenses * ((1 + data['inflation_rate']) ** years_to_retirement)

        total_retirement_need = adjusted_retirement_expenses * 12 * years_in_retirement
        pension_income = data['estimated_pension'] * 12 * years_in_retirement
        gap = total_retirement_need - pension_income

        # Future value of current savings
        fv_current_savings = data['current_savings'] * ((1 + data['investment_return']) ** years_to_retirement)

        # Future value of monthly contributions
        monthly_return = (1 + data['investment_return']) ** (1/12)
        fv_contributions = data['monthly_contribution'] * (((monthly_return ** (years_to_retirement * 12)) - 1) / (monthly_return - 1))

        total_accumulated = fv_current_savings + fv_contributions

        # Display Results
        st.subheader("📊 Resultado da Simulação")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="result-box">
                <p>Necessidade Total para Aposentadoria</p>
                <div class="result-number">R$ {gap:,.0f}</div>
                <p style="font-size: 14px;">Valor necessário além do INSS</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="result-box">
                <p>Acumulado Estimado</p>
                <div class="result-number">R$ {total_accumulated:,.0f}</div>
                <p style="font-size: 14px;">Com suas contribuições atuais</p>
            </div>
            """, unsafe_allow_html=True)

        # Analysis
        st.subheader("📈 Análise Detalhada")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Anos até aposentadoria", years_to_retirement)

        with col2:
            st.metric("Anos em aposentadoria", years_in_retirement)

        with col3:
            st.metric("Despesa mensal na aposentadoria", f"R$ {adjusted_retirement_expenses:,.0f}")

        # Status
        st.markdown("---")

        if total_accumulated >= gap:
            st.markdown("""
            <div class="success-box">
                <h4>✅ Excelente! Você está no caminho certo!</h4>
                <p>Com suas contribuições atuais, você conseguirá acumular o valor necessário para sua aposentadoria.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            deficit = gap - total_accumulated
            monthly_needed = deficit / (years_to_retirement * 12)
            current_plus_needed = data['monthly_contribution'] + monthly_needed

            st.markdown(f"""
            <div class="warning-box">
                <h4>⚠️ Atenção: Há um déficit em sua poupança</h4>
                <p>Você precisa aumentar sua contribuição mensal de <strong>R$ {data['monthly_contribution']:,.0f}</strong> para <strong>R$ {current_plus_needed:,.0f}</strong></p>
                <p>Isso representa um aumento de <strong>R$ {monthly_needed:,.0f}</strong> por mês</p>
            </div>
            """, unsafe_allow_html=True)

        # Breakdown Table
        st.subheader("📋 Detalhamento Financeiro")

        breakdown_data = {
            'Descrição': [
                'Patrimônio Atual',
                'Valor Futuro do Patrimônio',
                'Contribuições Mensais',
                'Valor Futuro das Contribuições',
                'Total Acumulado',
                '',
                'Necessidade Total',
                'Renda do INSS',
                'Déficit/Superávit'
            ],
            'Valor (R$)': [
                f"{data['current_savings']:,.0f}",
                f"{fv_current_savings:,.0f}",
                f"{data['monthly_contribution']:,.0f}",
                f"{fv_contributions:,.0f}",
                f"{total_accumulated:,.0f}",
                '',
                f"{gap:,.0f}",
                f"{pension_income:,.0f}",
                f"{total_accumulated - gap:,.0f}"
            ]
        }

        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

        # Chart
        st.subheader("📉 Projeção de Crescimento")

        years = np.arange(0, years_to_retirement + 1)
        accumulated_values = []

        for year in years:
            months = year * 12
            fv_savings = data['current_savings'] * ((1 + data['investment_return']) ** year)
            fv_contrib = data['monthly_contribution'] * (((monthly_return ** months) - 1) / (monthly_return - 1))
            accumulated_values.append(fv_savings + fv_contrib)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(years + data['current_age'], accumulated_values, linewidth=3, color='#667eea', label='Acumulado')
        ax.axhline(y=gap, color='#ff6b6b', linestyle='--', linewidth=2, label='Meta Necessária')
        ax.fill_between(years + data['current_age'], 0, accumulated_values, alpha=0.3, color='#667eea')

        ax.set_xlabel('Idade', fontsize=12)
        ax.set_ylabel('Valor Acumulado (R$)', fontsize=12)
        ax.set_title('Projeção de Crescimento Patrimonial', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1e6:.1f}M' if x >= 1e6 else f'R$ {x/1e3:.0f}K'))

        st.pyplot(fig)

        # Recommendations
        st.subheader("💡 Recomendações")

        recommendations = []

        if total_accumulated < gap:
            recommendations.append("🔴 **Aumentar contribuições**: Você precisa aumentar a poupança mensal para atingir sua meta")
        else:
            recommendations.append("🟢 **Manter contribuições**: Continue com o plano atual, você está no caminho certo")

        if data['investment_return'] < 0.06:
            recommendations.append("📈 **Revisar investimentos**: Considere investimentos com melhor rentabilidade")

        if data['monthly_contribution'] == 0:
            recommendations.append("⚠️ **Iniciar poupança**: Comece a poupar o quanto antes para aproveitar o tempo")

        if years_to_retirement > 30:
            recommendations.append("💪 **Aproveite o tempo**: Você tem bastante tempo para acumular, mantenha a disciplina")

        for rec in recommendations:
            st.info(rec)

        # Download Report
        st.markdown("---")

        report = f"""
RELATÓRIO DE SIMULAÇÃO DE APOSENTADORIA
{'='*50}

DADOS PESSOAIS:
- Idade Atual: {data['current_age']} anos
- Idade para Aposentar: {data['retirement_age']} anos
- Expectativa de Vida: {data['life_expectancy']} anos
- Anos até Aposentadoria: {years_to_retirement} anos
- Anos em Aposentadoria: {years_in_retirement} anos

SITUAÇÃO FINANCEIRA:
- Renda Mensal: R$ {data['current_salary']:,.2f}
- Patrimônio Atual: R$ {data['current_savings']:,.2f}
- Contribuição Mensal: R$ {data['monthly_contribution']:,.2f}
- Despesa Mensal: R$ {data['monthly_expenses']:,.2f}

PREMISSAS:
- Taxa de Inflação Anual: {data['inflation_rate']*100:.1f}%
- Retorno Esperado: {data['investment_return']*100:.1f}%
- Despesa na Aposentadoria: {data['retirement_expenses_percent']}% da atual

RESULTADOS:
- Despesa Mensal na Aposentadoria: R$ {adjusted_retirement_expenses:,.2f}
- Necessidade Total: R$ {gap:,.2f}
- Renda do INSS: R$ {pension_income:,.2f}
- Acumulado Estimado: R$ {total_accumulated:,.2f}
- Diferença: R$ {total_accumulated - gap:,.2f}

STATUS: {'✅ SUPERÁVIT' if total_accumulated >= gap else '❌ DÉFICIT'}

Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
"""

        st.download_button(
            label="📥 Baixar Relatório",
            data=report,
            file_name=f"relatorio_aposentadoria_{datetime.now().strftime('%d%m%Y')}.txt",
            mime="text/plain"
        )
    else:
        st.info("👈 Preencha os dados na aba 'Dados Pessoais' e clique em 'Calcular Simulação'")
