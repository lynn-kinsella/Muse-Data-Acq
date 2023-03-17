mkdir Split_clips
ffmpeg -i $1 -c copy -map 0 -segment_time 00:05:00 -f segment -reset_timestamps 1 Split_clips/$2_%03d.mp4
