import streamlit as st
import leafmap.foliumap as leafmap
import geopandas as gpd
import os

# Mengatur layout menjadi "wide" dan mengubah nama tab
st.set_page_config(page_title="Smart-I: Forest City Monitoring", layout="wide")

# Menambahkan CSS untuk background dark
st.markdown(
    """
    <style>
    /* Mengubah warna latar belakang */
    body {
        background-color: #121212; /* Warna latar belakang dark */
    }
    /* Mengubah warna teks default */
    .stText, .stMarkdown, .stButton > button {
        color: #e0e0e0; /* Warna teks light agar mudah terbaca di background dark */
    }
    /* Styling khusus untuk elemen-elemen tertentu */
    .css-18e3th9 { /* Sesuaikan dengan class yang sesuai untuk elemen seperti header */
        color: #75F442 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Menentukan jalur file logo
smart_i_logo_path = "Images/logo_gabungan.png"  # Ganti dengan jalur file logo Smart-I
other_logo_path = "Images/logo gg gemink.png"  # Ganti dengan jalur file logo lainnya
statistik_folder = "Images/statistik"  

st.image(smart_i_logo_path)

# Tanda panah besar mengarah ke bawah
# Menambahkan panah mengarah ke bawah
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
initial_location = [-2.548926, 118.0148634]  # Koordinat pusat Indonesia
zoom_level = 5

# Menentukan folder tempat shapefile berada
shapefile_folder = 'Supervised/'
new_shapefiles_folder = 'SAM SEMUA/'

# Mendapatkan daftar file shapefile
shapefiles = [f for f in os.listdir(shapefile_folder) if f.endswith('.shp')]
new_shapefiles = [f for f in os.listdir(new_shapefiles_folder) if f.endswith('.shp')]

# Inisialisasi session state untuk indeks shapefile
if 'shapefile_index' not in st.session_state:
    st.session_state['shapefile_index'] = 1

# Menampilkan tombol navigasi dengan warna biru menggunakan CSS
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #800080;
        color: white;
        padding: 10px 10px;
        border: none;
        border-radius: 4px;
        margin: 0 auto;
        display: block;
        font-size: 10px;
    }
    .center-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    st.write("")

with col2:
    col5, col6 = st.columns([1,1])
    with col5:
        previous = st.button("Previous", use_container_width=True)
    with col6:
        next = st.button("Next", use_container_width=True)

with col3:
    st.write("")

if previous:
    st.session_state['shapefile_index'] -= 1
    if st.session_state['shapefile_index'] < 1:
        st.session_state['shapefile_index'] = len(shapefiles)
elif next:
    st.session_state['shapefile_index'] += 1
    if st.session_state['shapefile_index'] > len(shapefiles):
        st.session_state['shapefile_index'] = 1

# Menampilkan indeks shapefile saat ini
shapefile_index = st.session_state['shapefile_index']

# Membuat layout dengan dua kolom untuk informasi shapefile dan peta
col_info, col_map = st.columns([2, 3])

with col_info:

    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    # Menggunakan HTML dan CSS untuk menampilkan border di sekitar informasi
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

    selected_file_name = shapefiles[shapefile_index - 1]
    shapefile_path = os.path.join(shapefile_folder, selected_file_name)
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

    # Fungsi untuk menentukan warna berdasarkan nilai gridcode
    def get_color(gridcode):
        color_map = {
            1: "#FF0000",  # Merah
            2: "#00FF00",  # Hijau
            3: "#0000FF",  # Biru
            4: "#FFFF00",  # Kuning
            5: "#FFA500",  # Oranye
        }
        return color_map.get(gridcode, "#FF0000")  # Default warna abu-abu jika tidak ada di peta warna

    # Menambahkan data shapefile yang dipilih ke peta dengan warna berdasarkan gridcode
    def style_function(feature):
        gridcode = feature['properties'].get('gridcode', 0)
        color = get_color(gridcode)
        return {
            'fillColor': color,
            'color': color,
            'weight': 2,
            'fillOpacity': 0.5
        }

    m.add_gdf(gdf, layer_name=selected_file_name, style_function=style_function)

    # Menambahkan shapefile hasil segmentasi jika checkbox dipilih
    show_segmented = st.checkbox("Tampilkan Segmentasi")
    # Menambahkan data shapefile hasil segmentasi ke peta dengan border berwarna ungu
    def segment_style_function(feature):
            gridcode = feature['properties'].get('gridcode', 0)
            color = get_color(gridcode)
            return {
                'fillColor': color,
                'color': "#800080",  # Warna border ungu untuk hasil segmentasi
                'weight': 2,  # Ketebalan border
                'fillOpacity': 1
            }
    if show_segmented and shapefile_index <= len(new_shapefiles):
        # Cek apakah ada segmentasi dengan nama yang sama
        selected_file_name = shapefiles[shapefile_index - 1]
        segmented_file_name = selected_file_name  # Sesuaikan nama segmentasi dengan nama file asli

        # Pastikan ada segmentasi dengan nama yang sama di folder segmentasi
        segmented_shapefile_path = os.path.join(new_shapefiles_folder, segmented_file_name)
        if os.path.exists(segmented_shapefile_path):
            segmented_gdf = gpd.read_file(segmented_shapefile_path)
            # Menambahkan data shapefile hasil segmentasi ke peta dengan border berwarna ungu
            m.add_gdf(segmented_gdf, layer_name=segmented_file_name, style_function=segment_style_function)
        else:
            st.write("Tidak ada segmentasi yang cocok.")

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

