from modules import RainFallAnalyzer

if __name__ == '__main__':

    # create analyzer
    rfa = RainFallAnalyzer.RainFallAnalyzer('D:\\work\\rain_fall_analysis')
    #rfa = RainFallAnalyzer.RainFallAnalyzer('/home/.ecryptfs/napan/work/rain_fall_analysis/')
    
    for index, station_name in enumerate( rfa.station_name_list ):
        rfa.calculate_average_rainfall_daily( station_name )
        rfa.calculate_average_rainfall_monthly( station_name )
        rfa.calculate_average_rainfall_yearly( station_name )
    
        rfa.calculate_peak_rainfall_daily( station_name )
        
        rfa.calculate_annual_sum( station_name )
        rfa.create_scatter_plot( station_name )
        rfa.create_line_plot( station_name )