# Import library numpy untuk komputasi numerik
import numpy as np

# Import modul pyplot dari matplotlib untuk visualisasi 2D/3D
import matplotlib.pyplot as plt

# Import FuncAnimation untuk membuat animasi
from matplotlib.animation import FuncAnimation

# Import toolkit 3D dari matplotlib
from mpl_toolkits.mplot3d import Axes3D

# Import Poly3DCollection untuk menggambar objek 3D kompleks
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Import modul animation dari matplotlib
import matplotlib.animation as animation

# Import AudioSegment dari pydub untuk memproses audio
from pydub import AudioSegment

# Import wavfile dari scipy.io untuk membaca file WAV
from scipy.io import wavfile

# Import subprocess untuk menjalankan perintah shell/FFmpeg
import subprocess

# Import modul os untuk operasi sistem file
import os

# Import FancyArrowPatch untuk menggambar panah 3D
from matplotlib.patches import FancyArrowPatch

# Import proj3d untuk proyeksi 3D
from mpl_toolkits.mplot3d import proj3d

# Import LinearSegmentedColormap untuk membuat colormap kustom
from matplotlib.colors import LinearSegmentedColormap

# Konfigurasi video vertikal dengan rasio 9:16
VIDEO_DURATION = 120  # Durasi video dalam detik (30 detik per model atom)
VIDEO_FPS = 30        # Frame rate video (frame per second)
TOTAL_FRAMES = VIDEO_DURATION * VIDEO_FPS  # Total frame video
VIDEO_WIDTH = 1080    # Lebar video dalam piksel (format vertikal)
VIDEO_HEIGHT = 1920   # Tinggi video dalam piksel (format vertikal)
OUTPUT_FILE = "atomic_models_animation.mp4"  # Nama file output
AUDIO_FILE = "music.mp3"  # File audio background
TEMP_AUDIO_FILE = "temp_audio.wav"  # File audio sementara

# Warna modern untuk visualisasi
COLORS = {
    'background': '#121212',  # Warna latar belakang gelap
    'text': '#FFFFFF',        # Warna teks putih
    'electron': '#4285F4',    # Warna elektron (biru)
    'proton': '#EA4335',      # Warna proton (merah)
    'neutron': '#34A853',     # Warna neutron (hijau)
    'nucleus': '#FBBC05',     # Warna nukleus (kuning)
    'orbit': '#9C27B0',       # Warna orbit (ungu)
    'highlight': '#00ACC1'    # Warna highlight (cyan)
}

# Fungsi untuk memproses file audio
def process_audio(audio_path, duration):
    """Mengolah file audio untuk disesuaikan dengan durasi video"""
    # Baca file audio MP3
    audio = AudioSegment.from_mp3(audio_path)
    
    # Potong audio jika lebih panjang dari durasi video
    if len(audio) > duration * 1000:  # Konversi detik ke milidetik
        audio = audio[:duration * 1000]
    
    # Ekspor ke format WAV sementara
    audio.export(TEMP_AUDIO_FILE, format="wav")
    return TEMP_AUDIO_FILE

# Proses file audio
audio_path = process_audio(AUDIO_FILE, VIDEO_DURATION)

# Membuat figure dengan orientasi vertikal (rasio 9:16)
fig = plt.figure(figsize=(10.8, 19.2), dpi=100)  # Ukuran dalam inci
ax = fig.add_subplot(111, projection='3d')  # Subplot 3D

# Set batas sumbu 3D
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)

# Menghilangkan sumbu
ax.set_axis_off()

# Set warna latar belakang
ax.set_facecolor(COLORS['background'])
fig.set_facecolor(COLORS['background'])

# Fungsi untuk membuat partikel 3D
def create_particle(x, y, z, radius, color, alpha=1.0):
    """Membuat partikel 3D berbentuk sphere"""
    # Buat grid untuk koordinat sphere
    u = np.linspace(0, 2 * np.pi, 20)  # Sudut azimuth
    v = np.linspace(0, np.pi, 20)      # Sudut polar
    
    # Hitung koordinat x, y, z untuk sphere
    x_p = x + radius * np.outer(np.cos(u), np.sin(v))
    y_p = y + radius * np.outer(np.sin(u), np.sin(v))
    z_p = z + radius * np.outer(np.ones(np.size(u)), np.cos(v))
    
    return x_p, y_p, z_p

# Fungsi untuk membuat orbit 3D
def create_orbit(radius, color, alpha=0.3, resolution=100):
    """Membuat orbit lingkaran 2D di ruang 3D"""
    theta = np.linspace(0, 2*np.pi, resolution)  # Sudut lingkaran
    x = radius * np.cos(theta)  # Koordinat x orbit
    y = radius * np.sin(theta)  # Koordinat y orbit
    z = np.zeros_like(x)        # Koordinat z orbit (datar)
    return x, y, z

# Teks judul animasi
title = ax.text(0, 0, 6, "", color=COLORS['text'], 
                ha='center', va='center', fontsize=36, fontweight='bold')

# Teks deskripsi model atom
description = ax.text(0, -4.5, 5, "", color=COLORS['text'], 
                     ha='center', va='center', fontsize=24, wrap=True)

# Fungsi update untuk animasi
def update(frame):
    """Update frame animasi untuk setiap model atom"""
    # Bersihkan axes setiap frame
    ax.clear()
    
    # Set ulang batas dan properti axes
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.set_axis_off()
    ax.set_facecolor(COLORS['background'])
    
    # Hitung progress animasi (0-1)
    progress = frame / TOTAL_FRAMES
    
    # Animasi rotasi kamera
    elev = 15 + 10 * np.sin(progress * np.pi/2)  # Elevasi kamera
    azim = progress * 360                         # Azimuth kamera
    ax.view_init(elev=elev, azim=azim)            # Set view kamera
    
    # Tentukan bagian animasi (4 bagian untuk 4 model atom)
    section = int(progress * 4)
    section_progress = (progress * 4) % 1  # Progress dalam bagian saat ini
    
    # Model Atom Dalton (1803)
    if section == 0:
        title.set_text("Dalton's Atomic Model (1803)")
        
        # Deskripsi model Dalton
        desc_text = "John Dalton proposed that:\n" \
                   "1. Matter is made of indivisible atoms\n" \
                   "2. Atoms of same element are identical\n" \
                   "3. Compounds form from atom combinations"
        animate_text(description, desc_text, section_progress * 3)
        
        # Visualisasi model Dalton sebagai bola pejal
        if section_progress > 0.2:
            # Buat beberapa atom berbeda (elemen berbeda)
            for i, (x, y, z, size, color) in enumerate([(-2, -1, 0, 0.8, COLORS['proton']),
                                                        (2, 1, 0, 1.0, COLORS['electron']),
                                                        (0, -2, 1, 0.6, COLORS['neutron'])]):
                x_p, y_p, z_p = create_particle(x, y, z, size, color)
                ax.plot_surface(x_p, y_p, z_p, color=color, alpha=min(1, (section_progress-0.2)*1.5))
                
                # Tambahkan label elemen
                if section_progress > 0.5:
                    ax.text(x, y, z + size + 0.3, f"Element {i+1}", 
                           color=COLORS['text'], ha='center', fontsize=12)
    
    # Model Atom Thomson (1904) - Plum Pudding
    elif section == 1:
        title.set_text("Thomson's Plum Pudding Model (1904)")
        
        # Deskripsi model Thomson
        desc_text = "J.J. Thomson discovered electrons and proposed:\n" \
                   "1. Atoms contain negatively charged electrons\n" \
                   "2. Electrons are embedded in a positively charged 'pudding'\n" \
                   "3. Overall atom is electrically neutral"
        animate_text(description, desc_text, section_progress * 3)
        
        # Visualisasi model Thomson
        if section_progress > 0.1:
            # Bola positif besar (pudding)
            x_p, y_p, z_p = create_particle(0, 0, 0, 3, COLORS['nucleus'], 0.3)
            ax.plot_surface(x_p, y_p, z_p, color=COLORS['nucleus'], alpha=0.3)
            
            # Elektron kecil tersebar acak (plum)
            if section_progress > 0.3:
                n_electrons = int(section_progress * 10)  # Jumlah elektron bertambah seiring waktu
                np.random.seed(42)  # Untuk konsistensi animasi
                
                for _ in range(n_electrons):
                    # Posisi acak dalam bola
                    theta = np.random.uniform(0, 2*np.pi)
                    phi = np.random.uniform(0, np.pi)
                    r = np.random.uniform(1, 2.8)
                    
                    # Koordinat elektron
                    x = r * np.sin(phi) * np.cos(theta)
                    y = r * np.sin(phi) * np.sin(theta)
                    z = r * np.cos(phi)
                    
                    # Gambar elektron
                    x_e, y_e, z_e = create_particle(x, y, z, 0.2, COLORS['electron'])
                    ax.plot_surface(x_e, y_e, z_e, color=COLORS['electron'])
    
    # Model Atom Rutherford (1911) - Nuklir
    elif section == 2:
        title.set_text("Rutherford's Nuclear Model (1911)")
        
        # Deskripsi model Rutherford
        desc_text = "Ernest Rutherford's gold foil experiment showed:\n" \
                   "1. Atom has a tiny, dense nucleus\n" \
                   "2. Electrons orbit the nucleus\n" \
                   "3. Most of atom is empty space"
        animate_text(description, desc_text, section_progress * 3)
        
        # Visualisasi model Rutherford
        if section_progress > 0.1:
            # Inti atom kecil
            x_n, y_n, z_n = create_particle(0, 0, 0, 0.5, COLORS['nucleus'])
            ax.plot_surface(x_n, y_n, z_n, color=COLORS['nucleus'])
            
            # Orbit elektron
            if section_progress > 0.3:
                n_orbits = 3  # Jumlah orbit
                for i in range(n_orbits):
                    radius = 1.5 + i * 1.0  # Radius orbit bertambah
                    x_o, y_o, z_o = create_orbit(radius, COLORS['orbit'], 0.2)
                    
                    # Gambar orbit secara bertahap
                    if section_progress > 0.3 + i*0.2:
                        ax.plot(x_o, y_o, z_o, color=COLORS['orbit'], alpha=0.5, linestyle='--')
                        
                        # Elektron yang mengorbit
                        if section_progress > 0.4 + i*0.2:
                            angle = (section_progress * 10 + i) * 2 * np.pi  # Sudut orbit
                            x_e = radius * np.cos(angle)
                            y_e = radius * np.sin(angle)
                            z_e = 0
                            
                            # Gambar elektron
                            x_el, y_el, z_el = create_particle(x_e, y_e, z_e, 0.2, COLORS['electron'])
                            ax.plot_surface(x_el, y_el, z_el, color=COLORS['electron'])
    
    # Model Atom Bohr (1913) - Tingkat Energi
    else:
        title.set_text("Bohr's Quantum Model (1913)")
        
        # Deskripsi model Bohr
        desc_text = "Niels Bohr introduced quantum theory to atoms:\n" \
                   "1. Electrons move in fixed orbits (energy levels)\n" \
                   "2. Orbits have quantized energy\n" \
                   "3. Light is emitted when electrons jump levels"
        animate_text(description, desc_text, min(1, section_progress * 3))
        
        # Visualisasi model Bohr
        if section_progress > 0.1:
            # Inti atom
            x_n, y_n, z_n = create_particle(0, 0, 0, 0.5, COLORS['nucleus'])
            ax.plot_surface(x_n, y_n, z_n, color=COLORS['nucleus'])
            
            # Orbit diskrit (tingkat energi)
            n_orbits = 3
            for i in range(n_orbits):
                radius = 1.0 + i * 1.5  # Radius orbit
                x_o, y_o, z_o = create_orbit(radius, COLORS['orbit'], 0.3)
                
                # Gambar orbit secara bertahap
                if section_progress > 0.2 + i*0.2:
                    ax.plot(x_o, y_o, z_o, color=COLORS['orbit'], alpha=0.7, linewidth=2)
                    
                    # Label tingkat energi
                    if section_progress > 0.3 + i*0.2:
                        ax.text(radius, 0, 0.3, f"n={i+1}", color=COLORS['text'], ha='center')
            
            # Animasi elektron berpindah tingkat energi
            if section_progress > 0.5:
                # Tentukan posisi elektron berdasarkan progress
                if section_progress < 0.7:
                    # Di tingkat dasar (n=1)
                    level = 0
                    angle = section_progress * 10 * 2 * np.pi
                elif section_progress < 0.8:
                    # Transisi ke tingkat n=2
                    level = (section_progress - 0.7) * 10
                    angle = 0
                else:
                    # Di tingkat n=2
                    level = 1
                    angle = (section_progress - 0.8) * 5 * 2 * np.pi
                
                # Hitung posisi elektron
                radius = 1.0 + level * 1.5
                x_e = radius * np.cos(angle)
                y_e = radius * np.sin(angle)
                z_e = 0
                
                # Gambar elektron
                x_el, y_el, z_el = create_particle(x_e, y_e, z_e, 0.2, COLORS['electron'])
                ax.plot_surface(x_el, y_el, z_el, color=COLORS['electron'])
                
                # Animasi emisi foton saat transisi
                if 0.7 < section_progress < 0.75:
                    ax.plot([0, 0], [0, 0], [0, 3], color=COLORS['highlight'], 
                           linewidth=3, alpha=(section_progress-0.7)*5)
                    ax.text(0, 0, 3.5, "Photon emitted", color=COLORS['highlight'], 
                           ha='center', fontsize=16)
    
    return []  # Return empty list karena tidak menggunakan blit

# Fungsi untuk animasi teks bertahap
def animate_text(text_obj, full_text, progress):
    """Animasi teks muncul bertahap"""
    chars_to_show = int(progress * len(full_text))  # Hitung jumlah karakter yang ditampilkan
    partial_text = full_text[:chars_to_show]        # Ambil sebagian teks
    text_obj.set_text(partial_text)                 # Set teks pada objek

# Buat animasi dengan FuncAnimation
ani = FuncAnimation(fig, update, frames=TOTAL_FRAMES, 
                   interval=1000/VIDEO_FPS, blit=False)

# Simpan animasi sementara tanpa audio
temp_video = "temp_video.mp4"

# Konfigurasi writer untuk video
writer = animation.FFMpegWriter(fps=VIDEO_FPS, bitrate=10000, 
                               extra_args=['-preset', 'slow', '-crf', '18'])

# Simpan animasi ke file sementara
ani.save(temp_video, writer=writer, dpi=100)

# Fungsi untuk menggabungkan video dan audio
def combine_video_audio(video_path, audio_path, output_path):
    """Menggabungkan video dan audio menggunakan FFmpeg"""
    cmd = [
        'ffmpeg',
        '-y',  # Overwrite output file tanpa prompt
        '-i', video_path,  # Input video
        '-i', audio_path,  # Input audio
        '-c:v', 'libx264',  # Codec video
        '-c:a', 'aac',      # Codec audio
        '-strict', 'experimental',
        '-map', '0:v:0',    # Ambil video dari input pertama
        '-map', '1:a:0',    # Ambil audio dari input kedua
        '-shortest',        # Sesuaikan durasi dengan yang terpendek
        '-movflags', '+faststart',  # Optimasi streaming
        '-pix_fmt', 'yuv420p',     # Format pixel
        output_path         # Output file
    ]
    subprocess.run(cmd)  # Jalankan perintah FFmpeg

# Gabungkan video dan audio
combine_video_audio(temp_video, TEMP_AUDIO_FILE, OUTPUT_FILE)

# Bersihkan file sementara
os.remove(temp_video)
os.remove(TEMP_AUDIO_FILE)

# Cetak pesan sukses
print(f"Atomic models animation complete! Saved to {OUTPUT_FILE}")