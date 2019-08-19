from modules import RainFallAnalyzer

if __name__ == '__main__':

    # create analyzer
    #rfa = RainFallAnalyzer.RainFallAnalyzer('D:\\work\\rain_fall_analysis')
    rfa = RainFallAnalyzer.RainFallAnalyzer('/home/.ecryptfs/napan/work/rain_fall_analysis/')
    
    rfa.calculate_average_rainfall_daily( rfa.station_name_list[2] )
    rfa.calculate_average_rainfall_monthly( rfa.station_name_list[2] )
    rfa.calculate_average_rainfall_yearly( rfa.station_name_list[2] )
    
    rfa.calculate_peak_rainfall_daily( rfa.station_name_list[2] )