import streamlit as st
import pandas as pd 
#yeh viersion naam hai 
APP_VERSION = " V.1.0.0 "
#yeh page ka page ka naam aur icon hai 
st.set_page_config(
    page_title = " Flow X ",
    page_icon = "✖️",
    layout = "wide"
)
# yeh page ke under ka naam hai 
st.title(" Flow X ")
st.header(" Data Cleaner ")
st.caption(f"Version : {APP_VERSION} ")
# yeh mardown page ke under ka title ka upar ka khali jagah ko hata diya
st.markdown(
    ''' <style>
    .block-container{
    padding-top:2rem;
    }
    </style>
''',unsafe_allow_html=True)
# input user file 
upload_file = st.file_uploader("File Upload (Csv / Excel)",type =["csv","xlsx"])
if upload_file is not None :
    file_loaded = False

    try:
        
        if upload_file.name.endswith('.csv'):
             file_read = pd.read_csv(upload_file)
           # yeh check karega file ke under mein koi extra row hai but uska colum nahi hai (like : salary 2,200 aise number mein ho extra column left side se nikal deta hai )
             if not isinstance(file_read.index, pd.RangeIndex):
                # yeh usko rok ta hai aaur message phek ta hai 
                raise ValueError("🚨 Alert: Invalid CSV format. Data has shifted due to extra commas (e.g., '2,200'). Please upload an Excel (.xlsx) file.")
             st.dataframe(file_read.head())
             
        else:
            file_read = pd.read_excel(upload_file)
            st.dataframe(file_read.head())
    # check file empty hai ya nahi hai 
        if file_read.empty or len(file_read.columns) ==0 :
            st.error("🚨 Error: The uploaded file is completely empty. Please check your data.")
        else:
            file_loaded = True
    # 4 column but row len 5 hai tab yeh dikhega 
    except pd.errors.ParserError:
        st.error("🚨 Data Alert: The CSV file structure is corrupted (column count mismatch). Please upload this data as an Excel (.xlsx) file to maintain alignment.")
        # jab user galt file upload karenge like png/text file 
    except UnicodeDecodeError:
        st.error("🚨 Error: Invalid file type. Please upload only tabular data (CSV or Excel). Images/Videos/Other file are not supported.")
        # empty file upload karne se 
    except pd.errors.EmptyDataError:
        st.error("🚨 Error: The uploaded file appears to be empty or lacks identifiable columns. Please verify the file content.")
        # jab user try kiya hoga galat csv format ko excel mein banane keliye / jab csv file mein ek column ka row mein aisa likha hoga (like :2,200) to ho ek extra column mein ghus jaat hai toh "raise value error" phekega
    except ValueError as err:
        error_message = str(err).lower()
            # jab csv file ke under aisa vlue ho jo ek value but do coloumn leta hai (like : 2,200)
        if "invalid csv" in error_message or "shifted" in error_message:
            st.error(err)
        # jab hum  csv file ko zabardasti excel file mein banane ki kosish karte hian to yeh dikhayega
        else:
            # Agar koi aur bimari hai, toh yeh hidden reason screen par print kar dega
            st.error(f"🚨 Error: Invalid Excel file detected. [Hidden Reason: {err}]")
      # jo error hum ko pata nahi hai usko yahan block karke ui se nahi dikhane keliye 
    except Exception:
        st.error("🚨 System Error: The file could not be processed. ")

    if file_loaded:
        st.write("-----------")

        if st.button("Click Here To Clean Data", type="primary"):                

            empty_row = file_read.dropna(how = 'all')
            remove_duplicate_value = empty_row.drop_duplicates()
         # reset_ index jab data clean karne ke baad dikhayega user ko tab index ko sequence mein rakhne keliye (drop = true) use hua 
            index_correct = remove_duplicate_value.reset_index(drop= True)

            st.dataframe(index_correct)
            st.success("✅ Data Clean Successfully")

          # File  download hone ke baad index download file mein show nahi karega isliye (index = False) hai 
            csv_download = remove_duplicate_value.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Cleaned Data Download ",
                type = "primary",
                data= csv_download,
                file_name="cleaned_data.csv",
                mime="text/csv"
            )

