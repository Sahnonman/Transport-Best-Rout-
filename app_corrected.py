
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Transport Route Optimizer", page_icon="🚛")

st.title("🚛 Transport Route Optimizer")
st.write("""
This tool helps you distribute transport demand between company trucks and 3PL
providers based on cost and availability. Upload your Excel file to begin.
""")

uploaded_file = st.file_uploader("📂 Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Routes")
    st.success("✅ File loaded successfully!")
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
    st.subheader("📊 Optimized Distribution")
    st.dataframe(result_df)

    # Save to in-memory file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        result_df.to_excel(writer, index=False)
    output.seek(0)

    st.download_button(
        label="⬇️ Download Optimized Plan as Excel",
        data=output,
        file_name="Optimized_Route_Distribution.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("📌 Please upload a file to start optimization.")
