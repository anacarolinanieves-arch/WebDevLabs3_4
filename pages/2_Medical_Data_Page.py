# Lab 3: API data page
# TODO: Rename this file to fit your page. Keep the number at the front, since it sets the
#       page's order in the sidebar (for example, 2_Pokedex.py).
#
# This page shows data from your API, processed with your own Python code. No AI on this page.
# It should have:
#   - at least 2 meaningful user inputs (for example st.selectbox, st.text_input, st.slider)
#   - at least 2 dynamic visuals that change based on the user's input: charts, displays of
#     images, or other visualizations (see the example website for examples!)

import requests
import streamlit as st

def buildQuery(deviceName, startYear, endYear, mfgName):
    dateFilter = f"date_received:[{startYear}0101 TO {endYear}1231]"
    query = f'device.generic_name:"{deviceName}" AND {dateFilter}'
    if mfgName.strip() != "":
        query += f' AND device.manufacturer_d_name:"{mfgName.strip()}"'
    return query


def getFdaCounts(searchQuery, countField):
    url = "https://api.fda.gov/device/event.json"
    paramsDict = { "search": searchQuery,"count": countField}
    try:
        r = requests.get(url, params=paramsDict)
        if r.status_code != 200:
            return []
        data = r.json()
        if "results" in data:
            return data["results"]
        else:
            return []
    except:
        return []

def makeCountDict(aList, maxItems):
    aDict = {}
    for item in aList:
        if len(aDict) >= maxItems:
            break
        label = item["term"]
        aDict[label] = item["count"]
    return aDict


def groupByYear(dateList):
    yearlyDict = {}
    for item in dateList:
        year = item["time"][:4]
        count = item["count"]
        if year in yearlyDict:
            yearlyDict[year] += count
        else:
            yearlyDict[year] = count

    sortedDict = {}
    for year in sorted(yearlyDict):
        sortedDict[year] = yearlyDict[year]
    return sortedDict


st.title("Medical Device Reliability Explorer")
st.write("Explore hospital medical device malfunction and safety reports from the official openFDA MAUDE database.")

deviceList = [
    "Infusion Pump",
    "Ventilator",
    "Patient Monitor",
    "Defibrillator",
    "Pacemaker"
]
selectedDevice = st.selectbox("Select a medical device type:", deviceList)
yearRange = st.slider("Select year range:", 2018, 2025, (2020, 2024))
topNum = st.slider("Number of top manufacturers / failure reasons to display:", 3, 10, 5)
mfgInput = st.text_input("Optional: filter by manufacturer name (e.g., Medtronic, Philips, Baxter):")

startYear = yearRange[0]
endYear = yearRange[1]
searchQuery = buildQuery(selectedDevice, startYear, endYear, mfgInput)

eventResults = getFdaCounts(searchQuery, "event_type.exact")
dateResults = getFdaCounts(searchQuery, "date_received")
mfgResults = getFdaCounts(searchQuery, "device.manufacturer_d_name.exact")
probResults = getFdaCounts(searchQuery, "product_problems.exact")

if not eventResults:
    st.warning("No FDA reports found for those filters. Try clearing the manufacturer filter or widening the year range.")
else:
    eventDict = makeCountDict(eventResults, 10)

    totalReports = 0
    for key in eventDict:
        totalReports += eventDict[key]

    if "Malfunction" in eventDict:
        malfunctions = eventDict["Malfunction"]
    else:
        malfunctions = 0

    if "Injury" in eventDict:
        injuries = eventDict["Injury"]
    else:
        injuries = 0

    if "Death" in eventDict:
        deaths = eventDict["Death"]
    else:
        deaths = 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reports", totalReports)
    col2.metric("Malfunctions", malfunctions)
    col3.metric("Injuries", injuries)
    col4.metric("Deaths", deaths)

    # visual 1
    st.subheader(f"Reported Issues Over Time ({selectedDevice})")
    yearlyData = groupByYear(dateResults)
    st.line_chart(yearlyData)

    # visual 2
    st.subheader("Reports by Event Type")
    st.bar_chart(eventDict)

    # visual 3
    st.subheader(f"Top {topNum} Manufacturers by Report Count")
    topMfgDict = makeCountDict(mfgResults, topNum)
    st.bar_chart(topMfgDict)

    # visual 4
    st.subheader(f"Top {topNum} Most Common Failure Reasons")
    if len(probResults) > 0:
        topProbDict = makeCountDict(probResults, topNum)
        st.bar_chart(topProbDict)
    else:
        st.info("No specific failure problem categories were listed for this selection.")
