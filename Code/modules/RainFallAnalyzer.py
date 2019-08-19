import os
from datetime import datetime

import pandas as pd 
from openpyxl import load_workbook

import matplotlib.pyplot as plt
import seaborn as sns


def get_filename_list( path ):
    ''' This function gets all .csv file in this path
    '''
    # set suffix to .csv
    suffix = ".csv"

    # list file in the path
    filenames = os.listdir( path )

    # return list of csv file
    return [ filename for filename in filenames if filename.endswith( suffix )]

def get_stationname_list( filename_list ):
    ''' This function extract station name from filename list
    '''
    return [ os.path.splitext( filename )[0] for filename in filename_list ]

def save_xls( dframe, path, sheet_name ):
    ''' This function save dataframe to excel file
    '''  
    if os.path.exists(path): 
        book = load_workbook(path)
        writer = pd.ExcelWriter(path, engine='openpyxl')
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        dframe.to_excel(writer, sheet_name )
        writer.save()
    else: 
        writer = path.ExcelWriter(path)
        dframe.to_excel(writer, sheet_name )
        writer.save() 

''' This is the main module for rainfall analysis
'''
class RainFallAnalyzer:

    def __init__ ( self, csv_path ):
        ''' This is init function for the class
        '''
        # set path
        self.path = csv_path

        # get all file name
        self.data_filename_list = get_filename_list( csv_path )

        # get all station name (based on data_filename)
        self.station_name_list = get_stationname_list( self.data_filename_list ) 
        
        # define variables
        self.dataframe = None
        self.daily_avg = None
        self.monthly_avg = None
        self.yearly_avg = None
        self.daily_peak = None
    
    def createYearMonthDay( self, station_name ):
        #converting the type of Invoice Date Field from string to datetime.
        self.dataframe[station_name]['Date'] = pd.to_datetime(self.dataframe[station_name]['Date'])

        #creating YearMonthDay field for the ease of reporting and visualization
        self.dataframe[station_name]['YearMonthDay'] =  self.dataframe[station_name]['Date'].map(lambda date: 10000*date.year + 100*date.month + date.day)
    
    def createYearMonth( self, station_name ):
        #converting the type of Invoice Date Field from string to datetime.
        self.dataframe[station_name]['Date'] = pd.to_datetime(self.dataframe[station_name]['Date'])

        #creating YearMonthDay field for the ease of reporting and visualization
        self.dataframe[station_name]['YearMonth'] =  self.dataframe[station_name]['Date'].map(lambda date: 100*date.year + date.month )
    
    def createYear( self, station_name ):
        #converting the type of Invoice Date Field from string to datetime.
        self.dataframe[station_name]['Date'] = pd.to_datetime(self.dataframe[station_name]['Date'])

        #creating YearMonthDay field for the ease of reporting and visualization
        self.dataframe[station_name]['Year'] =  self.dataframe[station_name]['Date'].map(lambda date: date.year ) 

    def calculate_average_rainfall_daily( self, station_name ):
        ''' This function calculates average rainfall daily
        '''
        
        if self.daily_avg == None:
            self.daily_avg = {}
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )
            self.createYear( station_name )

        # calculate daily average
        tmp_df_daily_avg =  self.dataframe[station_name].groupby('YearMonthDay')['Rain (mm)'].mean().reset_index()
        tmp_df_daily_avg = tmp_df_daily_avg.round(2)
        tmp_df_daily_avg['Date'] = tmp_df_daily_avg['YearMonthDay'].map( lambda date: str(date)[6:8]+'/'+str(date)[4:6]+'/'+str(date)[:4]  )
        df_daily_avg = tmp_df_daily_avg[['Date','Rain (mm)']].copy()
        df_daily_avg.rename(columns={'Rain (mm)':'Daily Avg (mm)'}, inplace=True)

        # set dataframe to dictionary
        self.daily_avg[station_name] = df_daily_avg
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )     
        
        save_xls( df_daily_avg, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Daily Average' )
    
    def calculate_average_rainfall_monthly( self, station_name ):
        ''' This function calculates average rainfall monthly
        '''
        
        if self.monthly_avg == None:
            self.monthly_avg = {}
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )
            self.createYear( station_name )
            
        # calculate monthly average
        tmp_df_monthly_avg =  self.dataframe[station_name].groupby('YearMonth')['Rain (mm)'].mean().reset_index()
        tmp_df_monthly_avg = tmp_df_monthly_avg.round(2)
        tmp_df_monthly_avg['Month'] = tmp_df_monthly_avg['YearMonth'].map( lambda date: str(date)[4:6]+'/'+str(date)[:4]  )
        df_monthly_avg = tmp_df_monthly_avg[['Month','Rain (mm)']].copy()
        df_monthly_avg.rename(columns={'Rain (mm)':'Daily Avg (mm)'}, inplace=True)
        
        # set dataframe to dictionary
        self.monthly_avg[station_name] = df_monthly_avg
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )       

        save_xls( df_monthly_avg, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Monthly Average' )

    def calculate_average_rainfall_yearly( self, station_name ):
        ''' This function calculates average rainfall monthly
        '''
        
        if self.yearly_avg == None:
            self.yearly_avg = {}
            
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )
            self.createYear( station_name )
            
        # calculate monthly average
        tmp_df_yearly_avg =  self.dataframe[station_name].groupby('Year')['Rain (mm)'].mean().reset_index()
        tmp_df_yearly_avg = tmp_df_yearly_avg.round(2)
        tmp_df_yearly_avg['Year'] = tmp_df_yearly_avg['Year'].map( lambda date: str(date)  )
        df_yearly_avg = tmp_df_yearly_avg[['Year','Rain (mm)']].copy()
        df_yearly_avg.rename(columns={'Rain (mm)':'Daily Avg (mm)'}, inplace=True)
        
        # set dataframe to dictionary
        self.yearly_avg[station_name] = df_yearly_avg
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )       

        save_xls( df_yearly_avg, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Yearly Average' )


    def calculate_peak_rainfall_daily( self, station_name ):
        ''' This function calculates average rainfall daily
        '''
        
        if self.daily_peak == None:
            self.daily_peak = {}
        
        # filename
        filename = station_name + '.csv'
        assert filename in self.data_filename_list

        # read csv using pandas
        if self.dataframe == None:
            self.dataframe = {}
        if station_name not in self.dataframe.keys():
            # read data from csv 
            self.dataframe[station_name] = pd.read_csv( os.path.join( self.path, filename ) )

            # group data by date, month(year-month), year
            self.createYearMonthDay( station_name )    
            self.createYearMonth( station_name )
            self.createYear( station_name )

        # calculate daily average
        tmp_df_daily_peak =  self.dataframe[station_name].groupby('YearMonthDay')['Rain (mm)'].max().reset_index()
        tmp_df_daily_peak = tmp_df_daily_peak.round(2)
        tmp_df_daily_peak['Date'] = tmp_df_daily_peak['YearMonthDay'].map( lambda date: str(date)[6:8]+'/'+str(date)[4:6]+'/'+str(date)[:4]  )
        df_daily_peak = tmp_df_daily_peak[['Date','Rain (mm)']].copy()
        df_daily_peak.rename(columns={'Rain (mm)':'Daily Avg (mm)'}, inplace=True)

        # set dataframe to dictionary
        self.daily_peak[station_name] = df_daily_peak
        
        if not os.path.exists( os.path.join( self.path, 'result_xlsx') ):
            os.mkdir(os.path.join( self.path, 'result_xlsx') )     
        
        save_xls( df_daily_peak, os.path.join( self.path, 'result_xlsx', station_name+'.xlsx' ), 'Daily Peak' )
         