import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os



st.set_page_config("NEET 2024 DATA ANALYSIS", layout='wide')

@st.cache_data
def load_data():
    # List all files in the directory
    files = [os.path.join("./data2024", f) for f in os.listdir("./data2024") if f.startswith('df_chunk_')]
    # Sort files to maintain order
    files.sort()
    combined_df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
    return combined_df

@st.cache_data
def load_states(df):
    return df['CENTER STATE'].unique().tolist()

@st.cache_data
def load_cities(df, state):
    state_df = df[df['CENTER STATE']==state]
    return state_df, state_df['CENTER CITY'].unique().tolist()

@st.cache_data
def load_centers(state_df, city):
    city_df = state_df[state_df['CENTER CITY']==city]
    return city_df, city_df['CENTER NAME'].unique().tolist()

@st.cache_data
def overall(df):
    data ={
        "Location": [],
        "Marks": [],
        "Percentage": []
    }
    records = len(df)
    for m in range(-180, 721):
        count = (df['MARKS'] >= m).sum() * 100 / records
        data['Location'].append("OVERALL")
        data['Percentage'].append(count)
        data['Marks'].append(m)
    return pd.DataFrame(data)


@st.cache_data
def overall_hist(df):
    return go.Histogram(x=df['MARKS'], name='OVERALL', histnorm='percent')

df = load_data()

filters = st.columns(3)

states = load_states(df)
state = filters[0].selectbox("STATE", states, None)

state_df, cities = load_cities(df, state)
city = filters[1].selectbox("CITY", cities, None)

city_df, centers = load_centers(state_df, city)
center = filters[2].selectbox("CENTER", centers, None)

if center:
    center_df = city_df[city_df['CENTER NAME']==center]
else:
    center_df = pd.DataFrame()


if len(center_df)>1:
    temp_df = center_df
elif len(city_df)>1:
    temp_df = city_df
elif len(state_df)>1:
    temp_df = state_df
else:
    temp_df = df

st.title("PERFORMANCE RANKING BASED ON AVERAGE MARKS")

performance = st.columns(3)
with performance[0]:
    temp_df["avg"] = temp_df.groupby("CENTER STATE")["MARKS"].transform('mean')
    sorted_df = temp_df.drop_duplicates(subset="CENTER STATE").sort_values("avg", ascending=False)
    state_ranking = pd.DataFrame(sorted_df['CENTER STATE'].unique(), columns=["RANKING OF STATES"])
    st.dataframe(state_ranking, hide_index=True, use_container_width=True)

with performance[1]:
    temp_df["avg"] = temp_df.groupby("CENTER CITY")["MARKS"].transform('mean')
    sorted_df = temp_df.drop_duplicates(subset="CENTER CITY").sort_values("avg", ascending=False)
    city_ranking = pd.DataFrame(sorted_df['CENTER CITY'].unique(), columns=["RANKING OF CITIES"])
    st.dataframe(city_ranking, hide_index=True, use_container_width=True)

with performance[2]:
    temp_df["avg"] = temp_df.groupby("CENTER NAME")["MARKS"].transform('mean')
    sorted_df = temp_df.drop_duplicates(subset="CENTER NAME").sort_values("avg", ascending=False)
    center_ranking = pd.DataFrame(sorted_df['CENTER NAME'].unique(), columns=["RANKING OF CENTERS"])
    st.dataframe(center_ranking, hide_index=True, use_container_width=True)



st.title("GRAPHICAL ANALYSIS")


m_range = range(-180, 721)

data ={
    "Location": [],
    "Marks": [],
    "Percentage": []
}

dfs = [(center, center_df), (city, city_df), (state, state_df)]


for k,i in dfs:
    records  = len(i)
    if records > 1:
        for m in m_range:
            count = (i['MARKS'] >= m).sum() * 100 / records
            data['Percentage'].append(count)
            data["Location"].append(k)
            data['Marks'].append(m)


data = pd.DataFrame(data)
data = pd.concat([data, overall(df)])


graphs = st.columns(2)

with graphs[0]:
    st.write("Percentage of Student >= Marks")
    fig = px.line(data, x="Marks", y="Percentage", color='Location')
    st.plotly_chart(fig, use_container_width=True)

with graphs[1]:
    st.write("Percentage of Students vs Marks")
    fig2 = go.Figure()

    fig2.add_trace(overall_hist(df))
    
    for k,i in dfs:
        records  = len(i)
        if records > 1:
            fig2.add_trace(go.Histogram(x=i['MARKS'], name=k, histnorm='percent'))

    fig2.update_layout(barmode='overlay')
    fig2.update_traces(opacity=0.75)

    st.plotly_chart(fig2, use_container_width=True)


st.title('COMPARE')

comp_filters = st.columns(3)

comp_states = comp_filters[0].multiselect('STATE', temp_df['CENTER STATE'].unique().tolist())
comp_cities = comp_filters[1].multiselect('CITY', temp_df['CENTER CITY'].unique().tolist())
comp_centers = comp_filters[2].multiselect('CENTER', temp_df['CENTER NAME'].unique().tolist())

m_range = range(-180, 721)

comp_data ={
    "Location": [],
    "Marks": [],
    "Percentage": []
}

entities = {
    "CENTER STATE": comp_states,
    "CENTER CITY": comp_cities,
    "CENTER NAME": comp_centers
}

for k,v in entities.items():
    for x in v:
        data = temp_df[temp_df[k]==x]
        records = len(data)
        for m in m_range:
            count = (data['MARKS'] >= m).sum() * 100 / records
            comp_data['Percentage'].append(count)
            comp_data["Location"].append(x)
            comp_data['Marks'].append(m)


comp_data = pd.DataFrame(comp_data)
comp_data = pd.concat([comp_data, overall(df)])


graphs = st.columns(2)

with graphs[0]:
    st.write("Percentage of Student >= Marks")
    fig = px.line(comp_data, x="Marks", y="Percentage", color='Location')
    st.plotly_chart(fig, use_container_width=True)

with graphs[1]:
    st.write("Percentage of Students vs Marks")
    fig2 = go.Figure()

    fig2.add_trace(overall_hist(df))

    for k,v in entities.items():
        for x in v:
            data = temp_df[temp_df[k]==x]
            records = len(data)
            if records > 1:
                fig2.add_trace(go.Histogram(x=data['MARKS'], name=x, histnorm='percent'))


    fig2.update_layout(barmode='overlay')
    fig2.update_traces(opacity=0.75)

    st.plotly_chart(fig2, use_container_width=True)
