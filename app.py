import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import pandas as pd
import os
from pyproj import CRS, Transformer
import matplotlib.pyplot as plt

# Mengatur layout menjadi "wide" dan mengubah nama tab
st.set_page_config(page_title="SMART-I: Forest City Monitoring", layout="wide")

# Menentukan jalur file logo dan data statistik
smart_i_logo_path = "Images/logo_gabungan.png"
statistik_file_path = "Statistik.xlsx"  # File data statistik dari unggahan
new_shapefiles_folder = "SAM SEMUA/"  # Folder shapefile

# Menampilkan logo
st.image(smart_i_logo_path)

# Header aplikasi
st.markdown("""
<div style="text-align: center; font-size: 150px; color: #800080; margin: -250px 0 20px 0;">
    &#x2193; <!-- Tanda panah -->
</div>
<div style="
    border: 2px dashed #800080;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
">
    <h1 style="text-decoration-line: underline; color: #75F442;">SMART-I</h1>
    <div style="font-size: 20px; color: #75F442; margin-bottom: 10px;">
        SEGMENT ANYTHING MODEL FOR RESILIENT AND SUSTAINABLE FOREST CITY IN IKN
    </div>
    <div style="font-size: 16px; color: white;">
        SMART-I adalah model segmentasi berbasis kecerdasan buatan (AI) yang dirancang untuk memantau pembangunan IKN Nusantara secara akurat dan real-time. Dengan SAM (Segment Anything Model), SMART-I mendukung keseimbangan pembangunan dengan kelestarian ekosistem hutan melalui analisis tutupan lahan.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("<hr>", unsafe_allow_html=True)

zoom_level = 5

# Membaca daftar shapefiles dan mengurutkannya berdasarkan angka di nama file
new_shapefiles = sorted(
    [f for f in os.listdir(new_shapefiles_folder) if f.endswith('.shp')],
    key=lambda x: int(x.split('.')[0])  # Mengurutkan berdasarkan angka sebelum .shp
)

# Inisialisasi session state untuk indeks shapefile dan status tombol
if 'shapefile_index' not in st.session_state:
    st.session_state['shapefile_index'] = 0
if 'show_segmentation' not in st.session_state:
    st.session_state['show_segmentation'] = False

# Navigasi segmen dengan tombol Previous dan Next
col1, col2, col3 = st.columns([3, 1, 3])
with col2:
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        previous = st.button("Previous", use_container_width=True)
    with col_next:
        next = st.button("Next", use_container_width=True)

# Mengatur navigasi Previous dan Next
if previous or next:
    st.session_state['show_segmentation'] = False  # Matikan tombol jika Next atau Previous ditekan
    if previous:
        st.session_state['shapefile_index'] -= 1
        if st.session_state['shapefile_index'] < 0:
            st.session_state['shapefile_index'] = len(new_shapefiles) - 1  # Kembali ke akhir jika kurang dari 0
    if next:
        st.session_state['shapefile_index'] += 1
        if st.session_state['shapefile_index'] >= len(new_shapefiles):
            st.session_state['shapefile_index'] = 0  # Kembali ke awal jika melebihi jumlah file


# Mendapatkan file shapefile yang dipilih berdasarkan indeks
shapefile_index = st.session_state['shapefile_index']
selected_file_name = new_shapefiles[shapefile_index]
shapefile_path = os.path.join(new_shapefiles_folder, selected_file_name)

# Membuat layout dengan dua kolom untuk informasi shapefile dan peta
col_info, col_map = st.columns([2, 3])

with col_info:
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown("""
    <div style="border: 2px solid #800080; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
        <h3 style="text-align: center;">Informasi Segmentasi</h3>
    """, unsafe_allow_html=True)

    # Membaca shapefile
    gdf = gpd.read_file(shapefile_path)
    source_crs = gdf.crs
    target_crs = CRS.from_epsg(4326)
    transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)
    # Pastikan geometri valid dan tidak kosong
    if gdf.geometry.is_empty.any():
        st.error("Shapefile tidak memiliki geometri yang valid atau kosong.")
    else:
        union_geometry = gdf.geometry.unary_union
        if union_geometry.is_empty:
            st.error("Shapefile memiliki geometri gabungan yang kosong.")
        else:
            # Tangani GeometryCollection atau MultiPolygon
            if union_geometry.geom_type == "GeometryCollection":
                union_geometry = [geom for geom in union_geometry if geom.is_valid][0]
            center = union_geometry.centroid.coords[0]

            # Transform koordinat pusat ke WGS84
            lon, lat = transformer.transform(center[0], center[1])

    # Membaca data statistik
    if os.path.exists(statistik_file_path):
        statistik_data = pd.read_excel(statistik_file_path)

        # Filter data berdasarkan shapefile yang dipilih
        segmen_data = statistik_data[statistik_data["Segmen"] == selected_file_name]

        # Menampilkan statistik
        st.write("### Statistik Segmen")
        if not segmen_data.empty:

            # Visualisasi Statistik Horizontal
            plt.style.use('dark_background')  # Mengatur tema menjadi gelap
            fig, axes = plt.subplots(3, 1, figsize=(8, 5))

            # Plot Jumlah Fitur (Horizontal)
            axes[0].barh(["Ground Truth", "SAM"], [segmen_data["Ground Truth (Fitur)"].iloc[0], segmen_data["SAM (Fitur)"].iloc[0]],
                        color=["orange", "green"])
            axes[0].set_title("Jumlah Fitur", loc='center', fontsize=12, fontweight='bold', color='white')
            axes[0].set_xlabel("Jumlah", color='white', fontweight='bold')
            axes[0].set_xlim(0, max(segmen_data["Ground Truth (Fitur)"].iloc[0], segmen_data["SAM (Fitur)"].iloc[0]) * 1.2)

            # Plot Luas Fitur (Horizontal)
            axes[1].barh(["Ground Truth", "SAM"], [segmen_data["Ground Truth (Luas)"].iloc[0], segmen_data["SAM (Luas)"].iloc[0]],
                        color=["orange", "green"])
            axes[1].set_title("Luas Fitur (Ha)", loc='center', fontsize=12, color='white', fontweight='bold')
            axes[1].set_xlabel("Luas (Ha)", fontweight='bold', color='white')
            axes[1].set_xlim(0, max(segmen_data["Ground Truth (Luas)"].iloc[0], segmen_data["SAM (Luas)"].iloc[0]) * 1.2)

            # Plot IoU (Horizontal)
            axes[2].barh(["Sukses", "Error"], [segmen_data["IOU (%)"].iloc[0], 100 - segmen_data["IOU (%)"].iloc[0]],
                        color=["green", "orange"])
            axes[2].set_title("IoU (%)", loc='center', fontsize=12, fontweight='bold', color='white')
            axes[2].set_xlabel("Persentase", fontweight='bold', color='white')
            axes[2].set_xlim(0, 100)

            # Menyesuaikan tampilan
            for ax in axes:
                ax.tick_params(axis='x', colors='white')
                ax.tick_params(axis='y', colors='white')
                ax.spines['bottom'].set_color('white')
                ax.spines['left'].set_color('white')
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)

            fig.tight_layout()
            st.pyplot(fig)

        else:
            st.warning("Data statistik untuk segmen ini tidak ditemukan.")
    else:
        st.error("File data statistik tidak ditemukan.")
    
    # Menampilkan metadata
    st.write("### Referensi Spasial:")
    st.write(f"**Koordinat Pusat :** ({lat:.5f}, {lon:.5f})")
    st.write(f"- **Proyeksi : Universal Transverse Mercator**")
    st.write(f"- **Datum : WGS 1984**")
    st.write(f"- **Zona : 50S**")
    st.markdown('</div>', unsafe_allow_html=True)

with col_map:
    # Tombol untuk menampilkan segmentasi
    show_segmentation = st.checkbox("Tampilkan Segmentasi pada Peta", value=st.session_state['show_segmentation'])
    st.session_state['show_segmentation'] = show_segmentation  # Perbarui status tombol

    # Membuat peta menggunakan Leafmap
    m = leafmap.Map(center=[lat, lon], zoom=zoom_level)
    m.add_basemap("Esri.WorldImagery")

    # Menambahkan shapefile ke peta
    def style_function(feature):
        if show_segmentation:
            # Jika segmentasi diaktifkan
            return {
                'fillColor': '#ff0000',
                'color': '#808080',  # Warna batas
                'weight': 2,         # Ketebalan batas
                'fillOpacity': 0.5   # Transparansi isian
            }
        else:
            # Jika segmentasi dimatikan
            return {
                'fillColor': 'none',  # Tidak ada warna isian
                'color': '#808080',   # Tetap menampilkan garis batas
                'weight': 0,          # Ketebalan batas
                'fillOpacity': 0      # Isian transparan
            }

    # Tambahkan GeoDataFrame ke peta
    m.add_gdf(gdf, layer_name=selected_file_name, style_function=style_function)
    m.to_streamlit(width=800, height=600)

# Menambahkan bagian About Author sebelum footer
st.write("<hr>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #75F442'>About the Authors</h2>", unsafe_allow_html=True)

# Menentukan jalur folder untuk gambar penulis
authors_folder = "Images/authors"

# Membuat layout dengan tiga kolom untuk informasi setiap penulis
col1, col2, col3 = st.columns(3)

with col1:
    author1_image_path = os.path.join(authors_folder, "1.png")  # Pastikan file berada di jalur relatif ini
    st.image(author1_image_path, use_column_width=True)
    st.markdown(
        """
        <div style="display: block; text-align: center;">
            <p style='color: #75F442; font-size: 1.5rem'>Mohammad Rifqi Alfarizi</p>
            <div style="display: inline-flex; gap: 10px;">
                <a href="https://www.linkedin.com/in/mohammad-rifqi-alfarizi-183517315?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" width="30" style="margin-bottom: 10px;">
                </a>
                <a href="https://www.instagram.com/rifqialfarizi" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30" style="margin-bottom: 10px;">
                </a>
            </div>
            <p>Mahasiswa S1 Teknik Geomatika ITS angkatan 2022 dan anggota Tim ABABIL. Bertanggung jawab atas pembuatan sistem SMART-I yang menggunakan Segment Anything Model (SAM) berbasis Artificial Intelligence, serta melakukan analisis data spasial untuk menguji tingkat keandalan dan statistik data.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    author2_image_path = os.path.join(authors_folder, "2.png")  # Ganti dengan nama file gambar penulis 2
    st.image(author2_image_path, use_column_width=True)
    st.markdown(
        """
        <div style="display: block; text-align: center;">
            <p style='color: #75F442; font-size: 1.5rem'>Michael Aragorn Purba</p>
            <div style="display: inline-flex; gap: 10px;">
                <a href="https://www.linkedin.com/in/michael-aragorn-purba-a047b8208" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" width="30" style="margin-bottom: 10px;">
                </a>
                <a href="https://www.instagram.com/mich_aragorn?igsh=MWJtdmNrY2h4cGl2dw==" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30" style="margin-bottom: 10px;">
                </a>
            </div>
            <p>Mahasiswa S1 Teknik Geomatika ITS angkatan 2022 dan Ketua Tim ABABIL. Bertanggung jawab atas keberhasilan perancangan konsep inovasi, mengarahkan tim, membangun sistem SAM (Segment Anything Model), serta melakukan analisis data geospasial untuk sistem SMART-I.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    author3_image_path = os.path.join(authors_folder, "3.png")  # Ganti dengan nama file gambar penulis 3
    st.image(author3_image_path, use_column_width=True)
    st.markdown(
        """
        <div style="display: block; text-align: center;">
            <p style='color: #75F442; font-size: 1.5rem'>M Ulin Nuha Abduh</p>
            <div style="display: inline-flex; gap: 10px;">
                <a href="https://www.linkedin.com/in/mulinnuhaabduh/" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/e/e9/Linkedin_icon.svg" width="30" style="margin-bottom: 10px;">
                </a>
                <a href="https://www.instagram.com/ulinuhabduh_?igsh=ZDk3bmJzMzQweDRt" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="30" style="margin-bottom: 10px;">
                </a>
            </div>
            <p>Mahasiswa S1 Teknik Geofisika ITS angkatan 2022 dan anggota Tim ABABIL. Bertanggung jawab dalam membangun WebGIS yang mengintegrasikan data spasial hasil pengolahan SAM berbasis AI agar SMART-I dapat digunakan secara meluas.</p>
            
        </div>
        """,
        unsafe_allow_html=True
    )

# Footer
st.write("<hr>", unsafe_allow_html=True)
st.write("<div style='text-align: center;'>Dibuat oleh Tim Ababil 🕊️</div>", unsafe_allow_html=True)
