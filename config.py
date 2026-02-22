from datetime import datetime

APP_CONFIG = {
    "app_name":    "PrevPlan | Planejamento Previdenciário",
    "description": "Simulador inteligente para aposentadoria",
    "version":     "1.0.0",
    "email":       "contato@prevplan.com.br",
    "whatsapp":    "5511999999999",
    "year":        datetime.now().year,   # ← chave ausente que causava KeyError
}

DEFAULT_VALUES = {
    "current_age":          35,
    "retirement_age":       65,
    "life_expectancy":      90,
    "current_salary":       5_000,
    "current_savings":      50_000,
    "monthly_contribution": 1_000,
    "monthly_expenses":     5_000,
    "inflation_rate":       4.5,
    "investment_return":    9.0,
}

COLORS = {
    "primary":   "#667eea",
    "secondary": "#764ba2",
    "dark":      "#1e3c72",
    "success":   "#4caf50",
    "warning":   "#ffc107",
    "danger":    "#c62828",
}
