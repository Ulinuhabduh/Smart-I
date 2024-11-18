import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import os

# Mengatur layout menjadi "wide" dan mengubah nama tab
st.set_page_config(page_title="Smart-I: Forest City Monitoring", layout="wide")

# Menentukan jalur file logo
smart_i_logo_path = "Images/logo_gabungan.png"  
statistik_folder = "Images/statistik"  

st.image(smart_i_logo_path)

# Tanda panah besar mengarah ke bawah
st.markdown(
    """
    <div style="text-align: center; font-size: 150px; color: #800080; margin: -250px 0 20px 0;">
        &#x2193; <!-- Kode untuk panah besar ke bawah -->
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        border: 2px dashed #800080;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    ">
        <h1 style="text-decoration-line: underline; color: #75F442;">Smart-I</h1>
        <div style="font-size: 20px; color: #75F442; margin-bottom: 10px;">
            SEGMENT ANYTHING MODEL FOR RESILIENT AND SUSTAINABLE FOREST CITY IN IKN
        </div>
        <div style="font-size: 16px; color: white;">
            SMART-I adalah model segmentasi berbasis kecerdasan buatan (AI) yang dirancang untuk memantau pembangunan IKN Nusantara secara akurat dan real-time dalam mendukung konsep Forest City. Dengan menggunakan Segment Anything Model (SAM), SMART-I mampu mendeteksi perubahan tutupan lahan dari citra satelit secara efisien, sehingga menjaga keseimbangan antara pembangunan dan kelestarian ekosistem hutan. Sistem ini terintegrasi dengan WebGIS interaktif, memungkinkan visualisasi data yang mudah dipahami dalam dashboard untuk mendukung pengambilan keputusan adaptif. Pendekatan ini diharapkan dapat mewujudkan pembangunan kota berkelanjutan di Indonesia dan menjadi inspirasi global.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("<hr>", unsafe_allow_html=True)

# Menentukan lokasi awal peta (misalnya di Indonesia)
initial_location = [-2.548926, 118.0148634] 
zoom_level = 5

# Menentukan folder tempat shapefile berada
new_shapefiles_folder = 'SAM SEMUA/'

# Mendapatkan daftar file shapefile
new_shapefiles = [f for f in os.listdir(new_shapefiles_folder) if f.endswith('.shp')]

# Inisialisasi session state untuk indeks shapefile
if 'shapefile_index' not in st.session_state:
    st.session_state['shapefile_index'] = 1

# Menampilkan tombol navigasi
col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    st.write("")

with col2:
    col5, col6 = st.columns([1, 1])
    with col5:
        previous = st.button("Previous", use_container_width=True)
    with col6:
        next = st.button("Next", use_container_width=True)

with col3:
    st.write("")

if previous:
    st.session_state['shapefile_index'] -= 1
    if st.session_state['shapefile_index'] < 1:
        st.session_state['shapefile_index'] = len(new_shapefiles)
elif next:
    st.session_state['shapefile_index'] += 1
    if st.session_state['shapefile_index'] > len(new_shapefiles):
        st.session_state['shapefile_index'] = 1

# Menampilkan indeks shapefile saat ini
shapefile_index = st.session_state['shapefile_index']

# Membuat layout dengan dua kolom untuk informasi shapefile dan peta
col_info, col_map = st.columns([2, 3])

with col_info:
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="border: 2px solid #800080; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
            <h3 style="text-align: center;">Informasi Segmentasi</h3>
        """,
        unsafe_allow_html=True
    )

    # Menampilkan gambar statistik berdasarkan indeks
    statistik_image_path = os.path.join(statistik_folder, f"{shapefile_index}.png")
    if os.path.exists(statistik_image_path):
        st.image(statistik_image_path, use_column_width=True)
    else:
        st.write("Gambar statistik tidak tersedia.")

    selected_file_name = new_shapefiles[shapefile_index - 1]
    shapefile_path = os.path.join(new_shapefiles_folder, selected_file_name)
    gdf = gpd.read_file(shapefile_path)

    # Mendapatkan pusat dari bounding box shapefile
    center = gdf.geometry.unary_union.centroid.coords[0]

    # Menampilkan informasi pusat koordinat shapefile
    st.write(f"**Koordinat Pusat:** {center}")

    # Menampilkan informasi metadata
    st.write("### Referensi Spasial:")
    st.write(f"- **Proyeksi : Universal Transverse Mercator**")
    st.write(f"- **Datum : WGS 1984**")
    st.write(f"- **Zona : 50S**")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col_map:
    # Membuat peta dasar dengan Leafmap
    m = leafmap.Map(center=initial_location, zoom=zoom_level)
    m.add_basemap("Esri.WorldImagery")


    # Menambahkan data shapefile yang dipilih ke peta
    def style_function(feature):
        gridcode = feature['properties'].get('gridcode', 0)
        return {
            'fillColor': '#ff0000',
            'color': '#808080',
            'weight': 2,
            'fillOpacity': 0.5
        }

    m.add_gdf(gdf, layer_name=selected_file_name, style_function=style_function)

    # Menampilkan peta di Streamlit
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



# Footer aplikasi
st.write("<hr>", unsafe_allow_html=True)
st.write("<div style='text-align: center;'>Dibuat oleh Tim Ababil 🕊️</div>", unsafe_allow_html=True)

