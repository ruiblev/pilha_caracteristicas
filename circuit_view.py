def render_circuit(current_I, current_U, current_P, r_ext, max_r=50.0):
    # A velocidade da animação é inversamente proporcional à corrente.
    # Corrente máxima (R=0, r=0.1, ε=12) seria 120A, mas o uso normal (R=5) é ~2A.
    if current_I > 0.01:
        anim_duration = max(0.2, 3.0 / current_I) # limite mínimo de 0.2s para não ficar frenético demais
    else:
        anim_duration = 0 # Pausado

    # Posição do slider do reóstato
    r_percentage = (r_ext / max_r) * 100

    html_code = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;600&display=swap');
            
            body {{
                margin: 0;
                padding: 0;
                background: transparent;
            }}
            .circuit-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
                border-radius: 15px;
                padding: 20px;
                box-shadow: inset 0 0 20px rgba(0,0,0,0.5), 0 10px 30px rgba(0,0,0,0.3);
                font-family: 'Inter', sans-serif;
                color: white;
                position: relative;
                width: 100%;
                height: 450px;
                box-sizing: border-box;
            }}
            .svg-circuit {{
                width: 100%;
                max-width: 800px;
                height: 100%;
                filter: drop-shadow(0 0 10px rgba(0,0,0,0.5));
            }}
            
            /* Wires */
            .wire {{
                fill: none;
                stroke: #5a6b8c;
                stroke-width: 8;
                stroke-linecap: round;
                stroke-linejoin: round;
            }}
            
            .wire-glow {{
                fill: none;
                stroke: rgba(114, 137, 218, 0.3);
                stroke-width: 16;
                stroke-linecap: round;
                stroke-linejoin: round;
            }}
            
            /* Flowing Electrons */
            .electrons {{
                fill: none;
                stroke: #00e5ff;
                stroke-width: 4;
                stroke-dasharray: 0 25;
                stroke-linecap: round;
                animation: flow {anim_duration}s linear infinite;
                filter: drop-shadow(0 0 5px #00e5ff);
            }}
            
            @keyframes flow {{
                from {{ stroke-dashoffset: 50; }}
                to {{ stroke-dashoffset: 0; }}
            }}
            
            .paused {{
                animation-play-state: paused;
                opacity: 0.3;
            }}

            /* Components */
            .component-box {{
                fill: #23272a;
                stroke: #7289da;
                stroke-width: 3;
                rx: 15;
                ry: 15;
            }}
            
            .meter-box {{
                fill: #18191c;
                stroke: #4f545c;
                stroke-width: 4;
            }}
            
            .text-label {{
                font-size: 14px;
                fill: #b9bbbe;
                font-weight: 600;
                text-anchor: middle;
            }}
            
            .text-value {{
                font-size: 26px;
                font-family: 'Orbitron', sans-serif;
                font-weight: 700;
                text-anchor: middle;
                letter-spacing: 2px;
            }}
            
            .text-unit {{
                font-size: 14px;
                font-family: 'Orbitron', sans-serif;
                fill: #7289da;
            }}
            
            /* Battery specific */
            .battery-body {{ fill: #2c2f33; stroke: #99aab5; stroke-width: 2; rx: 5; ry: 5; }}
            .battery-pos {{ fill: #f04747; }}
            .battery-neg {{ fill: #1e1e2f; }}
        </style>
    </head>
    <body>
        <div class="circuit-container">
            <svg class="svg-circuit" viewBox="0 0 800 400">
                <defs>
                    <linearGradient id="meterGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#2f3136" />
                        <stop offset="100%" stop-color="#202225" />
                    </linearGradient>
                    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" stop-color="rgba(0, 229, 255, 0.4)" />
                        <stop offset="100%" stop-color="rgba(0, 229, 255, 0)" />
                    </radialGradient>
                </defs>

                <!-- Glow background for power -->
                <circle cx="400" cy="220" r="100" fill="url(#glow)" />

                <!-- Wires Glow -->
                <path class="wire-glow" d="M 200 150 L 200 80 L 600 80 L 600 320 L 200 320 L 200 250" />
                <path class="wire-glow" d="M 200 120 L 100 120 L 100 280 L 200 280" />
                
                <!-- Main Circuit Wires -->
                <path class="wire" d="M 200 150 L 200 80 L 600 80 L 600 320 L 200 320 L 200 250" />
                <path class="wire" d="M 200 120 L 100 120 L 100 280 L 200 280" />
                
                <!-- Animated Electrons (Moving from Battery Negative to Positive through the external circuit) -->
                <!-- Direction: Bottom of battery is negative. Electrons move down, right, up, left, back to positive. -->
                <path class="electrons {'paused' if anim_duration == 0 else ''}" d="M 200 250 L 200 320 L 600 320 L 600 80 L 200 80 L 200 150" />
                
                <!-- Battery Schematic (Real Pilha) -->
                <rect x="130" y="140" width="120" height="120" fill="rgba(44, 47, 51, 0.5)" stroke="#99aab5" stroke-width="2" stroke-dasharray="8 8" rx="10" />
                <text x="190" y="130" class="text-label" fill="#99aab5">Pilha Real</text>
                
                <!-- Internal connections -->
                <line x1="200" y1="150" x2="200" y2="160" class="wire" />
                <line x1="200" y1="180" x2="200" y2="210" class="wire" />
                <line x1="200" y1="250" x2="200" y2="250" class="wire" /> <!-- to close the gap visually -->
                
                <!-- EMF Source (ε) -->
                <text x="160" y="175" class="text-label" font-size="16" fill="#fff">ε</text>
                <line x1="180" y1="160" x2="220" y2="160" stroke="#f04747" stroke-width="4" stroke-linecap="round" /> <!-- Positive -->
                <line x1="190" y1="175" x2="210" y2="175" stroke="#fff" stroke-width="8" stroke-linecap="round" /> <!-- Negative -->
                <text x="235" y="175" class="text-label" font-size="20">+</text>
                
                <!-- Internal Resistor (r) -->
                <text x="235" y="235" class="text-label" font-size="16" fill="#fff">r</text>
                <rect x="185" y="210" width="30" height="40" fill="none" stroke="#fff" stroke-width="3" rx="2" />
                
                <!-- Ammeter (Realistic Digital Multimeter) -->
                <rect x="340" y="40" width="120" height="80" rx="10" ry="10" fill="#f1c40f" stroke="#e67e22" stroke-width="3" />
                <rect x="350" y="50" width="100" height="40" rx="5" ry="5" fill="#2c3e50" />
                <text x="400" y="30" class="text-label">Amperímetro</text>
                <text x="400" y="78" class="text-value" fill="#43b581">{current_I:.2f}<tspan class="text-unit">A</tspan></text>
                <!-- Terminal Connectors -->
                <circle cx="370" cy="105" r="6" fill="#e74c3c" />
                <circle cx="430" cy="105" r="6" fill="#2c3e50" />
                
                <!-- Rheostat (Realistic Cylinder) -->
                <text x="600" y="130" class="text-label">Reóstato</text>
                <!-- Cylinder Base -->
                <rect x="565" y="140" width="70" height="140" rx="10" fill="#2c3e50" stroke="#34495e" stroke-width="4" />
                <!-- Wire Coils -->
                <rect x="575" y="150" width="50" height="120" fill="#95a5a6" />
                <path d="M 575 160 L 625 160 M 575 170 L 625 170 M 575 180 L 625 180 M 575 190 L 625 190 M 575 200 L 625 200 M 575 210 L 625 210 M 575 220 L 625 220 M 575 230 L 625 230 M 575 240 L 625 240 M 575 250 L 625 250 M 575 260 L 625 260" stroke="#7f8c8d" stroke-width="3" />
                <!-- Slider Rod -->
                <rect x="555" y="145" width="10" height="130" rx="5" fill="#bdc3c7" stroke="#7f8c8d" stroke-width="2" />
                <text x="600" y="310" class="text-label" fill="#f1c40f">R = {r_ext:.1f} Ω</text>
                
                <!-- Slider Mechanism (Moves with r_percentage) -->
                <g transform="translate(0, {(90 * r_percentage / 100)})">
                    <rect x="545" y="155" width="30" height="20" rx="5" fill="#e74c3c" stroke="#c0392b" stroke-width="2" /> <!-- Knob -->
                    <polygon points="575,165 585,155 585,175" fill="#e74c3c" /> <!-- Arrow touching coils -->
                </g>
                
                <!-- Voltmeter (Realistic Digital Multimeter) -->
                <rect x="40" y="160" width="120" height="80" rx="10" ry="10" fill="#f1c40f" stroke="#e67e22" stroke-width="3" />
                <rect x="50" y="170" width="100" height="40" rx="5" ry="5" fill="#2c3e50" />
                <text x="100" y="150" class="text-label">Voltímetro</text>
                <text x="100" y="198" class="text-value" fill="#e74c3c">{current_U:.2f}<tspan class="text-unit">V</tspan></text>
                <!-- Terminal Connectors -->
                <circle cx="70" cy="225" r="6" fill="#e74c3c" />
                <circle cx="130" cy="225" r="6" fill="#2c3e50" />
                
                <!-- Central Power Display -->
                <rect x="290" y="180" width="220" height="80" class="component-box" style="fill: rgba(35, 39, 42, 0.8);" />
                <text x="400" y="210" class="text-label" style="fill: #00e5ff;">Potência Útil (P)</text>
                <text x="400" y="245" class="text-value" fill="#fff">{current_P:.2f} <tspan class="text-unit" fill="#00e5ff">W</tspan></text>
            </svg>
        </div>
    </body>
    </html>
    """
    return html_code
