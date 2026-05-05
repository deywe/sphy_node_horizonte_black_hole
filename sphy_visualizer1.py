import py5
import pandas as pd
import hashlib
import numpy as np

# ==============================================================================
# 🌀 SPHY INTERACTIVE AUDITOR: HIGH-RES GPU NAVIGATION
# ==============================================================================

# Carregamento dos dados
try:
    df = pd.read_parquet("sphy_blackhole_data.parquet")
    TOTAL_FRAMES = df['frame'].max()
except Exception as e:
    print(f"Error: Run the Generator first. {e}")
    exit()

# --- VARIÁVEIS DE NAVEGAÇÃO SOBERANA ---
rot_x, rot_y = 0.0, 0.0
zoom = -450.0
pan_x, pan_y = 0.0, 0.0
current_frame = 0
RESOLUTION = 100  # Resolução para curvatura de Proporção Áurea

def setup():
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    py5.smooth(8) 
    py5.window_resizable(True)
    py5.text_font(py5.create_font("Monospaced", 18))

def draw():
    global current_frame, rot_x, rot_y, zoom, pan_x, pan_y
    py5.background(5) 
    
    # --- LÓGICA DE AUDITORIA ---
    frame_data = df[df['frame'] == current_frame]
    if frame_data.empty: return

    stored_hash = frame_data['sha256'].iloc[0]
    local_sum = frame_data['local_sum'].iloc[0]
    timestamp = frame_data['timestamp'].iloc[0]
    
    raw_check = f"{current_frame}-{local_sum}-{timestamp}"
    calc_hash = hashlib.sha256(raw_check.encode()).hexdigest()
    is_sovereign = (calc_hash == stored_hash)

    # --- HUD ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 255) if is_sovereign else py5.fill(255, 0, 0)
    py5.text(f"SPHY AUDITOR | FRAME: {current_frame}/{TOTAL_FRAMES}", 40, 50)
    py5.text(f"STATUS: {'SOVEREIGN' if is_sovereign else 'VIOLATION'}", 40, 80)
    py5.fill(200)
    py5.text(f"HASH: {calc_hash[:32]}...", 40, 110)
    py5.hint(py5.ENABLE_DEPTH_TEST)

    # --- MOTOR DE INTERATIVIDADE (CÂMERA) ---
    # Translação para o centro + Pan do usuário + Zoom
    py5.translate(py5.width/2 + pan_x, py5.height/2 + pan_y, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y)
    
    py5.lights()
    respiration = frame_data['respiration'].iloc[0]
    
    # Singularidade Central
    py5.no_stroke()
    py5.fill(255)
    py5.sphere(18)

    # Reconstrução Suave do Campo Ortogonal
    for _, row in frame_data.iterrows():
        phi = row['phi']
        py5.stroke(0, 255, 255, 85)
        py5.no_fill()
        
        py5.begin_shape()
        t_vals = np.linspace(0, 1, RESOLUTION)
        for t in t_vals:
            # R decai para o centro (Curvatura Geodésica)
            r = (py5.height * 0.48) * (t**0.6) * respiration
            x = r * py5.cos(t * 10 + phi)
            y = r * py5.sin(t * 10 + phi)
            z = row['z_ref'] * (1 - t)
            py5.vertex(x, y, z)
        py5.end_shape()

    # Controle de avanço automático (pode ser pausado se desejar)
    if not py5.is_mouse_pressed:
        current_frame = (current_frame + 1) % (TOTAL_FRAMES + 1)

# --- HANDLERS DE INTERAÇÃO (MOUSE & ZOOM) ---

def mouse_dragged():
    global rot_x, rot_y, pan_x, pan_y
    # Botão ESQUERDO: Rotacionar em torno da singularidade
    if py5.mouse_button == py5.LEFT:
        rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01
    # Botão DIREITO: Mover (Pan) o plano de observação
    elif py5.mouse_button == py5.RIGHT:
        pan_x += (py5.mouse_x - py5.pmouse_x)
        pan_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global zoom
    # Scroll: Zoom na estrutura de fase
    zoom -= event.get_count() * 50

def key_pressed():
    global rot_x, rot_y, zoom, pan_x, pan_y, current_frame
    if py5.key == 'r': # Resetar visão soberana
        rot_x, rot_y = 0, 0
        zoom, pan_x, pan_y = -450, 0, 0
    if py5.key == ' ': # Pausar/Continuar linha do tempo
        if py5.is_looping: py5.no_loop()
        else: py5.loop()

if __name__ == "__main__":
    py5.run_sketch()
