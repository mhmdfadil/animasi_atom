# Import library yang diperlukan
import numpy as np  # Untuk operasi matematika dan array
import matplotlib.pyplot as plt  # Untuk visualisasi
from matplotlib.animation import FuncAnimation  # Untuk animasi
from mpl_toolkits.mplot3d import Axes3D  # Untuk plot 3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # Untuk objek 3D
import matplotlib.animation as animation  # Untuk animasi
from pydub import AudioSegment  # Untuk memproses audio
from scipy.io import wavfile  # Untuk membaca file wav
import subprocess  # Untuk menjalankan perintah shell
import os  # Untuk operasi sistem file
from matplotlib.patches import FancyArrowPatch  # Untuk panah 3D
from mpl_toolkits.mplot3d import proj3d  # Untuk proyeksi 3D
from matplotlib.colors import LinearSegmentedColormap  # Untuk gradien warna
from matplotlib import cm  # Untuk colormap
from textwrap import wrap  # Untuk wrapping text

# Konfigurasi video vertikal 9:16
VIDEO_DURATION = 120  # Durasi video dalam detik (30 detik per model atom)
VIDEO_FPS = 30  # Frame rate video
TOTAL_FRAMES = VIDEO_DURATION * VIDEO_FPS  # Total frame video
VIDEO_WIDTH = 1080  # Lebar video (untuk orientasi vertikal)
VIDEO_HEIGHT = 1920  # Tinggi video (untuk orientasi vertikal)
OUTPUT_FILE = "atomic_models_animation_enhanced.mp4"  # Nama file output
AUDIO_FILE = "music.mp3"  # File audio background
TEMP_AUDIO_FILE = "temp_audio.wav"  # File audio sementara

# Warna modern dengan transparansi
COLORS = {
    'background': '#121212',  # Warna background gelap
    'text': '#FFFFFF',  # Warna teks putih
    'electron': '#4285F4',  # Biru untuk elektron
    'proton': '#EA4335',    # Merah untuk proton
    'neutron': '#34A853',   # Hijau untuk neutron
    'nucleus': '#FBBC05',   # Kuning untuk inti atom
    'orbit': '#9C27B0',     # Ungu untuk orbit
    'highlight': '#00ACC1', # Cyan untuk highlight
    'glow': '#FFFFFF'       # Putih untuk efek glow
}

# Fungsi untuk membuat gradien warna partikel
def create_particle_cmap(base_color):
    return LinearSegmentedColormap.from_list('particle_cmap', 
                                           ['#FFFFFF', base_color, '#000000'])

# Fungsi untuk memproses audio
def process_audio(audio_path, duration):
    # Memuat file audio dan memotongnya sesuai durasi video
    audio = AudioSegment.from_mp3(audio_path)
    if len(audio) > duration * 1000:
        audio = audio[:duration * 1000]
    audio.export(TEMP_AUDIO_FILE, format="wav")  # Export ke format wav
    return TEMP_AUDIO_FILE

# Proses audio
audio_path = process_audio(AUDIO_FILE, VIDEO_DURATION)

# Buat figure dengan orientasi vertikal
fig = plt.figure(figsize=(10.8, 19.2), dpi=100)  # Rasio 9:16 (1080x1920)
ax = fig.add_subplot(111, projection='3d')  # Subplot 3D
ax.set_xlim(-8, 8)  # Batas sumbu x
ax.set_ylim(-8, 8)  # Batas sumbu y
ax.set_zlim(-8, 8)  # Batas sumbu z
ax.set_axis_off()  # Matikan sumbu
ax.set_facecolor(COLORS['background'])  # Warna background
fig.set_facecolor(COLORS['background'])  # Warna background figure

# Fungsi untuk membuat partikel 3D dengan efek glow
def create_glowing_particle(x, y, z, radius, color, alpha=1.0, glow_size=1.5):
    # Membuat koordinat partikel utama
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 40)
    x_p = x + radius * np.outer(np.cos(u), np.sin(v))
    y_p = y + radius * np.outer(np.sin(u), np.sin(v))
    z_p = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    # Membuat koordinat efek glow
    u_g = np.linspace(0, 2 * np.pi, 40)
    v_g = np.linspace(0, np.pi, 40)
    x_g = x + radius*glow_size * np.outer(np.cos(u_g), np.sin(v_g))
    y_g = y + radius*glow_size * np.outer(np.sin(u_g), np.sin(v_g))
    z_g = z + radius*glow_size * np.outer(np.ones(np.size(u_g)), np.cos(v_g))
    
    return (x_p, y_p, z_p), (x_g, y_g, z_g)

# Fungsi untuk membuat orbit 3D elips
def create_elliptical_orbit(a, b, c, color, alpha=0.3, resolution=100, z_rotate=0):
    # Membuat orbit elips dengan variasi sumbu
    theta = np.linspace(0, 2*np.pi, resolution)
    x = a * np.cos(theta)
    y = b * np.sin(theta)
    z = c * np.sin(theta/2)  # Variasi sumbu z untuk efek 3D
    
    # Rotasi orbit jika diperlukan
    if z_rotate != 0:
        rot_matrix = np.array([
            [np.cos(z_rotate), -np.sin(z_rotate), 0],
            [np.sin(z_rotate), np.cos(z_rotate), 0],
            [0, 0, 1]
        ])
        x, y, z = np.dot(rot_matrix, np.vstack([x, y, z]))
    
    return x, y, z

# Teks judul dan deskripsi
title = ax.text2D(0.5, 0.92, "", color=COLORS['text'], transform=fig.transFigure,
                 ha='center', va='center', fontsize=48, fontweight='bold',
                 fontfamily='sans-serif')

subtitle = ax.text2D(0.5, 0.88, "", color=COLORS['highlight'], transform=fig.transFigure,
                    ha='center', va='center', fontsize=32, fontweight='normal',
                    fontfamily='sans-serif')

description = ax.text2D(0.5, 0.12, "", color=COLORS['text'], transform=fig.transFigure,
                       ha='center', va='center', fontsize=30, wrap=True,
                       fontfamily='sans-serif', bbox=dict(facecolor='#12121280', edgecolor='none', pad=10))

# Fungsi update untuk animasi
def update(frame):
    ax.clear()  # Bersihkan axes
    ax.set_xlim(-8, 8)  # Set batas sumbu
    ax.set_ylim(-8, 8)
    ax.set_zlim(-8, 8)
    ax.set_axis_off()  # Matikan sumbu
    ax.set_facecolor(COLORS['background'])  # Set warna background
    
    progress = frame / TOTAL_FRAMES  # Hitung progress animasi
    
    # Rotasi kamera dengan variasi
    elev = 20 + 10 * np.sin(progress * np.pi/3)
    azim = progress * 360
    ax.view_init(elev=elev, azim=azim)
    
    # Pembagian waktu untuk setiap model atom
    section = int(progress * 4)  # 4 bagian untuk 4 model atom
    section_progress = (progress * 4) % 1  # Progress dalam bagian saat ini
    
    # Efek transisi antar bagian
    if section_progress < 0.1:
        transition_alpha = section_progress * 10
    elif section_progress > 0.9:
        transition_alpha = (1 - section_progress) * 10
    else:
        transition_alpha = 1.0
    
    # Model Atom Dalton (1803)
    if section == 0:
        title.set_text("Dalton's Atomic Model")
        subtitle.set_text("(1803)")
        
        desc_text = "John Dalton proposed that:\n" \
                   "• Matter is made of indivisible atoms\n" \
                   "• Atoms of same element are identical\n" \
                   "• Compounds form from atom combinations"
        
        # Animasikan teks deskripsi
        if section_progress < 0.3:
            title.set_alpha(section_progress * 3)
            subtitle.set_alpha(section_progress * 3)
            description.set_alpha(0)
        else:
            title.set_alpha(1)
            subtitle.set_alpha(1)
            description.set_alpha(min(1, (section_progress-0.3)*2))
            animate_text(description, desc_text, min(1, (section_progress-0.3)*3))
        
        # Visualisasi model Dalton
        if section_progress > 0.2:
            atoms = [
                (-3, -2, 0, 1.6, COLORS['proton'], 0, 0),
                (3, 2, 0, 2.0, COLORS['electron'], np.pi/4, np.pi/4),
                (0, -3, 2, 1.2, COLORS['neutron'], np.pi/3, -np.pi/3)
            ]
            
            for i, (x, y, z, size, color, rot_x, rot_y) in enumerate(atoms):
                # Buat partikel dengan efek glow
                (x_p, y_p, z_p), (x_g, y_g, z_g) = create_glowing_particle(
                    x, y, z, size, color, 0.9, 1.8)
                
                # Gambar glow
                ax.plot_surface(x_g, y_g, z_g, color=COLORS['glow'], 
                              alpha=transition_alpha*0.2, edgecolor='none')
                
                # Gambar partikel dengan gradien warna
                cmap = create_particle_cmap(color)
                ax.plot_surface(x_p, y_p, z_p, color=color, cmap=cmap, 
                               alpha=transition_alpha*0.9, edgecolor='none')
                
                # Label elemen
                if section_progress > 0.5:
                    ax.text(x, y, z + size + 0.5, f"Element {i+1}", 
                           color=COLORS['text'], ha='center', fontsize=18,
                           alpha=min(1, (section_progress-0.5)*2))
    
    # Model Atom Thomson (1904)
    elif section == 1:
        title.set_text("Thomson's Plum Pudding Model")
        subtitle.set_text("(1904)")
        
        desc_text = "J.J. Thomson discovered electrons and proposed:\n" \
                   "• Atoms contain negatively charged electrons\n" \
                   "• Electrons are embedded in positive 'pudding'\n" \
                   "• Overall atom is electrically neutral"
        
        # Atur transparansi teks
        title.set_alpha(1)
        subtitle.set_alpha(1)
        description.set_alpha(min(1, section_progress*3))
        animate_text(description, desc_text, min(1, section_progress*3))
        
        # Visualisasi model Thomson
        if section_progress > 0.1:
            # Bola positif besar
            (x_p, y_p, z_p), (x_g, y_g, z_g) = create_glowing_particle(
                0, 0, 0, 5, COLORS['nucleus'], 0.2, 2.0)
            
            ax.plot_surface(x_g, y_g, z_g, color=COLORS['glow'], 
                          alpha=transition_alpha*0.1, edgecolor='none')
            ax.plot_surface(x_p, y_p, z_p, color=COLORS['nucleus'], 
                          alpha=transition_alpha*0.3, edgecolor='none')
            
            # Elektron kecil bergerak acak
            if section_progress > 0.2:
                n_electrons = min(12, int(section_progress * 20))
                np.random.seed(42)  # Untuk konsistensi animasi
                
                for i in range(n_electrons):
                    # Posisi acak dengan gerakan
                    theta = np.random.uniform(0, 2*np.pi)
                    phi = np.random.uniform(0, np.pi)
                    r = np.random.uniform(2, 4.5)
                    
                    move_factor = np.sin(progress*5 + i) * 0.5
                    x = r * np.sin(phi + move_factor) * np.cos(theta + progress*3)
                    y = r * np.sin(phi + move_factor) * np.sin(theta + progress*3)
                    z = r * np.cos(phi + move_factor)
                    
                    # Buat elektron dengan glow
                    (x_e, y_e, z_e), (x_eg, y_eg, z_eg) = create_glowing_particle(
                        x, y, z, 0.4, COLORS['electron'], 0.9, 1.5)
                    
                    ax.plot_surface(x_eg, y_eg, z_eg, color=COLORS['glow'], 
                                  alpha=transition_alpha*0.2, edgecolor='none')
                    ax.plot_surface(x_e, y_e, z_e, color=COLORS['electron'], 
                                  alpha=transition_alpha*0.9, edgecolor='none')
    
    # Model Atom Rutherford (1911)
    elif section == 2:
        title.set_text("Rutherford's Nuclear Model")
        subtitle.set_text("(1911)")
        
        desc_text = "Rutherford's gold foil experiment showed:\n" \
                   "• Atom has a tiny, dense nucleus\n" \
                   "• Electrons orbit the nucleus\n" \
                   "• Most of atom is empty space"
        
        # Atur transparansi teks
        title.set_alpha(1)
        subtitle.set_alpha(1)
        description.set_alpha(min(1, section_progress*3))
        animate_text(description, desc_text, min(1, section_progress*3))
        
        # Visualisasi model Rutherford
        if section_progress > 0.1:
            # Inti atom kecil
            (x_n, y_n, z_n), (x_ng, y_ng, z_ng) = create_glowing_particle(
                0, 0, 0, 1.0, COLORS['nucleus'], 0.9, 2.0)
            
            ax.plot_surface(x_ng, y_ng, z_ng, color=COLORS['glow'], 
                          alpha=transition_alpha*0.2, edgecolor='none')
            ax.plot_surface(x_n, y_n, z_n, color=COLORS['nucleus'], 
                          alpha=transition_alpha*0.9, edgecolor='none')
            
            # Orbit elektron elips 3D
            if section_progress > 0.2:
                n_orbits = 3
                for i in range(n_orbits):
                    a = 2.5 + i * 1.5
                    b = 2.0 + i * 1.2
                    c = 0.8 + i * 0.5
                    
                    # Buat orbit dengan rotasi unik
                    x_o, y_o, z_o = create_elliptical_orbit(
                        a, b, c, COLORS['orbit'], 0.3, 100, z_rotate=i*np.pi/6)
                    
                    # Gambar orbit bertahap
                    if section_progress > 0.2 + i*0.15:
                        ax.plot(x_o, y_o, z_o, color=COLORS['orbit'], 
                              alpha=transition_alpha*0.5, linestyle='--', linewidth=2.0)
                        
                        # Elektron yang mengorbit
                        if section_progress > 0.3 + i*0.15:
                            angle = (progress * 10 + i) * 2 * np.pi
                            x_e = a * np.cos(angle)
                            y_e = b * np.sin(angle)
                            z_e = c * np.sin(angle/2)
                            
                            # Buat elektron dengan glow
                            (x_el, y_el, z_el), (x_eg, y_eg, z_eg) = create_glowing_particle(
                                x_e, y_e, z_e, 0.4, COLORS['electron'], 0.9, 1.5)
                            
                            ax.plot_surface(x_eg, y_eg, z_eg, color=COLORS['glow'], 
                                          alpha=transition_alpha*0.2, edgecolor='none')
                            ax.plot_surface(x_el, y_el, z_el, color=COLORS['electron'], 
                                          alpha=transition_alpha*0.9, edgecolor='none')
    
    # Model Atom Bohr (1913)
    else:
        title.set_text("Bohr's Quantum Model")
        subtitle.set_text("(1913)")
        
        desc_text = "Niels Bohr introduced quantum theory:\n" \
                   "• Electrons move in fixed orbits (energy levels)\n" \
                   "• Orbits have quantized energy\n" \
                   "• Light is emitted when electrons jump levels"
        
        # Atur transparansi teks
        title.set_alpha(1)
        subtitle.set_alpha(1)
        description.set_alpha(min(1, section_progress*3))
        animate_text(description, desc_text, min(1, section_progress*3))
        
        # Visualisasi model Bohr
        if section_progress > 0.1:
            # Inti atom dengan glow
            (x_n, y_n, z_n), (x_ng, y_ng, z_ng) = create_glowing_particle(
                0, 0, 0, 1.0, COLORS['nucleus'], 0.9, 2.0)
            
            ax.plot_surface(x_ng, y_ng, z_ng, color=COLORS['glow'], 
                          alpha=transition_alpha*0.2, edgecolor='none')
            ax.plot_surface(x_n, y_n, z_n, color=COLORS['nucleus'], 
                          alpha=transition_alpha*0.9, edgecolor='none')
            
            # Orbit diskrit (tingkat energi)
            n_orbits = 3
            for i in range(n_orbits):
                radius = 1.5 + i * 2.0
                x_o, y_o, z_o = create_elliptical_orbit(
                    radius, radius*0.9, radius*0.3, COLORS['orbit'], 0.3, 100, z_rotate=i*np.pi/8)
                
                if section_progress > 0.2 + i*0.15:
                    ax.plot(x_o, y_o, z_o, color=COLORS['orbit'], 
                          alpha=transition_alpha*0.7, linewidth=2.5)
                    
                    # Label tingkat energi
                    if section_progress > 0.3 + i*0.15:
                        ax.text(radius, 0, 0.5, f"n={i+1}", color=COLORS['text'], 
                              ha='center', fontsize=18, alpha=transition_alpha)
            
            # Animasi transisi elektron
            if section_progress > 0.5:
                # Posisi elektron berdasarkan progress
                if section_progress < 0.6:
                    # Di tingkat dasar (n=1)
                    level = 0
                    angle = progress * 10 * 2 * np.pi
                    radius = 1.5 + level * 2.0
                    x_e = radius * np.cos(angle)
                    y_e = radius * np.sin(angle)
                    z_e = 0
                elif section_progress < 0.7:
                    # Transisi ke tingkat n=2
                    trans_progress = (section_progress - 0.6) * 10
                    start_radius = 1.5
                    end_radius = 3.5
                    radius = start_radius + (end_radius - start_radius) * trans_progress
                    angle = progress * 10 * 2 * np.pi
                    x_e = radius * np.cos(angle)
                    y_e = radius * np.sin(angle)
                    z_e = trans_progress * 1.5  # Gerakan vertikal
                else:
                    # Di tingkat n=2
                    level = 1
                    angle = (progress - 0.1) * 5 * 2 * np.pi
                    radius = 1.5 + level * 2.0
                    x_e = radius * np.cos(angle)
                    y_e = radius * np.sin(angle)
                    z_e = 0
                
                # Buat elektron dengan glow
                (x_el, y_el, z_el), (x_eg, y_eg, z_eg) = create_glowing_particle(
                    x_e, y_e, z_e, 0.5, COLORS['electron'], 0.9, 1.8)
                
                ax.plot_surface(x_eg, y_eg, z_eg, color=COLORS['glow'], 
                              alpha=transition_alpha*0.2, edgecolor='none')
                ax.plot_surface(x_el, y_el, z_el, color=COLORS['electron'], 
                              alpha=transition_alpha*0.9, edgecolor='none')
                
                # Panah foton saat transisi
                if 0.6 < section_progress < 0.65:
                    ax.plot([x_e, x_e], [y_e, y_e], [z_e, z_e + 4], color=COLORS['highlight'], 
                          linewidth=4, alpha=(section_progress-0.6)*10)
                    ax.text(x_e, y_e, z_e + 5, "Photon emitted", color=COLORS['highlight'], 
                          ha='center', fontsize=20, alpha=(section_progress-0.6)*10)
    
    return []  # Return empty list for blit=False

# Fungsi untuk animasi teks bertahap
def animate_text(text_obj, full_text, progress):
    chars_to_show = int(progress * len(full_text))
    partial_text = full_text[:chars_to_show]
    text_obj.set_text(partial_text)

# Buat animasi
ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, interval=1000/VIDEO_FPS, blit=False)

# Simpan animasi tanpa audio terlebih dahulu
temp_video = "temp_video.mp4"
writer = animation.FFMpegWriter(fps=VIDEO_FPS, bitrate=12000, 
                               extra_args=['-preset', 'slow', '-crf', '18'])
ani.save(temp_video, writer=writer, dpi=100)

# Gabungkan video dan audio
def combine_video_audio(video_path, audio_path, output_path):
    cmd = [
        'ffmpeg',
        '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-map', '0:v:0',
        '-map', '1:a:0',
        '-shortest',
        '-movflags', '+faststart',
        '-pix_fmt', 'yuv420p',
        output_path
    ]
    subprocess.run(cmd)

combine_video_audio(temp_video, TEMP_AUDIO_FILE, OUTPUT_FILE)

# Bersihkan file sementara
os.remove(temp_video)
os.remove(TEMP_AUDIO_FILE)

print(f"Enhanced atomic models animation complete! Saved to {OUTPUT_FILE}")