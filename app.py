import streamlit as st
from model import Evaluate


evaluator = Evaluate()

#st.title("Bible Verse Search")
#st.markdown('built by [@shreydan](https://github.com/shreydan)')
#st.markdown("### Praise the Lord.")
#st.markdown("##### Please type the text you recall from the verse to get references.")


with st.container():
    text_input:str = st.text_input(label='Bible search phrase / keywords',key='input')
    text_input = text_input.strip()
    #st.caption('Examples: do not be afraid, bless the Lord oh my soul')
    num_responses = st.number_input(
        label='number of responses',
        min_value=10,
        max_value=500,
        step=10,
        value=25
    )
    num_responses = int(num_responses)

    submitted = st.button(
        label='Search'
        #,type='primary'
    )




if len(text_input) != 0 or submitted:
    response = evaluator.get_verses(text_input,top=num_responses)
    references = response['reference']
    verses = response['verse']

    st.markdown('Verses found ...\n___')
    #[{ref}](https://www.esv.org/verses/{ref.replace(" ","%20")})/  
    #{ref}https://www.esv.org/verses/{ref.replace(" ","%20")}/
 
    for ver, ref in zip(verses,references):
        with st.container():
            md = f"""
         
            [{ref}](https://www.esv.org/verses/{ref.replace(" ","%20")}/)   {ver}
            ___
            """
            st.markdown(md, unsafe_allow_html=True)

st.caption('Thanks and credit to [@shreydan](https://github.com/shreydan)')
