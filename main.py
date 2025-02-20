from video_converter import FfmpegVideoConverterClass, Resolution, AspectRatio,FfmpegPreset,VideoCodec

if __name__ == "__main__":
    cls = FfmpegVideoConverterClass(input_file="input_video.mp4")
    cls.set_aspect_ratio(aspect_ratio=AspectRatio.AR_2_39_1)
    # cls.trim_video(start_time="00:00:00", end_time="00:00:15")
    # cls.set_resolution(resolution=Resolution.R_360P)
    # cls.compress_video(crf=23, codec=VideoCodec.H264, preset=FfmpegPreset.SLOW)
    cls.mirror()
    cls.convert(output_file="output.mp4")
