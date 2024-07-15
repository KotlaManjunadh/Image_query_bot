from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = api_key )

# creating model
model = genai.GenerativeModel('gemini-pro-vision')

def getting_gemini_response(query,image,prompt):
    response = model.generate_content([query,image[0],prompt])
    return response

def input_image(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {'mime_type':uploaded_file.type, 'data':bytes_data}
        ]
        return image_parts
    else:
        raise FileNotFoundError('File not found')
# creating webpage
st.set_page_config(page_title='Image_answering')
st.header('This is a bot which answers all the questions related to your image.')

uploaded_file = st.file_uploader('Upload your Image here', type=['jpg','jpeg','gif','png'])

image = ''
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption='Uploaded image', use_column_width= True)

query = st.text_input('What do you wanna know about this image',key ='input')

prompt = '''
You are a great expert in understanding images. 
we will be asking you questions related to the image that we have provided and you need to answer them carefully.
'''


submit = st.button('Submit')

if submit:
    image_data = input_image(uploaded_file)
    response = getting_gemini_response(query=query, image= image_data, prompt = prompt)
    st.subheader('Answer:')
    st.write(response.text)

