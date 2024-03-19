import streamlit as st
import pandas as pd

# Function to transform data to long format using wide_to_long function
def transform_data(df):
    transformed_data = {}
    for letter in ["a", "b", "c", "l"]:
        data = []
        for index, row in df.iterrows():
            for col in df.columns:
                if col.startswith('hs') and col != 'hs'+letter:
                    other_letter = col.replace('hs', '')
                    main_text = row['hs{}'.format(letter)]
                    additional_text = '{}: {}'.format(other_letter.upper(), row['hs{}'.format(other_letter.lower())])
                    distance_column = [c for c in df.columns if "dis" in c and letter in c and other_letter in c][0]
                    distance = row[distance_column]
                    data.append([index, main_text, additional_text, distance])
        transformed_data[letter] = pd.DataFrame(data, columns=['Index', 'Main Text', 'Additional Text', 'Distance'])
    return transformed_data

# Function to filter data based on selected main text and distance threshold
def filter_data(threshold, df):
    filtered_df = df.copy()
    filtered_df.loc[filtered_df['Distance'] < threshold, 'Additional Text'] = ''
    grouped_df = filtered_df.groupby(['Index', 'Main Text'])['Additional Text'].apply(lambda x: '<br>'.join(x)).reset_index()
    return grouped_df

# Main function to run the Streamlit app
def main():
    st.title("Text Filtering App")

    # Read CSV file
    try:
        df = pd.read_csv("master.csv", sep=";", decimal=",")
        df.fillna('', inplace=True)
    except FileNotFoundError:
        st.warning("CSV file not found. Displaying example data.")
        example_data = {
            'hsa': ['this is text a1', 'this is text a2', 'this is text a3'],
            'hsb': ['this is text b1', 'this is text b2', 'this is text b3'],
            'hsc': ['this is text c1', 'this is text c2', 'this is text c3'],
            'hsl': ['this is text l1', 'this is text l2', 'this is text l3'],
            'dis a b': [0.1, 0.2, 0.3],
            'dis a c': [0.4, 0.5, 0.6],
            'dis a l': [0.7, 0.8, 0.9],
            'dis b c': [0.1, 0.2, 0.3],
            'dis b l': [0.4, 0.5, 0.6],
            'dis c l': [0.7, 0.8, 0.9]
        }
        df = pd.DataFrame(example_data)

    # Transform data to long format
    transformed_data = transform_data(df)

    # Sidebar widgets
    st.sidebar.header("Filter Options")
    main_text = st.sidebar.selectbox("Choose Main Text", ["a", "b", "c", "l"])
    threshold = st.sidebar.slider("Distance Threshold", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

    # Filter data
    filtered_df = filter_data(threshold, transformed_data[main_text])

    # Display filtered texts
    st.write("Filtered Texts:")
    if not filtered_df.empty:
        st.write(filtered_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.write("No filtered texts found.")

if __name__ == "__main__":
    main()
