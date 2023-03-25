import os
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

st.title('DocxMatch')
st.subheader('Docx Similarity Analyzer')
uploaded_files = st.file_uploader('Upload two more word files:', type='docx', accept_multiple_files=True)
if uploaded_files:
    texts = []
    for uploaded_file in uploaded_files:
        document = Document(uploaded_file)
        text = '\n'.join([paragraph.text for paragraph in document.paragraphs])
        texts.append(text)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    threshold = 0.9
    similar_files = []
    from sklearn.metrics.pairwise import pairwise_distances
    identity_matrix = 1 - pairwise_distances(X.toarray(), metric='cosine')
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            if identity_matrix[i,j] > threshold:
                similar_files.append((uploaded_files[i].name, uploaded_files[j].name))
    if similar_files:
        st.write(f"The following pairs of files have identity above {threshold*100}%:")
        for file1, file2 in similar_files:
            st.write(f"{file1} and {file2}")
    else:
        st.write(f"No pairs of files have identity above {threshold*100}%.")
    import pandas as pd
    similarity_matrix = cosine_similarity(X)
    fig, ax = plt.subplots()
    im = ax.imshow(similarity_matrix, cmap='RdYlGn_r')
    fig.colorbar(im)
    ax.set_xticks(range(len(texts)))
    ax.set_yticks(range(len(texts)))
    file_names = [uploaded_file.name for uploaded_file in uploaded_files]
    truncated_names = [name[:10] + '...' if len(name) > 10 else name for name in file_names]
    ax.set_xticklabels(truncated_names, rotation=90)
    ax.set_yticklabels(truncated_names)
    st.pyplot(fig)
    from scipy.cluster.hierarchy import dendrogram, linkage
    Z = linkage(similarity_matrix)
    fig, ax = plt.subplots()
    dendrogram(Z, ax=ax, labels=truncated_names)
    plt.xticks(rotation=90)
    st.pyplot(fig)
    
    df = pd.DataFrame(identity_matrix, columns=[uploaded_file.name for uploaded_file in uploaded_files], index=[uploaded_file.name for uploaded_file in uploaded_files])
    st.write(df)

st.write('Copyright © 2023 Nuno S. Osório')
