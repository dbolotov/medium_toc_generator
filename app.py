import streamlit as st
import requests
from bs4 import BeautifulSoup

def extract_headings(html):
    soup = BeautifulSoup(html, "html.parser")
    headings = []
    for h in soup.find_all(["h1", "h2", "h3", "h4"]):
        id_attr = h.get("id")
        text = h.get_text(strip=True)
        if id_attr and text:
            level = int(h.name[1])
            headings.append((level, text, id_attr))
    return headings


with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(page_title="Medium TOC Generator", layout="wide")


left_spacer, left_col, c_spacer, right_col, right_spacer = st.columns([1, 5, 0.3, 4, 1])

with left_col:

    st.markdown('<div class="boxed-title">Medium Table of Contents Generator</div>', unsafe_allow_html=True)

    input_mode = st.radio("Choose input method", ["URL", "HTML"])



    html = None

    if input_mode == "URL":
        url = st.text_input("Medium article URL", placeholder="https://medium.com/your-article")

        if url:
            try:
                res = requests.get(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0 Safari/537.36"
                    },
                )
                res.raise_for_status()
                html = res.text
            except Exception as e:
                st.error(f"Error fetching article: {e}")
    else:
        html = st.text_area(
            "Medium article HTML",
            height=300,
            placeholder="Paste the full HTML source here",
        )

    if html:
        headings = extract_headings(html)

        if not headings:
            st.warning("No headings with ID attributes found.")
        else:
            toc_lines = []
            for level, text, id_attr in headings:
                indent = "  " * (level - 1)
                toc_lines.append(f"{indent}- {text}#{id_attr}")
            st.subheader("Table of Contents")
            st.code("  \n".join(toc_lines), language="text")

with right_col:
    st.markdown("### About")
    st.markdown(

        "Generate a Table of Contents and the necessary link ids for your articles on Medium.com.\n\n"
        
        "**Why the need for this app?** Medium doesn’t support automatic TOC generation when creating articles.\n"
    )

    st.markdown("### Instructions")
    st.markdown(
        """
    1. Choose input method (**URL** or **HTML**), paste the link or HTML in the box, and press `Enter` (or `Ctrl+Enter` for HTML).\n
        *Note: Try URL first. If the TOC looks incomplete, switch to 'Paste HTML'. Some Medium articles load content dynamically, so the URL method may miss sections.*\n
        *To get the full HTML: Right-click on the Medium page, choose **"View Page Source"**, select all and copy, paste it here.*\n
    2. The Table of Contents will appear. It contains all the headings in the article, each followed by its id (for example: `#1234ab`).\n
        *Note: The first entry should be the title (and subtitle if there is one in the article) - no need to copy-paste this.*
    3. Copy the list and paste it directly into your Medium draft at the top.
    4. In the Medium draft, for each entry in the TOC:
        - Use `Ctrl+X`/`Cmd+X` to cut the id, including the `#` character.
        - Highlight each entry, and either press the link icon in the menu or press `Ctrl+K`/`Cmd+K` to bring up the link pasting field, and press `Ctrl+V`/`Cmd+V` to paste the link.
    5. Optionally, add the text "Table of Contents" above the list of sections.
    6. Publish the draft and try out the TOC.
"""
    )
