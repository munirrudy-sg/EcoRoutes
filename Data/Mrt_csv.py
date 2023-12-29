import requests
import csv
import pandas as pd


all_results = []
unwanted = ['EXIT','UOB','DBS','OCBC','DEPOT']

def get_MRT_data():
    # Define OneMap API endpoint URL and parameters
    url = 'https://developers.onemap.sg/commonapi/search?searchVal=MRT&returnGeom=Y&getAddrDetails=N'

    # Include your OneMap API key as a header
    headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwMzcxLCJ1c2VyX2lkIjoxMDM3MSwiZW1haWwiOiIyMjAxMjI2QHNpdC5zaW5nYXBvcmV0ZWNoLmVkdS5zZyIsImZvcmV2ZXIiOmZhbHNlLCJpc3MiOiJodHRwOlwvXC9vbTIuZGZlLm9uZW1hcC5zZ1wvYXBpXC92MlwvdXNlclwvc2Vzc2lvbiIsImlhdCI6MTY4NTExNDc3NiwiZXhwIjoxNjg1NTQ2Nzc2LCJuYmYiOjE2ODUxMTQ3NzYsImp0aSI6ImQ0NDg2ZTgxNjhkODJjNzVlY2EwMzg1MTBiN2I1ZGI5In0.PCG-xbtdn4Plt1mNrJayJygv98Aa9HIOgcmuqVb5d8Q'}

    # Initialize variables
    pageNum = 1
    totalResults = 0
    

    # Send HTTP GET request to OneMap API endpoint URL
    # Paginate through results to extract MRT station data
    while True:
        # Update API endpoint URL with current pageNum
        response = requests.get(f'{url}&pageNum={pageNum}', headers=headers)
        
        # Parse response content to extract MRT station data
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            numResults = len(results)
            totalResults += numResults
            # Loop through results to extract MRT station coordinates
            for result in results:
                if not any(word in result['SEARCHVAL'] for word in unwanted):
                    all_results.append(result)

            # Check if all results have been retrieved
            if numResults == 0 or pageNum >= data['totalNumPages']:
                break
            
            # Increment pageNum for next request
            pageNum += 1
        
        else:
            print('Error:', response.status_code)
    return all_results

def get_LRT_data():
    # Define OneMap API endpoint URL and parameters
    url_LRT = 'https://developers.onemap.sg/commonapi/search?searchVal=LRT\&returnGeom=Y&getAddrDetails=N'   

    # Include your OneMap API key as a header
    headers = {'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwMzcxLCJ1c2VyX2lkIjoxMDM3MSwiZW1haWwiOiIyMjAxMjI2QHNpdC5zaW5nYXBvcmV0ZWNoLmVkdS5zZyIsImZvcmV2ZXIiOmZhbHNlLCJpc3MiOiJodHRwOlwvXC9vbTIuZGZlLm9uZW1hcC5zZ1wvYXBpXC92MlwvdXNlclwvc2Vzc2lvbiIsImlhdCI6MTY4NTExNDc3NiwiZXhwIjoxNjg1NTQ2Nzc2LCJuYmYiOjE2ODUxMTQ3NzYsImp0aSI6ImQ0NDg2ZTgxNjhkODJjNzVlY2EwMzg1MTBiN2I1ZGI5In0.PCG-xbtdn4Plt1mNrJayJygv98Aa9HIOgcmuqVb5d8Q'}

    # Initialize variables
    pageNum = 1
    totalResults = 0
    # Send HTTP GET request to OneMap API endpoint URL
    # Paginate through results to extract MRT station data
    while True:
        # Update API endpoint URL with current pageNum
        response = requests.get(f'{url_LRT}&pageNum={pageNum}', headers=headers)
        
        # Parse response content to extract MRT station data
        if response.status_code == 200:
            data = response.json()
            results = data['results']
            numResults = len(results)
            totalResults += numResults
            # Loop through results to extract MRT station coordinates
            for result in results:
                if not any(word in result['SEARCHVAL'] for word in unwanted):
                    all_results.append(result)

            # Check if all results have been retrieved
            if numResults == 0 or pageNum >= data['totalNumPages']:
                break
            
            # Increment pageNum for next request
            pageNum += 1
        
        else:
            print('Error:', response.status_code)
    return all_results

def write_Dataframe():
    # Create an empty dataframe with the desired columns
    columns = ['STN_NAME', 'STN_NO', 'X', 'Y', 'Latitude', 'Longitude']
    dataframe = pd.DataFrame(columns=columns)

    # Loop through results to extract MRT station coordinates
    get_MRT_data()
    results = get_LRT_data()
    for result in results:
        name_parts = result['SEARCHVAL'].split(' (')
        if len(name_parts) < 2:
            # Skip entries without parentheses in the name
            continue
        name = name_parts[0]
        line_order = name_parts[1].replace(')', '')

        # Check if line_order contains multiple line and order values
        if '/' in line_order:
            line_parts = line_order.split(' / ')
            for line_part in line_parts:
                

                # Create a temporary dataframe for each line and order combination
                data = {
                    'STN_NAME': [name],
                    'STN_NO': [line_part],
                    'X': [result['X']],
                    'Y': [result['Y']],
                    'Latitude': [result['LATITUDE']],
                    'Longitude': [result['LONGITUDE']]
                }
                temp_dataframe = pd.DataFrame(data)

                # Concatenate the temporary dataframe with the main dataframe
                dataframe = pd.concat([dataframe, temp_dataframe], ignore_index=True)
        else:
            if any(char.isdigit() for char in line_order):
                line = line_order[:2]
                order = line_order[2:] if line_order[2:].isdigit() else '0'
            else:
                line = line_order
                order = '0'

            # Append the data to the dataframe
            data = {
                'STN_NAME': [name],
                'STN_NO': f"{line}{order}",
                'X': [result['X']],
                'Y': [result['Y']],
                'Latitude': [result['LATITUDE']],
                'Longitude': [result['LONGITUDE']]
            }
            temp_dataframe = pd.DataFrame(data)

            # Concatenate the temporary dataframe with the main dataframe
            dataframe = pd.concat([dataframe, temp_dataframe], ignore_index=True)

    #drop unwanted/ under construction
    #DT36,DT37, TE21,23,24,25,26,27,28,29,30,31 CC19,30,31,32 ne18   // S30,S40 
    unwanted_stations = ["DT36","DT37","TE10","TE21","TE23","TE24","TE25","TE26","TE27","TE28","TE29","TE30","TE31","CC18","CC30","CC31","CC32","NE18","S30","S40"]
    # remove cck LRT as is same as mrt 
    mRT_AND_LRT= ["CHOA CHU KANG LRT STATION","BUKIT PANJANG LRT STATION","SENGKANG LRT STATION","PUNGGOL LRT STATION"]
    dataframe.loc[dataframe['STN_NAME'] == 'CHOA CHU KANG MRT STATION', 'STN_NO'] = dataframe.loc[dataframe['STN_NAME'] == 'CHOA CHU KANG MRT STATION', 'STN_NO'] + '/BP1'
    dataframe.loc[dataframe['STN_NAME'] == 'BUKIT PANJANG MRT STATION', 'STN_NO'] = dataframe.loc[dataframe['STN_NAME'] == 'BUKIT PANJANG MRT STATION', 'STN_NO'] + '/BP6'
    dataframe.loc[dataframe['STN_NAME'] == 'TANAH MERAH MRT STATION', 'STN_NO'] = dataframe.loc[dataframe['STN_NAME'] == 'TANAH MERAH MRT STATION', 'STN_NO'] + '/CG0'
    dataframe.loc[dataframe['STN_NAME'] == 'SENGKANG MRT STATION', 'STN_NO'] = dataframe.loc[dataframe['STN_NAME'] == 'SENGKANG MRT STATION', 'STN_NO'] + '/STC'
    dataframe.loc[dataframe['STN_NAME'] == 'PUNGGOL MRT STATION', 'STN_NO'] = dataframe.loc[dataframe['STN_NAME'] == 'PUNGGOL MRT STATION', 'STN_NO'] + '/PTC'
    dataframe = dataframe[~dataframe['STN_NO'].isin(unwanted_stations)]
    dataframe = dataframe[~dataframe['STN_NAME'].isin(mRT_AND_LRT)]

    dataframe.to_csv('MRT Stations.csv', sep=',',index=False)
    print("done")
    return dataframe
