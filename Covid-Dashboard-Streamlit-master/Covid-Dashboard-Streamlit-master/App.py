import streamlit as st
from streamlit_folium import folium_static
import json
import folium
import http.client
import pandas as pd
from folium.plugins import HeatMap
import plotly.express as px


def main():
        st.markdown("<h1 style='text-align: center; color: #ff634d;'><strong><u>Covid-19 Dashboard</u></strong></h1>",
                    unsafe_allow_html=True)
        st.sidebar.markdown(
            "<h1 style='text-align: center; color: #aaccee;'><strong><u>Covid-19 Dashboard</u></strong></h1>",
            unsafe_allow_html=True)

        st.markdown("This Web App is a live Covid-19 Dashboard which access Data sourced from this API  https://api.covid19api.com/summary",
                    unsafe_allow_html=True)

        conn = http.client.HTTPSConnection("api.covid19api.com")
        payload = ''
        headers = {}
        conn.request("GET", "/summary", payload, headers)
        res = conn.getresponse()
        data = res.read().decode('UTF-8')
        covid = json.loads(data)

        df = pd.DataFrame(covid['Countries'])

        covid1 = df.drop(columns=['CountryCode', 'Slug', 'Date', 'Premium'], axis=1)
        covid1['ActiveCases'] = covid1['TotalConfirmed'] - covid1['TotalRecovered']
        covid1['ActiveCases'] = covid1['ActiveCases'] - covid1['TotalDeaths']

        dfn = covid1.drop(['NewConfirmed', 'NewDeaths', 'NewRecovered'], axis=1)
        dfn = dfn.groupby('Country')['TotalConfirmed', 'TotalDeaths', 'ActiveCases'].sum().sort_values(
            by='TotalConfirmed', ascending=False)
        # dfn.style.background_gradient(cmap='Oranges')

        dfc = covid1.groupby('Country')['TotalConfirmed', 'TotalDeaths', 'ActiveCases'].max().sort_values(
            by='TotalConfirmed', ascending=False).reset_index()

        m = folium.Map(tiles='Stamen Terrain', min_zoom=1.5)
        url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
        country_shapes = f'{url}/world-countries.json'
        folium.Choropleth(
            geo_data=country_shapes,
            min_zoom=2,
            name='Covid-19',
            data=covid1,
            columns=['Country', 'TotalConfirmed'],
            key_on='feature.properties.name',
            fill_color='YlOrRd',
            nan_fill_color='black',
            legend_name='Total Confirmed Cases',
        ).add_to(m)

        m1 = folium.Map(tiles='Stamen Terrain', min_zoom=1.5)
        url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
        country_shapes = f'{url}/world-countries.json'
        folium.Choropleth(
            geo_data=country_shapes,
            min_zoom=2,
            name='Covid-19',
            data=covid1,
            columns=['Country', 'TotalRecovered'],
            key_on='feature.properties.name',
            fill_color='YlOrRd',
            nan_fill_color='black',
            legend_name='Total Recovered Cases',
        ).add_to(m1)

        m4 = folium.Map(tiles='Stamen Terrain', min_zoom=1.5)
        url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
        country_shapes = f'{url}/world-countries.json'
        folium.Choropleth(
            geo_data=country_shapes,
            min_zoom=2,
            name='Covid-19',
            data=covid1,
            columns=['Country', 'ActiveCases'],
            key_on='feature.properties.name',
            fill_color='YlOrRd',
            nan_fill_color='black',
            legend_name='Active Cases',
        ).add_to(m4)

        coordinates = pd.read_csv(
            'https://raw.githubusercontent.com/VinitaSilaparasetty/covid-map/master/country-coordinates-world.csv')
        covid_final = pd.merge(covid1, coordinates, on='Country')

        dfn
        confirmed_tot = int(dfc['TotalConfirmed'].sum())
        deaths_tot = int(dfc['TotalDeaths'].sum())
        active_tot = int(dfc['ActiveCases'].sum())

        st.write('TOTAL CONFIRMED CASES FROM ALL OVER THE WORLD - ', confirmed_tot)
        st.write('TOTAL DEATH CASES FROM ALL OVER THE WORLD - ', deaths_tot)
        st.write('TOTAL ACTIVE CASES FROM ALL OVER THE WORLD - ', active_tot)

        st.sidebar.subheader('Analysis through Map - Folium')

        select = st.sidebar.selectbox('Choose Map Type', ['Confirmed Cases', 'Recovered Cases', 'Active Cases', 'Deaths'],
                                      key='1')

        if not st.sidebar.checkbox("Hide Map", True):

            if select == "Confirmed Cases":
                folium_static(m)



            elif select == "Recovered Cases":

                folium_static(m1)


            elif select == "Active Cases":

                folium_static(m4)


            else:
                m2 = folium.Map(tiles='StamenToner', min_zoom=1.5)
                deaths = covid_final['TotalDeaths'].astype(float)
                lat = covid_final['latitude'].astype(float)
                long = covid_final['longitude'].astype(float)

                m2.add_child(HeatMap(zip(lat, long, deaths), radius=0))
                folium_static(m2)
       # st.sidebar.markdown("""---""")

        st.sidebar.subheader('Analysis through Bar Chart - Plotly')

        select = st.sidebar.selectbox('Choose Bar Chart', ['Confirmed Cases', 'Active Cases', 'Deaths'],
                                      key='2')
        st.markdown("""---""")
        if not st.sidebar.checkbox("Hide Bar Chart", True):

            if select == "Confirmed Cases":
                fig = px.bar(dfc.head(10), y='TotalConfirmed', x='Country', color='Country', height=400)
                fig.update_layout(title='Comparison of Total Confirmed Cases of 10 Most Affected Countries',
                                  xaxis_title='Country', yaxis_title='Total Confirmed Case', template="plotly_dark")
                st.plotly_chart(fig)
            elif select == "Active Cases":

                fig = px.bar(dfc.head(10), y='ActiveCases', x='Country', color='Country', height=400)
                fig.update_layout(title='Comparison of Active Cases of 10 Most Affected Countries', xaxis_title='Country',
                                  yaxis_title='Total ActiveCases', template="plotly_dark")
                st.plotly_chart(fig)


            else:
                fig = px.bar(dfc.head(10), y='TotalDeaths', x='Country', color='Country', height=400)
                fig.update_layout(title='Comparison of Total Deaths of 10 Most Affected Countries', xaxis_title='Country',
                                  yaxis_title='Total Deaths', template="plotly_dark")
                st.plotly_chart(fig)

        #st.sidebar.markdown("""---""")
        st.sidebar.subheader('Analysis through Pie Chart - Plotly')

        select1 = st.sidebar.selectbox('Choose Pie Chart', ['Confirmed Cases', 'Active Cases', 'Deaths'],
                                      key='2')
        st.markdown("""---""")


        if not st.sidebar.checkbox("Hide Pie Chart", True):

            if select1 == "Confirmed Cases":
                figg = px.pie(dfc.head(10), values='TotalConfirmed', names='Country', title='TotalConfirmed')
                st.plotly_chart(figg)
            elif select1 == "Active Cases":
                figg1 = px.pie(dfc.head(10), values='ActiveCases', names='Country', title='ActiveCases')
                st.plotly_chart(figg1)
            else:
                figg2 = px.pie(dfc.head(10), values='TotalDeaths', names='Country', title='TotalDeaths')
                st.plotly_chart(figg2)




if __name__ == '__main__':
        main()
        st.markdown("""---""")

        st.markdown("For issues Contact - hbfawaz112@gmail.com")
        st.markdown("""---""")
