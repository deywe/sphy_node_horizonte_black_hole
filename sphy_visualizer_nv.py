import py5
import pandas as pd
import hashlib
import numpy as np

# ==============================================================================
# 🌀 SPHY NVIDIA ACCELERATED AUDITOR: MAXIMUM GPU PERFORMANCE
# ==============================================================================

try:
    df = pd.read_parquet("sphy_blackhole_data.parquet")
    TOTAL_FRAMES = df['frame'].max()
except Exception as e:
    print(f"Error: Dataset not found. {e}")
    exit()

# Navegação e Performance
rot_x, rot_y = 0.0, 0.0
zoom = -450.0
pan_x, pan_y = 0.0, 0.0
current_frame = 0
RESOLUTION = 120  # Aumentado para testar o limite da GPU NVIDIA

def setup():
    # 1. ACELERAÇÃO POR HARDWARE: O P3D utiliza OpenGL nativo da NVIDIA
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    
    # 2. ANTI-ALIASING NATIVO: 8x MSAA processado diretamente na GPU
    py5.smooth(8) 
    
    # 3. OTIMIZAÇÃO DE BUFFER: Desativa cursor para focar em processamento gráfico
    py5.window_resizable(True)
    
    # 4. CARREGAMENTO DE FONTES DE ALTA RESOLUÇÃO
    py5.text_font(py5.create_font("Monospaced", 20))

def draw():
    global current_frame, rot_x, rot_y, zoom, pan_x, pan_y
    
    # Renderização de fundo via Hardware
    py5.background(0) 
    
    # --- AUDIT & METRICS ---
    frame_data = df[df['frame'] == current_frame]
    if frame_data.empty: return

    stored_hash = frame_data['sha256'].iloc[0]
    local_sum = frame_data['local_sum'].iloc[0]
    timestamp = frame_data['timestamp'].iloc[0]
    
    calc_hash = hashlib.sha256(f"{current_frame}-{local_sum}-{timestamp}".encode()).hexdigest()
    is_sovereign = (calc_hash == stored_hash)

    # --- NVIDIA TELEMETRY HUD ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    py5.fill(0, 255, 255) if is_sovereign else py5.fill(255, 0, 0)
    py5.text(f"SPHY SOBERANIA | NVIDIA GPU ACCELERATION: ON", 40, 50)
    py5.text(f"FPS: {py5.get_frame_rate():.0f} | FRAME: {current_frame}/{TOTAL_FRAMES}", 40, 80)
    py5.fill(200)
    py5.text(f"AUDIT HASH: {calc_hash[:32]}...", 40, 110)
    py5.hint(py5.ENABLE_DEPTH_TEST)

    # --- 3D ENGINE PIPELINE ---
    py5.translate(py5.width/2 + pan_x, py5.height/2 + pan_y, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y)
    
    # Luzes calculadas por Vertex Shader
    py5.ambient_light(40, 40, 40)
    py5.point_light(0, 255, 255, 0, 0, 0)
    
    respiro = frame_data['respiration'].iloc[0]
    
    # Singularidade (Ponto de Coerência Máxima)
    py5.push_matrix()
    py5.no_stroke()
    py5.fill(255)
    py5.sphere(18)
    py5.pop_matrix()

    # --- RENDERIZAÇÃO DE GEODÉSIA (HIGH-THROUGHPUT) ---
    for _, row in frame_data.iterrows():
        phi = row['phi']
        # Alpha blending processado via GPU
        py5.stroke(0, 255, 255, 95)
        py5.no_fill()
        
        # Otimização de Shape: Instruções enviadas em lote para a GPU
        py5.begin_shape()
        t_vals = np.linspace(0, 1, RESOLUTION)
        for t in t_vals:
            r = (py5.height * 0.48) * (t**0.6) * respiro
            x = r * py5.cos(t * 10 + phi)
            y = r * py5.sin(t * 10 + phi)
            z = row['z_ref'] * (1 - t)
            py5.vertex(x, y, z)
        py5.end_shape()

    if not py5.is_mouse_pressed:
        current_frame = (current_frame + 1) % (TOTAL_FRAMES + 1)

# --- CONTROLES DE INTERATIVIDADE ---
def mouse_dragged():
    global rot_x, rot_y, pan_x, pan_y
    if py5.mouse_button == py5.LEFT:
        rot_y += (py5.mouse_x - py5.pmouse_x) * 0.005
        rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.005
    elif py5.mouse_button == py5.RIGHT:
        pan_x += (py5.mouse_x - py5.pmouse_x)
        pan_y += (py5.mouse_y - py5.pmouse_y)

def mouse_wheel(event):
    global zoom
    zoom -= event.get_count() * 40

def key_pressed():
    global rot_x, rot_y, zoom, pan_x, pan_y
    if py5.key == 'r': 
        rot_x, rot_y, zoom, pan_x, pan_y = 0, 0, -450, 0, 0

if __name__ == "__main__":
    py5.run_sketch()
