import py5
import pandas as pd
import hashlib
import numpy as np

# ==============================================================================
# 🌀 SPHY VISUALIZER: INTERACTIVE BLACK HOLE AUDITOR (GPU)
# ==============================================================================

# Load the signed dataset
try:
    df = pd.read_parquet("sphy_blackhole_data.parquet")
    TOTAL_FRAMES = df['frame'].max()
except Exception as e:
    print(f"Error: Dataset not found. Run the Generator first. {e}")
    exit()

# Camera & Interaction Variables
rot_x, rot_y = 0.0, 0.0
zoom = -450.0
current_frame = 0

def setup():
    # GPU Acceleration via P3D
    py5.size(py5.display_width, py5.display_height, py5.P3D)
    py5.smooth(8) # Hardware Anti-Aliasing
    py5.window_resizable(True)
    py5.text_font(py5.create_font("Monospaced", 18))

def draw():
    global current_frame, rot_x, rot_y, zoom
    py5.background(5) # Deep Phase Space
    
    # --- AUDIT LOGIC ---
    frame_data = df[df['frame'] == current_frame]
    if frame_data.empty: return

    stored_hash = frame_data['sha256'].iloc[0]
    local_sum = frame_data['local_sum'].iloc[0]
    timestamp = frame_data['timestamp'].iloc[0]
    
    # Recalculate Hash (Integrity Verification)
    raw_check = f"{current_frame}-{local_sum}-{timestamp}"
    calc_hash = hashlib.sha256(raw_check.encode()).hexdigest()
    is_sovereign = (calc_hash == stored_hash)

    # --- SOVEREIGNTY HUD ---
    py5.hint(py5.DISABLE_DEPTH_TEST)
    if is_sovereign:
        py5.fill(0, 255, 255) # Cyan for Coherence
        status_txt = "STATUS: SOVEREIGN (TOTAL INTEGRITY)"
    else:
        py5.fill(255, 0, 0) # Red for Data Corruption/Noise
        status_txt = "STATUS: DATA VIOLATION DETECTED"
    
    py5.text(f"SPHY BLACK HOLE AUDITOR | FRAME: {current_frame}/{TOTAL_FRAMES}", 40, 50)
    py5.text(status_txt, 40, 80)
    py5.fill(200)
    py5.text(f"SHA-256: {calc_hash[:32]}...", 40, 110)
    py5.hint(py5.ENABLE_DEPTH_TEST)

    # --- INTERACTIVE GPU RENDERER ---
    py5.translate(py5.width/2, py5.height/2, zoom)
    py5.rotate_x(rot_x)
    py5.rotate_y(rot_y)
    
    py5.lights() # Calculate lighting on GPU
    respiration = frame_data['respiration'].iloc[0]
    
    # The Singularity (Maximum Coherence Center)
    py5.no_stroke()
    py5.fill(255)
    py5.sphere(18 + 4 * py5.sin(py5.frame_count * 0.1))

    # Reconstruct Event Horizon from Phase Logic
    for _, row in frame_data.iterrows():
        phi = row['phi']
        py5.stroke(0, 255, 255, 75)
        py5.no_fill()
        
        py5.begin_shape()
        t_vals = np.linspace(0, 1, 35)
        for t in t_vals:
            # Orthogonal Field Curvature
            r = (py5.height * 0.48) * (t**0.6) * respiration
            x = r * py5.cos(t * 10 + phi)
            y = r * py5.sin(t * 10 + phi)
            z = row['z_ref'] * (1 - t)
            py5.vertex(x, y, z)
        py5.end_shape()

    # Progress Through the Deterministic Timeline
    current_frame = (current_frame + 1) % (TOTAL_FRAMES + 1)

# --- INTERACTION CONTROLS ---
def mouse_dragged():
    global rot_x, rot_y
    if py5.mouse_button == py5.LEFT:
        rot_y += (py5.mouse_x - py5.pmouse_x) * 0.01
        rot_x -= (py5.mouse_y - py5.pmouse_y) * 0.01

def mouse_wheel(event):
    global zoom
    zoom -= event.get_count() * 50

if __name__ == "__main__":
    py5.run_sketch()
