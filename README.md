# Welcome to our Search Intent Inspector Streamlit App!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, write to [us](https://wordlift.io).

How to run:
```python
$ python3.7 -m venv ~/.streamlit_v
$ source ~/.streamlit_v/bin/activate
$ pip install -U pip
$ cd my/directory
$ pip install -r requirements.txt
$ streamlit run streamlit_app.py
```
How to change text color:
```python
st.markdown(""" <span style="color:red"> text in red </span> """, unsafe_allow_html=True)
```

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── streamlit_app.py *** the main driver of the app.
  ├── utils.py *** classes, functions, statements, etc
  ├── struct.py *** mainly for design
  ├── requirements.txt *** The dependencies we need to install with "pip install -r requirements.txt"
  └── static
      ├── style.css
      ├── index.html
      ├── fonts
      └── img
  ```
