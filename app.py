import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import base64

from circuit_view import render_circuit

st.set_page_config(page_title="Simulador AL 2.1", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS ---
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-card h3 {
        margin-top: 0;
        font-size: 1.2rem;
        color: #31333F;
    }
    .metric-card p {
        font-size: 2rem;
        font-weight: bold;
        color: #0068c9;
        margin-bottom: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'data' not in st.session_state:
    st.session_state.data = []

# --- Sidebar Controls ---
with st.sidebar:
    st.header("🎛️ Controlos")
    
    st.subheader("Bateria Oculta")
    with st.expander("Configurar Pilha (Professor)", expanded=False):
        true_emf = st.slider("Força Eletromotriz (ε) [V]", 1.0, 12.0, 9.0, 0.1, help="Valor real da f.e.m. da pilha.")
        true_r = st.slider("Resistência Interna (r) [Ω]", 0.1, 10.0, 2.0, 0.1, help="Valor real da resistência interna da pilha.")
    
    st.markdown("---")
    st.subheader("Circuito Externo")
    r_ext = st.slider("Resistência Externa (R) [Ω]", 0.0, 50.0, 10.0, 0.5, help="Resistência do reóstato no circuito.")
    
    # Calculate current values based on physics (Non-linear model at high currents)
    # Polarization overpotential: U = ε - r*I - c*I^2
    # External circuit: U = R*I
    # Equating both: c*I^2 + (R + r)*I - ε = 0
    c_polarization = 0.15 # empirical polarization factor
    
    # Quadratic formula: I = (-b + sqrt(b^2 - 4ac)) / 2a
    a = c_polarization
    b = r_ext + true_r
    c = -true_emf
    current_I = (-b + np.sqrt(b**2 - 4*a*c)) / (2*a)
    
    # U = R * I
    current_U = r_ext * current_I
    # P = U * I
    current_P = current_U * current_I
    
    st.markdown("---")
    if st.button("📝 Registar Dados", type="primary", width="stretch"):
        # Add a tiny bit of random noise to simulate real measurements
        # We will round to 2-3 decimal places like a real multimeter
        measured_I = round(current_I + np.random.normal(0, 0.005), 3)
        measured_U = round(current_U + np.random.normal(0, 0.02), 2)
        measured_P = round(measured_U * measured_I, 3)
        
        # Ensure positive values
        measured_I = max(0.001, measured_I)
        measured_U = max(0.001, measured_U)
        
        st.session_state.data.append({
            "R (Ω)": r_ext,
            "I (A)": measured_I,
            "U (V)": measured_U,
            "P (W)": measured_P
        })
        
    if st.button("🗑️ Limpar Dados", width="stretch"):
        st.session_state.data = []
        st.rerun()

# --- Main Area ---
st.title("🔋 AL 2.1 - Características de uma Pilha")
st.markdown("Simulador virtual para determinar a força eletromotriz e a resistência interna de uma pilha, explorando as aprendizagens essenciais de Física e Química A (10º ano).")

# Circuit Animation & Live Readings
html_circuit = render_circuit(current_I, current_U, current_P, r_ext)
html_b64 = base64.b64encode(html_circuit.encode()).decode()
st.iframe(src=f"data:text/html;charset=utf-8;base64,{html_b64}", height=470)

st.markdown("---")

df = pd.DataFrame(st.session_state.data)

tab1, tab2, tab3 = st.tabs(["📊 Gráfico U(I) e Regressão", "📈 Gráfico P(R)", "📋 Tabela de Dados"])

with tab3:
    st.subheader("Dados Experimentais Registados")
    if not df.empty:
        st.dataframe(df, width="stretch", hide_index=True)
    else:
        st.info("Varie a resistência no reóstato (painel lateral) e clique em 'Registar Dados' para começar a recolher valores.")

with tab1:
    st.subheader("Curva Característica da Pilha: U = f(I)")
    if len(df) >= 2:
        # Scatter plot
        fig_u = px.scatter(df, x="I (A)", y="U (V)", title="Tensão em função da Corrente", 
                           template="plotly_white", size_max=10)
        fig_u.update_traces(marker=dict(size=10, color="#FF4B4B", line=dict(width=2, color="DarkSlateGrey")))
        
        # Linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(df["I (A)"], df["U (V)"])
        
        # Line of best fit
        line_x = np.array([0, max(df["I (A)"]) * 1.2])
        line_y = intercept + slope * line_x
        fig_u.add_trace(go.Scatter(x=line_x, y=line_y, mode='lines', name='Ajuste Linear', line=dict(color='blue', dash='dash')))
        
        fig_u.update_layout(xaxis_title="Corrente, I / A", yaxis_title="Tensão, U / V", 
                            xaxis=dict(range=[0, max(df["I (A)"])*1.2]), yaxis=dict(range=[0, max(df["U (V)"])*1.2]))
        st.plotly_chart(fig_u, width="stretch")
        
        st.success(f"**Equação da reta de ajuste:** $U = {slope:.3f}I + {intercept:.3f}$")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.info(f"**Força Eletromotriz Experimental (ε):** {intercept:.2f} V")
        with col_res2:
            st.info(f"**Resistência Interna Experimental (r):** {-slope:.2f} Ω")
            
    elif len(df) == 1:
        st.warning("Registe pelo menos 2 pontos para realizar o ajuste linear.")
    else:
        st.info("Aguardando dados...")

with tab2:
    st.subheader("Curva de Potência: P = f(R)")
    st.markdown("A potência útil transferida para o circuito é máxima quando a resistência externa é semelhante à resistência interna da pilha ($R \\approx r$).")
    
    if len(df) > 0:
        fig_p = px.scatter(df, x="R (Ω)", y="P (W)", title="Potência Útil em função da Resistência Externa",
                           template="plotly_white")
        fig_p.update_traces(marker=dict(size=10, color="#0068c9", line=dict(width=2, color="DarkSlateGrey")))
        
        # Theoretical curve overlay
        if len(df) >= 2:
            try:
                # Use experimental values if available
                slope, intercept, _, _, _ = stats.linregress(df["I (A)"], df["U (V)"])
                exp_emf = intercept
                exp_r = -slope
                
                # generate R values
                r_vals = np.linspace(0.1, max(20.0, max(df["R (Ω)"]) * 1.2), 100)
                p_vals = (exp_emf**2 * r_vals) / ((r_vals + exp_r)**2)
                
                fig_p.add_trace(go.Scatter(x=r_vals, y=p_vals, mode='lines', name='Curva Teórica (Ajuste)', line=dict(color='orange', dash='dot')))
            except:
                pass
                
        fig_p.update_layout(xaxis_title="Resistência Externa, R / Ω", yaxis_title="Potência Útil, P / W")
        st.plotly_chart(fig_p, width="stretch")
    else:
         st.info("Aguardando dados...")
