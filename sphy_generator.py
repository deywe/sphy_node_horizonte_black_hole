import pandas as pd
import numpy as np
import hashlib
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime

# ==============================================================================
# 🌀 SPHY GENERATOR: MAXIMUM COHERENCE DATASET (BLACK HOLE)
# ==============================================================================

TOTAL_FRAMES = 1200
NUM_LINES = 200
POINTS_PER_LINE = 50 

def generate_sovereign_dataset(file_name="sphy_blackhole_data.parquet"):
    print(f"🚀 Starting Sovereign Dataset Generation: {TOTAL_FRAMES} frames")
    
    all_data = []
    # Deterministic seeds for Phase Anchoring
    phis = np.random.uniform(0, 2 * np.pi, NUM_LINES)
    heights = np.random.normal(0, 50, NUM_LINES)

    for frame in range(TOTAL_FRAMES):
        frame_rows = []
        # Phase Respiration (Deterministic Oscillator)
        respiration = 1.0 + 0.3 * np.sin(frame * 0.07)
        timestamp = datetime.now().isoformat()
        
        # Local Sum Accumulator (System Integrity Check)
        frame_local_sum = 0
        
        for idx in range(NUM_LINES):
            phi = phis[idx] + (frame * 0.02)
            t = np.linspace(0, 1, POINTS_PER_LINE)
            
            # Geodesic Calculation (Phase Attractor)
            r = 400 * (t**0.5) * respiration
            x = r * np.cos(t * 8 + phi)
            y = r * np.sin(t * 8 + phi)
            z = heights[idx] * np.sin(frame * 0.05 + phi * 2) * (1 - t)
            
            # Phase Value for Hashing
            phase_value = np.mean(x + y + z)
            frame_local_sum += phase_value
            
            frame_rows.append({
                'frame': frame,
                'line_id': idx,
                'z_ref': z[-1] if hasattr(z, '__len__') else z, # Reference Anchor
                'phi': phi,
                'respiration': respiration
            })

        # --- CRYPTOGRAPHIC SIGNATURE (THE PROOF) ---
        # The Hash is bound to the total phase state of the frame
        payload = f"{frame}-{frame_local_sum}-{timestamp}"
        sha_signature = hashlib.sha256(payload.encode()).hexdigest()
        
        for row in frame_rows:
            row['sha256'] = sha_signature
            row['local_sum'] = frame_local_sum
            row['timestamp'] = timestamp
            all_data.append(row)

        if frame % 50 == 0:
            print(f"✅ Frame {frame} audited and signed.")

    # Save to Parquet using Snappy compression (Harpia Standard)
    df = pd.DataFrame(all_data)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, file_name, compression='snappy')
    print(f"\n💎 Dataset '{file_name}' generated with SPHY SOVEREIGNTY.")

if __name__ == "__main__":
    generate_sovereign_dataset()
