
import streamlit as st
import pandas as pd

st.title("Transport Route Optimizer")
st.write("Upload your Excel file with routes, costs, and availability.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Routes")
    st.success("File loaded successfully!")
    st.dataframe(df)

    results = []
    for _, row in df.iterrows():
        demand = row["Demand"]
        available = row["Company_Trucks_Available"]
        company_trips = min(demand, available)
        remaining_trips = demand - company_trips
        company_cost = company_trips * row["Company_Cost"]
        pl3_cost = remaining_trips * row["3PL_Cost"]
        total_cost = company_cost + pl3_cost

        results.append({
            "From": row["From"],
            "To": row["To"],
            "Company_Trips": company_trips,
            "3PL_Trips": remaining_trips,
            "Company_Cost": company_cost,
            "3PL_Cost": pl3_cost,
            "Total_Cost": total_cost
        })

    result_df = pd.DataFrame(results)
    st.subheader("Optimized Distribution")
    st.dataframe(result_df)

    st.download_button(
        label="Download Optimized Plan as Excel",
        data=result_df.to_excel(index=False, engine='openpyxl'),
        file_name="Optimized_Route_Distribution.xlsx"
    )
else:
    st.info("Please upload a file to start optimization.")
