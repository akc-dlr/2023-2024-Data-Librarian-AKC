import streamlit as st
import pyterrier as pt
import pickle

if not pt.started():
	pt.init()

def init():

	index = pt.IndexFactory.of("/home/anni/Desktop/2023-2024-Data_Librarian_Ann-Kathrin_Christann/Modul_2/Modul_2-1/df_index/data.properties")
	st.session_state["engine"] = pt.BatchRetrieve(index, wmodel="TF_IDF")
	st.session_state["data"] = pickle.load(open("/home/anni/Schreibtisch/2023-2024-Data_Librarian_Ann-Kathrin_Christann/Modul_2/Modul_2-1/df_publications.pkl", "rb"))

# years = [str(year) for year in range(1908, 2023)]
# def search(query, years):

def search(query):

	res = st.session_state["engine"].search(query)
	fields_to_show = ['text', 'source', 'authors', 'searchterm', 'publication_year']

	for _, row in res.iterrows():
		score = round(row['score'], 2)
		entry = st.session_state["data"][st.session_state["data"]['docno'] == row['docno']].iloc[0]

		for field in fields_to_show:
			if 	field == "text":
				st.title(entry[field])
			else:
				st.write(f"{field.capitalize()}: \t {entry[field]}")

		st.write(f"Relevanz: {score}")
		st.divider()

if not "engine" in st.session_state:
	init()

query = st.sidebar.text_input("Search", help="This is a tooltip", on_change=search)

# st.sidebar.text_input("Clicksearch", on_change=search(query))
# st.sidebar.button("Go!", on_click=search, args=(query,))
# st.sidebar.text_input("Clicksearch", on_change=search(query))
st.sidebar.button("Go!", on_click=search, args=())

sort_option = st.sidebar.selectbox(
    "Sort results by",
    ["Relevance", "Publication Year"],
    index=0
)
