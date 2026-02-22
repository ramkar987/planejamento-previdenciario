import streamlit as st
import pandas as pd
from datetime import datetime
import json

st.set_page_config(
    page_title="Planejamento Previdenciário - Seu Futuro Seguro",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #333;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 16px;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: transform 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
    }
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 60px 20px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 40px;
    }
    .feature-card {
        background: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin: 15px 0;
    }
    .benefit-item {
        background: #f8f9fa;
        padding: 20px;
        border-left: 4px solid #667eea;
        margin: 15px 0;
        border-radius: 5px;
    }
    .cta-section {
        background: #667eea;
        color: white;
        padding: 40px;
        border-radius: 10px;
        text-align: center;
        margin: 40px 0;
    }
    .stat-box {
        background: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 32px;
        font-weight: bold;
        color: #667eea;
    }
    .stat-label {
        color: #666;
        font-size: 14px;
        margin-top: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 style="font-size: 48px; margin-bottom: 20px;">🎯 Seu Futuro Financeiro Começa Agora</h1>
    <p style="font-size: 20px; margin-bottom: 30px;">Planejamento Previdenciário Inteligente para uma Aposentadoria Tranquila</p>
    <p style="font-size: 16px; opacity: 0.9;">Descubra quanto você precisa poupar e como otimizar sua estratégia de investimentos</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Início", "📊 Simulador", "❓ FAQ", "📞 Contato"])

with tab1:
    st.markdown("---")

    # Statistics Section
    st.subheader("📈 Por Que Planejar Sua Aposentadoria?")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">73%</div>
            <div class="stat-label">Brasileiros sem planejamento</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">2.1x</div>
            <div class="stat-label">Mais segurança financeira</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">R$ 1.2M</div>
            <div class="stat-label">Diferença média acumulada</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">30+</div>
            <div class="stat-label">Anos de aposentadoria</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Benefits Section
    st.subheader("✨ Benefícios do Planejamento Previdenciário")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="benefit-item">
            <h4>💰 Otimização Fiscal</h4>
            <p>Reduza impostos legalmente e maximize seus ganhos com investimentos.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="benefit-item">
            <h4>🎯 Meta Clara</h4>
            <p>Saiba exatamente quanto precisa poupar para sua aposentadoria.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="benefit-item">
            <h4>🛡️ Segurança</h4>
            <p>Proteja seu futuro com uma estratégia diversificada e robusta.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="benefit-item">
            <h4>📱 Acompanhamento</h4>
            <p>Monitore seu progresso em tempo real com relatórios personalizados.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="benefit-item">
            <h4>🚀 Crescimento</h4>
            <p>Potencialize seus investimentos com estratégias comprovadas.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="benefit-item">
            <h4>👨‍💼 Especialistas</h4>
            <p>Acesso a consultores experientes em planejamento financeiro.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # CTA Section
    st.markdown("""
    <div class="cta-section">
        <h2>Comece Seu Planejamento Hoje</h2>
        <p style="margin: 20px 0; font-size: 18px;">Clique no botão abaixo para acessar o simulador e descobrir sua situação previdenciária</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Acessar Simulador Agora", key="cta_home"):
            st.session_state.page = "simulator"
            st.switch_page("pages/simulator.py")

with tab2:
    st.subheader("📊 Simulador de Aposentadoria")
    st.info("Clique em 'Acessar Simulador Agora' na aba Início para começar sua análise personalizada.")

with tab3:
    st.subheader("❓ Perguntas Frequentes")

    with st.expander("Como funciona o planejamento previdenciário?"):
        st.write("""
        O planejamento previdenciário é um processo que envolve:
        1. Análise de sua situação atual (idade, renda, patrimônio)
        2. Definição de metas de aposentadoria
        3. Cálculo do valor necessário para aposentar-se
        4. Criação de estratégia de investimentos
        5. Acompanhamento periódico
        """)

    with st.expander("Qual é a idade ideal para começar?"):
        st.write("Quanto mais cedo melhor! O tempo é seu maior aliado. Começar aos 25 anos faz uma diferença enorme comparado a começar aos 40.")

    with st.expander("Quanto preciso poupar por mês?"):
        st.write("Isso depende de vários fatores: sua idade, renda, despesas, meta de aposentadoria. Use nosso simulador para descobrir!")

    with st.expander("Quais são as melhores opções de investimento?"):
        st.write("""
        Existem várias opções:
        - PGBL e VGBL (previdência privada)
        - Fundos de investimento
        - Ações
        - Imóveis
        - Renda fixa

        A melhor estratégia é diversificada e personalizada para seu perfil.
        """)

    with st.expander("Posso começar com pouco dinheiro?"):
        st.write("Sim! Muitos planos aceitam contribuições a partir de R$ 50-100 por mês. O importante é começar.")

with tab4:
    st.subheader("📞 Entre em Contato")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Informações de Contato:**

        📧 Email: contato@planejamentoprevidenciario.com.br

        📱 WhatsApp: (11) 99999-9999

        🏢 Endereço: São Paulo, SP

        ⏰ Horário: Seg-Sex, 9h-18h
        """)

    with col2:
        st.markdown("**Envie uma Mensagem:**")
        name = st.text_input("Seu Nome")
        email = st.text_input("Seu Email")
        message = st.text_area("Sua Mensagem")

        if st.button("Enviar Mensagem"):
            if name and email and message:
                st.success("Mensagem enviada com sucesso! Entraremos em contato em breve.")
            else:
                st.error("Por favor, preencha todos os campos.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>© 2024 Planejamento Previdenciário. Todos os direitos reservados.</p>
    <p style="font-size: 12px; margin-top: 10px;">Aviso: Este simulador é apenas informativo. Consulte um especialista para recomendações personalizadas.</p>
</div>
""", unsafe_allow_html=True)# Escreva o seu código aqui :-)
