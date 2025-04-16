import streamlit as st
from module3model import Module3Model

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

def main():
    st.title("Input Example for Streamlit App")
    
    # Input 1: allowed_directions via selectbox (or radio if preferred)
    allowed_directions = st.selectbox(
        "Select allowed direction:",
        options=["up", "down"]
    )
    
    # Input 2: allowed_magnitudes from a predefined list
    allowed_magnitudes = st.selectbox(
        "Select allowed magnitude:",
        options=[5, 10, 15, 20, 25, 30, 40, 50, 75, 100]
    )
    
    # Input 3: max_amount as a positive scalar value
    # Setting a minimum value to 0.0 helps ensure only non-negative values,
    # and the default is set to 1.0.
    max_amount = st.number_input(
        "Enter max amount (a positive scalar value):",
        min_value=0.0,
        value=1.0,
        step=0.1,
        format="%.2f"
    )
    
    # Display the chosen inputs when the user clicks the 'Submit' button
    if st.button("Submit"):
        st.write("### Your Inputs:")
        st.write("**Allowed Direction:**", allowed_directions)
        st.write("**Allowed Magnitude:**", allowed_magnitudes)
        st.write("**Max Amount:**", max_amount)

    st.title("Module3Model Data Demo")

    model = Module3Model()
    asset_df, asset_price, df_gas = model.load_data()

    st.subheader("Asset Data")
    st.dataframe(asset_df)

    st.subheader("Asset Price Data")
    st.dataframe(asset_price)

    st.subheader("Gas Price Data")
    st.dataframe(df_gas)

if __name__ == "__main__":
    main()


