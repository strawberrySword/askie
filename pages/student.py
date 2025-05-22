import streamlit as st

st.set_page_config( 
    page_title="Student | Askie",
    page_icon="./assets/brand/logo.png",
    layout="wide"
)

# Check access
if "role" not in st.session_state or st.session_state.role != "student":
    st.error("Access denied. Please log in as a student.")
    st.stop()

# st.title("🎓 Student Page")
# st.write(f"Welcome, **{st.session_state.name}**!")

# if st.button("Logout"):
#     st.session_state.clear()
#     st.switch_page("main.py")


# Custom CSS for the gallery
st.markdown(
    """
    <style>
    .gallery-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 1rem;
    }
    .gallery-item {
        position: relative;
        width: 32%;                 /* Three items per row with small gaps */
        overflow: hidden;
        border-radius: 0.5rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        cursor: pointer;
        text-align: center;
    }
    .gallery-item img {
        width: 100%;
        height: auto;
        display: block;
        transition: transform 0.3s ease;
    }
    .gallery-item:hover img {
        transform: scale(1.05);
    }
    .overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        color: #FFF;
        opacity: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        font-weight: 500;
        transition: opacity 0.3s ease;
    }
    .gallery-item:hover .overlay {
        opacity: 1;
    }
    /* Make sure links don’t inherit unwanted styling */
    .gallery-item a {
        color: inherit;
        text-decoration: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎨 Streamlit Gallery Demo")
st.write("Hover over each image to see the overlay text. Click anywhere on the card to follow the link.")

# Sample data for 2 rows (6 items). Each dict has: image URL, overlay text, and target URL.
items = [
    {
        "img_url": "bob.png",
        "title": "Item 1",
        "link": "https://example.com/1",
    },
    {
        "img_url": "pat.png",
        "title": "Item 2",
        "link": "https://example.com/2",
    },
    {
        "img_url": "squid.jpg",
        "title": "Item 3",
        "link": "https://example.com/3",
    },
    {
        "img_url": "krabs.png",
        "title": "Item 4",
        "link": "https://example.com/4",
    },
    {
        "img_url": "bob.png",
        "title": "Item 5",
        "link": "https://example.com/5",
    },
    {
        "img_url": "squid.jpg",
        "title": "Item 6",
        "link": "https://example.com/6",
    },
]

# Break into rows of 3
rows = [items[i : i + 3] for i in range(0, len(items), 3)]

# Render each row
for row in rows:
    cols = st.columns(3, gap="small")
    for col, item in zip(cols, row):
        with col:
            st.image(item["img_url"], caption=item["title"], use_container_width=True)