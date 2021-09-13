# Streamlit app

from helpers import *
import streamlit as st

COVID_DATABASE_URL = 'https://www.covid19.act.gov.au/act-status-and-response/act-covid-19-exposure-locations'

st.set_page_config(page_title='CovidAlyzer')


def _get_webdriver():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.headless = True
    driver = webdriver.Firefox('./geckodriver',options=fireFoxOptions)
    return driver


@st.cache()
def collect_data_cached(url):  
    driver = _get_webdriver()
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    current = pd.read_html(html)[0]
    element = driver.find_element(By.ID,"chkArchived1822887")
    element.click()
    time.sleep(1)
    html = driver.page_source
    archived = pd.read_html(html)[0]
    return current, archived


markdown_text = """
# Covid Exposure Sites Web App
---
## Usage:
Type in the stores that you want to see separated by slashes, 
for example `Coles/Woolworths/IGA`, and select whether you want 
to see the archived entries (`True`) or whether you want them to be hidden (`False`)
"""
st.markdown(markdown_text)

shops = st.text_input(label='Which shops do you want to analyse', value='Coles/Woolworths/IGA')
view_archived = st.checkbox(label='Include archived exposure sites?', value=True)

current, archived = collect_data_cached(url=COVID_DATABASE_URL)

COVID_DATABASE_URL = 'https://www.covid19.act.gov.au/act-status-and-response/act-covid-19-exposure-locations'

if view_archived:
    data = archived
else:
    data = current

shop_data = check_shop(data, shops)
times = add_times(shop_data)

chart = make_plot(times, shops)
st.write(chart)
st.write(shop_data)

print('finished')
