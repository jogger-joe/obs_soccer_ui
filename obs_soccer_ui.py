import obspython as obs

def script_description():
    return "Get current video name from VLC source"

def script_update(settings):
    pass

def get_vlc_source():
    sources = obs.obs_enum_sources()
    vlc_source = None
    for source in sources:
        if obs.obs_source_get_id(source) == "vlc_source":
            vlc_source = source
            break
    obs.source_list_release(sources)
    return vlc_source

def get_vlc_source_info():
    vlc_source = get_vlc_source()
    if vlc_source:
        settings = obs.obs_source_get_settings(vlc_source)
        playlist = obs.obs_data_get_array(settings, "playlist")
        
        if playlist:
            current_item = obs.obs_data_array_item(playlist, 0)  # Assuming the first item is the current one
            value = obs.obs_data_get_string(current_item, "value")
            
            obs.obs_data_release(current_item)
            obs.obs_data_array_release(playlist)
            obs.obs_data_release(settings)
            
            return value
    
    return "No VLC source found or no video playing"

def get_current_video_progress():
    vlc_source = get_vlc_source()
    if vlc_source:
        settings = obs.obs_source_get_settings(vlc_source)
        current_time = obs.obs_data_get_int(settings, "time")
        total_time = obs.obs_data_get_int(settings, "duration")
        obs.obs_data_release(settings)
        
        if total_time > 0:
            progress = (current_time / total_time) * 100
            return f"Current progress: {progress:.2f}%"
    return "No VLC source found or no video playing"

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "button1", "Get Current Video", get_current_video_callback)
    obs.obs_properties_add_button(props, "button2", "Get Current Video Progress", get_current_video_progress_callback)
    return props

def get_current_video_callback(props, prop):
    video_name = get_vlc_source_info()
    print(f"Current video: {video_name}")
    return True

def get_current_video_progress_callback(props, prop):
    video_progress = get_current_video_progress()
    print(f"Current video-progress: {video_progress}")
    return True