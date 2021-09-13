# Streamlit app

from helpers import *
import streamlit as st

COVID_DATABASE_URL = 'https://www.covid19.act.gov.au/act-status-and-response/act-covid-19-exposure-locations'

st.set_page_config(page_title='CovidAlyzer')

print('')
def _get_webdriver():
    options = webdriver.FirefoxOptions()
    options.add_argument("-remote-debugging-port=9224")
    options.add_argument("-headless")
    options.add_argument("-disable-gpu")
    options.add_argument("-no-sandbox")

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

    firefox_driver = webdriver.Firefox(
		firefox_binary=binary,
		executable_path=os.environ.get('GECKODRIVER_PATH'),
		options=options)

    return firefox_driver

driver = _get_webdriver()
@st.cache()
def collect_data_cached(url):  
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
