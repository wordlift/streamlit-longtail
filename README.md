# streamlit-longtail  
This is the repository for the streamlit web application of the the long-tail query inspector. A tool meant to help you find new query opportunities.  

**In order to run the app (you must set up a virtual environment), do the following in terminal:**  
How to run:
```python
$ python3.7 -m venv ~/.streamlit_v
$ source ~/.streamlit_v/bin/activate
$ pip install -U pip
$ cd my/directory
$ pip install -r requirements.txt
$ streamlit run streamlit_app.py
```
(streamlit_v is the name of the virtual environment, you can use any other name)

How to change text color:
```python
st.markdown(""" <span style="color:red"> text in red </span> """, unsafe_allow_html=True)
```

Main Files: Project Structure
├── README.md
├── app.py *** the main driver of the app. 
├── utils.py ***
├── requirements.txt *** The dependencies we need to install with "pip install -r requirements.txt"
└── static
    ├── style.css 
    ├── index.html
    ├── font
    └── img
    
