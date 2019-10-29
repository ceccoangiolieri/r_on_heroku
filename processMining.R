  
  data <- readr::read_csv('/Users/francescobranda/Desktop/dataset_disco.csv')
  
  # change timestamp to date var
  data$starttimestamp = as.POSIXct(data$'Start Timestamp', 
                                   format = "%Y/%m/%d %H:%M:%S")
  
  data$endtimestamp = as.POSIXct(data$'Complete Timestamp', 
                                 format = "%Y/%m/%d %H:%M:%S")
  
  # remove blanks from var names
  names(data) <- str_replace_all(names(data), c(" " = "_" , "," = "" ))
  
  
  # transform data into eventlog
  events <- bupaR::activities_to_eventlog(
    head(data, n = 10000),
    case_id = 'Case_ID',
    activity_id = 'Activity',
    resource_id = 'Resource',
    timestamps = c('starttimestamp', 'endtimestamp')
  )
  
  events <- bupaR::activities_to_eventlog(
    data,
    case_id = 'Case_ID',
    activity_id = 'Activity',
    resource_id = 'Resource',
    timestamps = c('starttimestamp', 'endtimestamp')
  )
  
  
  # process map ####
  events %>%
    filter_activity_frequency(percentage = 1.0) %>% # show only most frequent activities
    filter_trace_frequency(percentage = .80) %>%    # show only the most frequent traces
    process_map(render = F) %>% 
    export_graph(file_name = 'static/processMap.svg',
                 file_type = 'SVG') 
    
  
   
processmonitR::activity_dashboard(events)  
  
