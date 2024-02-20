import streamlit as st
import pyterrier as pt
import pickle

if not pt.started():
	pt.init()

def init():

	index = pt.IndexFactory.of("/home/anni/Desktop/2023-2024-Data_Librarian_Ann-Kathrin_Christann/Modul_2/Modul_2-1/df_index/data.properties")
	st.session_state["engine"] = pt.BatchRetrieve(index, wmodel="TF_IDF")
	st.session_state["data"] = pickle.load(open("/home/anni/Schreibtisch/2023-2024-Data_Librarian_Ann-Kathrin_Christann/Modul_2/Modul_2-1/df_publications.pkl", "rb"))

sort_option = st.sidebar.selectbox(
    "Sort results by",
    ["Relevance", "Publication Year"],
    index=0
)


def search(query):

        res = st.session_state["engine"].search(query)
        fields_to_show = ['text', 'source', 'authors', 'searchterm', 'publication_year']
if sort_option == "Publication Year":
        # Sort the DataFrame by the 'publication_year' in the entry data
        # This assumes you can access 'publication_year' directly or you adjust accordingly
        res['publication_year'] = res['docno'].apply(lambda x: st.session_state["data"][st.session_state["data"]['docno'] == x].iloc[0]['publication_year'])
        sorted_res = res.sort_values(by='publication_year', ascending=True)
else:  # Default to sorting by relevance score
        sorted_res = res.sort_values(by='score', ascending=False)

def display_results(sorted_res):
    fields_to_show = ['text', 'source', 'authors', 'searchterm', 'publication_year']

    for _, row in sorted_res.iterrows():
        score = round(row['score'], 2)
        entry = st.session_state["data"][st.session_state["data"]['docno'] == row['docno']].iloc[0]

        for field in fields_to_show:
            if field == "text":
                st.title(entry[field])
            else:
                st.write(f"{field.capitalize()}: \t {entry[field]}")

        st.write(f"Relevanz: {score}")
        st.divider()

if not "engine" in st.session_state:
	init()

query = st.sidebar.text_input("Searchterm", help="This is a tooltip")
# st.text_input(on_change=search, args=(query,))
st.sidebar.button("Go!", on_click=search)     #args=(query,))


