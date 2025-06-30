import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Medium TOC Generator", layout="wide")
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)
# st.title("Medium TOC Generator")
st.markdown("<h1 style='text-align: center;'>Medium Table of Contents Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

# left_col, right_col = st.columns([2,3])
left_spacer, left_col, right_col, right_spacer = st.columns([1,4,5,1])

with left_col:
    url = st.text_input("Enter Medium article URL")

    def extract_headings(html):
        soup = BeautifulSoup(html, 'html.parser')
        headings = []
        for h in soup.find_all(['h1', 'h2', 'h3', 'h4']):
            id_attr = h.get('id')
            text = h.get_text(strip=True)
            if id_attr and text:
                level = int(h.name[1])
                headings.append((level, text, id_attr))
        return headings

    if url:
        try:
            res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            res.raise_for_status()
            headings = extract_headings(res.text)

            if not headings:
                st.warning("No headings with ID attributes found.")
            else:
                toc_lines = []
                for level, text, id_attr in headings:
                    indent = '  ' * (level - 1)
                    toc_lines.append(f"{indent}- {text}#{id_attr}")
                st.subheader("Table of Contents")
                st.code("  \n".join(toc_lines), language="text")
        except Exception as e:
            st.error(f"Error fetching article: {e}")

with right_col:
    st.markdown("### About")
    st.markdown("Generate a Table of Contents and the necessary link ids for articles on Medium. Supports two levels of indentation.")
    st.markdown("This tool is based on the approach described in [this article](https://medium.com/@AllienWorks/creating-table-of-contents-for-medium-articles-5f9087377b82).")
    st.markdown("### Instructions")
    st.markdown("""
1. Paste your Medium article URL in the box on the left and press Enter.
2. The Table of Contents will appear. It contains all the headings in the article, each followed by its id (for example: `#1234ab`).\n
    *Note: The entry should be the title (and subtitle if there is one in the article) - no need to copy-paste this.*
3. Copy the list and paste it directly into your Medium draft at the top.
4. In the Medium draft, for each entry in the TOC:
    - Use `Ctrl+X`/`Cmd+X` to cut the id, including the `#` character.
    - Highlight each entry, and either press the link icon in the menu or press `Ctrl+K`/`Cmd+K` to bring up the link pasting field, and press `Ctrl+V`/`Cmd+V` to paste the link.
5. Optionally, add the text "Table of Contents" above the list of sections.
6. Publish the draft and try out the TOC.
""")
