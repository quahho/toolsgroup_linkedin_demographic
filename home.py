
# Import libraries
import streamlit as st
import enrich as en
from random import randint


# Function to display enrich sheets page
def showEnrichPage() :


    # Adjust length of button
    st.write(
        """
        <style>
        [class="row-widget stButton"] button {
            width: 100%;
            background-color: #FD6767;
        }
        [class="row-widget stDownloadButton"] button {
            width: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # To store campaign uploader key
    if 'campaign_upload' not in st.session_state:
        st.session_state['campaign_upload'] = str(randint(1000, 100000000))

    # To store file uploader key
    if 'file_upload' not in st.session_state:
        st.session_state['file_upload'] = str(randint(1000, 100000000))

    # To store process ended boolean
    if 'process_ended' not in st.session_state:
        st.session_state['process_ended'] = True

    # To store export now boolean
    if 'export_now' not in st.session_state:
        st.session_state['export_now'] = False
    
    # To store output table
    if 'output_table' not in st.session_state:
        st.session_state['output_table'] = []

    # To store company name dataframe
    if 'company_name_data' not in st.session_state:
        st.session_state['company_name_data'] = []

    # To store company industry dataframe
    if 'company_industry_data' not in st.session_state:
        st.session_state['company_industry_data'] = []
    
    # To store company size dataframe
    if 'company_size_data' not in st.session_state:
        st.session_state['company_size_data'] = []
    
    # To store country-region dataframe
    if 'country_region_data' not in st.session_state:
        st.session_state['country_region_data'] = []

    # To store location dataframe
    if 'location_data' not in st.session_state:
        st.session_state['location_data'] = []
    
    # To store job seniority dataframe
    if 'job_seniority_data' not in st.session_state:
        st.session_state['job_seniority_data'] = []

    # To store job title dataframe
    if 'job_title_data' not in st.session_state:
        st.session_state['job_title_data'] = []
    
    # To store job function dataframe
    if 'job_function_data' not in st.session_state:
        st.session_state['job_function_data'] = []

    # To store county dataframe
    if 'county_data' not in st.session_state:
        st.session_state['county_data'] = []

    # To store campaigns covered
    if 'campaign_covered' not in st.session_state:
        st.session_state['campaign_covered'] = []

    # =====================================================================================================================


    # Set page title
    st.title('LinkedIn Demographics :world_map:')

    # Create space
    st.write('')
    st.write('')


    # =====================================================================================================================


    # First step -- Upload Campaign List
    st.subheader(':spiral_note_pad: Upload Campaign List')

    # Create space
    st.write('')

    # Create file uploader for campaign list
    campaign_list = st.file_uploader(
        label = 'Upload CSV file', 
        type = 'csv',
        key = st.session_state['campaign_upload'],
        label_visibility = 'collapsed'
    )

    # Initialize campaign data holder
    campaign_data = []

    # Initialize campaign presence check
    campaign_check = False

    # When there is a campaign list 
    if campaign_list :

        # Get campaign data
        campaign_data = en.getCampaignData(campaign_list)

        # When there are campaigns
        if len(campaign_data) > 0 :

            # Set trigger
            campaign_check = True

    # When there is no campaign list
    else :

        # Change the key of the file uploader
        st.session_state['file_upload'] = str(randint(1000, 100000000))

        # Set process to end
        st.session_state['process_ended'] = True

        # Set process to end
        st.session_state['export_now'] = False

        # Clear out stored data
        st.session_state['output_table'] = []
        st.session_state['company_name_data'] = []
        st.session_state['company_industry_data'] = []
        st.session_state['company_size_data'] = []
        st.session_state['country_region_data'] = []
        st.session_state['location_data'] = []
        st.session_state['job_seniority_data'] = []
        st.session_state['job_title_data'] = []
        st.session_state['openejob_function_datad_data'] = []
        st.session_state['county_data'] = []
        st.session_state['campaign_covered'] = []

    # Create space
    st.write('')


    # =====================================================================================================================


    # Second step -- Select Campaign Name and Extract Date
    st.subheader(':spiral_calendar_pad: Select Campaign and Date')

    # Create equal size columns 
    column_1, column_2 = st.columns([1, 1])

    # In the first column
    with column_1 :

        # When there is a proper campaign list 
        if campaign_check :

            # Use the list of campaign name
            campaign_option = list(campaign_data['Campaign Name'])
        
        # When no proper campaign list found
        else :

            # No options should be available
            campaign_option = []
            

        # Create select box for campaign options
        campaign_choice = st.selectbox(
            label = 'Campaign :',
            options = campaign_option,
            disabled = not campaign_check
        )

        # Initialize campaign id holder
        campaign_info = ''

        # When there is a campaign selected
        if campaign_choice :

            # Get the selected campaign's info
            campaign_info = list(campaign_data[campaign_data['Campaign Name'] == campaign_choice]['Campaign ID'])[0]


    # In the second column
    with column_2 :

        # Create date picker for extract date
        extract_date = st.date_input(
            label = 'Date :'
        )

    # Create space
    st.write('')


    # =====================================================================================================================


    # Third step -- Upload CSV files
    st.subheader(':inbox_tray: Upload CSV File')
    
    # Create space
    st.write('')
    
    # Create file uploader for CSV file
    uploaded_file = st.file_uploader(
        label = 'Upload CSV file', 
        type = 'csv',
        key = st.session_state['file_upload'],
        label_visibility = 'collapsed'
    )
    
    # When there is an uploaded file with other inputs present
    if uploaded_file and campaign_info and extract_date :

        # Set process to end
        st.session_state['process_ended'] = False

    # When there is no uploaded file
    else :

        # Set process to end
        st.session_state['process_ended'] = True

    # Create space
    st.write('')
    

    # =====================================================================================================================


    # Fourth step -- Start Enrichment
    st.subheader(':postal_horn: Start Process')
    
    # Create space
    st.write('')

    # Create button for starting process
    start_button = st.button(
        label = '**Enrich CSV File**',
        type = 'primary',
        disabled = st.session_state['process_ended']
    )

    # When button is pressed
    if start_button :

        # Create spinner for loading
        with st.spinner('In progress...'):

            # Enrich data
            en.enrichCSV(uploaded_file, campaign_choice, campaign_info, extract_date)
            
            # End the process 
            en.endProcess()
    
    # Create space
    st.write('')


    # =====================================================================================================================


    # When process completed successfully and there is output
    if len(st.session_state['output_table']) > 0 :

        # Set label
        st.write('List of campaigns covered:')

        # Display dataframe
        st.dataframe(st.session_state['output_table'])

        # Create space
        st.write('')

        # Set fine print warning
        st.code('# Repeat the above steps until all campaigns are covered before proceeding.')

        # Create compile reports button
        compile_button = st.button(
            label = '**Compile All CSV Files By Segment**',
            type = 'primary',
            on_click = en.proceedExport,
            disabled = not st.session_state['process_ended']
        )

        # Create space
        st.write('')

    
    # =====================================================================================================================


    # When button is pressed
    if st.session_state['export_now'] :

        # Set label
        st.write('Export demographic data:')

        # When there is data for company name
        if len(st.session_state['company_name_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Company Name Segment Data',
                data = st.session_state['company_name_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Company Name Segment Data.csv',
                mime = 'text/csv'
            )

        # When there is data for company industry
        if len(st.session_state['company_industry_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Company Industry Segment Data',
                data = st.session_state['company_industry_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Company Industry Segment Data.csv',
                mime = 'text/csv'
            )

        # When there is data for company size
        if len(st.session_state['company_size_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Company Size Segment Data',
                data = st.session_state['company_size_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Company Size Segment Data.csv',
                mime = 'text/csv'
            )

        
        # When there is data for country region
        if len(st.session_state['country_region_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Country Region Segment Data',
                data = st.session_state['country_region_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Country Region Segment Data.csv',
                mime = 'text/csv'
            )

        # When there is data for location
        if len(st.session_state['location_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Location Segment Data',
                data = st.session_state['location_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Location Segment Data.csv',
                mime = 'text/csv'
            )

        # When there is data for job seniority
        if len(st.session_state['job_seniority_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Job Seniority Segment Data',
                data = st.session_state['job_seniority_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Job Seniority Segment Data.csv',
                mime = 'text/csv'
            )

        
        # When there is data for job title
        if len(st.session_state['job_title_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Job Title Segment Data',
                data = st.session_state['job_title_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Job Title Segment Data.csv',
                mime = 'text/csv'
            )

        # When there is data for job function
        if len(st.session_state['job_function_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All Job Function Segment Data',
                data = st.session_state['job_function_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled Job Function Segment Data.csv',
                mime = 'text/csv'
            )

        # When there is data for clicked
        if len(st.session_state['county_data']) > 0 :

            # Display download button
            st.download_button(
                label = 'Download All County Segment Data',
                data = st.session_state['county_data'].to_csv(encoding = 'utf-8-sig', index = False),
                file_name = 'Compiled County Segment Data.csv',
                mime = 'text/csv'
            )

        # ===========================================================================================================================

        # Create space
        st.write('')

        # Create checkbox for restart
        if st.checkbox(':arrows_counterclockwise: Restart') :

            # Change the key of the campaign uploader
            st.session_state['campaign_upload'] = str(randint(1000, 100000000))

            # Change the key of the file uploader
            st.session_state['file_upload'] = str(randint(1000, 100000000))

            # Set process to end
            st.session_state['process_ended'] = True

            # Set process to end
            st.session_state['export_now'] = False

            # Clear out stored data
            st.session_state['output_table'] = []
            st.session_state['company_name_data'] = []
            st.session_state['company_industry_data'] = []
            st.session_state['company_size_data'] = []
            st.session_state['country_region_data'] = []
            st.session_state['location_data'] = []
            st.session_state['job_seniority_data'] = []
            st.session_state['job_title_data'] = []
            st.session_state['openejob_function_datad_data'] = []
            st.session_state['county_data'] = []
            st.session_state['campaign_covered'] = []

            # Rerun the page
            st.experimental_rerun()
