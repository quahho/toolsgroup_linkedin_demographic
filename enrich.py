
# Import libraries
import streamlit as st
import numpy as np
import pandas as pd
from random import randint


# Function to obtain campaign dataframe
def getCampaignData(campaign_list) :

    # Anticipate errors in the code below
    try :

        # Read file content into a dataframe
        df = pd.read_csv(campaign_list)

        # When file's columns doesnt match expected columns
        if list(df.columns) != ['Campaign ID', 'Campaign Name'] :

            # Display error message
            st.error('Invalid file content. Please ensure file contains *Campaign ID* and *Campaign Name* fields.')

            # Escape function
            return []

        # When file does not contain any campaign data but the field names are present
        elif df.empty :

            # Display error message
            st.error('Missing file content. Please ensure file contains records of *Campaign ID* and *Campaign Name*.')

            # Escape function
            return []
            
        # When file contains duplicate combinations of campaign id and campaign name
        elif len(df[df.duplicated()]) > 0 :

            # Display error message
            st.error('There are duplicate combinations of *Campaign ID* and *Campaign Name* found.')

            # Escape function
            return []

        # When file's columns matches expected columns
        else :

            # Hide uploaded campaign list
            with st.expander('*View uploaded campaign list*'):

                # Set index to start from 1
                df.index += 1
                
                # Display dataframe
                st.dataframe(df)

            # Return dataframe
            return df

    # When the file is completely empty
    except pd.errors.EmptyDataError :

        # Display error message
        st.error('There is nothing in this file, please ensure there is content in file.')

        # Escape function
        return []

    # When the file is not a perfect table
    except pd.errors.ParserError :

        # Display error message
        st.error('Invalid file content. Please ensure file contains *Campaign ID* and *Campaign Name* fields.')

        # Escape function
        return []


# Function to end process - for start button
def endProcess() :

    # Enable pressed start trigger
    st.session_state['process_ended'] = True

    # Enable pressed start trigger
    st.session_state['export_now'] = False

    # Change the key of the file uploader
    st.session_state['file_upload'] = str(randint(1000, 100000000))

    # Rerun the page
    st.experimental_rerun()


# Function to proceed to export
def proceedExport() :

    # Enable pressed start trigger
    st.session_state['export_now'] = True


# Function to add the necessary columns
def addColumns(df, campaign_id, extract_date) :
    
    # Add the necessary columns
    df['Campaign ID'] = campaign_id
    df['Extract Date'] = extract_date

    # Return modified dataframe
    return df


# Function to enrich data
def enrichCSV(uploaded_file, campaign_choice, campaign_id, extract_date) :

    # Try block for reading data in
    try : 

        # Read csv
        df = pd.read_csv(
                uploaded_file, 
                sep = '\t',
                encoding = 'utf-16',
                skiprows = 4,
                skip_blank_lines = True
            )
        
        # Get all index where there is an empty row
        null_index_list = df.index[df['Company Name Segment'].isnull()].tolist()

    # When there is error
    except : 

        # Display error message
        st.error('Error in reading data from the CSV file.')

        # Escape function  
        return False
    
    # Try block for reading data in
    try : 

        # ======================================================================================================

        # Get company name data
        company_name_df = df.iloc[:null_index_list[0]] 

        # Add columns to dataframe
        company_name_df = addColumns(company_name_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['company_name_data']) == 0 :

            # Assign the first dataframe
            st.session_state['company_name_data'] = company_name_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['company_name_data']

            # Append new dataframe to the old dataframe
            st.session_state['company_name_data'] = pd.concat([old_df, company_name_df], ignore_index = True)

        # ======================================================================================================

        # Get company industry data
        company_industry_df = df.iloc[(null_index_list[0] + 1):null_index_list[1]] 

        # Set first row of data as columns
        company_industry_df.columns = company_industry_df.iloc[0]
        
        # Remove first row of data
        company_industry_df = company_industry_df[1:]

        # Add columns to dataframe
        company_industry_df = addColumns(company_industry_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['company_industry_data']) == 0 :

            # Assign the first dataframe
            st.session_state['company_industry_data'] = company_industry_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['company_industry_data']

            # Append new dataframe to the old dataframe
            st.session_state['company_industry_data'] = pd.concat([old_df, company_industry_df], ignore_index = True)

        # ======================================================================================================

        # Get company size data
        company_size_df = df.iloc[(null_index_list[1] + 1):null_index_list[2]] 

        # Set first row of data as columns
        company_size_df.columns = company_size_df.iloc[0]
        
        # Remove first row of data
        company_size_df = company_size_df[1:]

        # Add columns to dataframe
        company_size_df = addColumns(company_size_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['company_size_data']) == 0 :

            # Assign the first dataframe
            st.session_state['company_size_data'] = company_size_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['company_size_data']

            # Append new dataframe to the old dataframe
            st.session_state['company_size_data'] = pd.concat([old_df, company_size_df], ignore_index = True)

        # ======================================================================================================

        # Get country region data
        country_region_df = df.iloc[(null_index_list[2] + 1):null_index_list[3]] 

        # Set first row of data as columns
        country_region_df.columns = country_region_df.iloc[0]
        
        # Remove first row of data
        country_region_df = country_region_df[1:]

        # Add columns to dataframe
        country_region_df = addColumns(country_region_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['country_region_data']) == 0 :

            # Assign the first dataframe
            st.session_state['country_region_data'] = country_region_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['country_region_data']

            # Append new dataframe to the old dataframe
            st.session_state['country_region_data'] = pd.concat([old_df, country_region_df], ignore_index = True)

        # ======================================================================================================

        # Get location data
        location_df = df.iloc[(null_index_list[3] + 1):null_index_list[4]] 

        # Set first row of data as columns
        location_df.columns = location_df.iloc[0]
        
        # Remove first row of data
        location_df = location_df[1:]

        # Add columns to dataframe
        location_df = addColumns(location_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['location_data']) == 0 :

            # Assign the first dataframe
            st.session_state['location_data'] = location_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['location_data']

            # Append new dataframe to the old dataframe
            st.session_state['location_data'] = pd.concat([old_df, location_df], ignore_index = True)

        # ======================================================================================================

        # Get job seniority data
        job_seniority_df = df.iloc[(null_index_list[4] + 1):null_index_list[5]] 

        # Set first row of data as columns
        job_seniority_df.columns = job_seniority_df.iloc[0]
        
        # Remove first row of data
        job_seniority_df = job_seniority_df[1:]

        # Add columns to dataframe
        job_seniority_df = addColumns(job_seniority_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['job_seniority_data']) == 0 :

            # Assign the first dataframe
            st.session_state['job_seniority_data'] = job_seniority_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['job_seniority_data']

            # Append new dataframe to the old dataframe
            st.session_state['job_seniority_data'] = pd.concat([old_df, job_seniority_df], ignore_index = True)

        # ======================================================================================================

        # Get job title data
        job_title_df = df.iloc[(null_index_list[5] + 1):null_index_list[6]] 

        # Set first row of data as columns
        job_title_df.columns = job_title_df.iloc[0]
        
        # Remove first row of data
        job_title_df = job_title_df[1:]

        # Add columns to dataframe
        job_title_df = addColumns(job_title_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['job_title_data']) == 0 :

            # Assign the first dataframe
            st.session_state['job_title_data'] = job_title_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['job_title_data']

            # Append new dataframe to the old dataframe
            st.session_state['job_title_data'] = pd.concat([old_df, job_title_df], ignore_index = True)

        # ======================================================================================================

        # Get job function data
        job_function_df = df.iloc[(null_index_list[6] + 1):null_index_list[7]] 

        # Set first row of data as columns
        job_function_df.columns = job_function_df.iloc[0]
        
        # Remove first row of data
        job_function_df = job_function_df[1:]

        # Add columns to dataframe
        job_function_df = addColumns(job_function_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['job_function_data']) == 0 :

            # Assign the first dataframe
            st.session_state['job_function_data'] = job_function_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['job_function_data']

            # Append new dataframe to the old dataframe
            st.session_state['job_function_data'] = pd.concat([old_df, job_function_df], ignore_index = True)

        # ======================================================================================================

        # Get county data
        county_df = df.iloc[(null_index_list[7] + 1):null_index_list[8]] 

        # Set first row of data as columns
        county_df.columns = county_df.iloc[0]
        
        # Remove first row of data
        county_df = county_df[1:]

        # Add columns to dataframe
        county_df = addColumns(county_df, campaign_id, extract_date)

        # When there is no data for this segment
        if len(st.session_state['county_data']) == 0 :

            # Assign the first dataframe
            st.session_state['county_data'] = county_df

        # When there is data for this segment
        else :

            # Get existing dataframe
            old_df = st.session_state['county_data']

            # Append new dataframe to the old dataframe
            st.session_state['county_data'] = pd.concat([old_df, county_df], ignore_index = True)

        # ======================================================================================================

        # Add campaign choice to list of covered campaign
        st.session_state['campaign_covered'].append(campaign_choice)

        # Create output dictionary
        dict_of_lists = {
            'Campaign Name': st.session_state['campaign_covered']
        }

        # Create output dataframe
        output_table = pd.DataFrame(dict_of_lists)

        # Start table from index 1
        output_table.index += 1

        # Set session output table
        st.session_state['output_table'] = output_table

        # Mark the end of successful completion
        return True


    # When there is error
    except : 

        # Display error message
        st.error('Error in splitting data from the CSV file.')

        # Escape function
        return False



