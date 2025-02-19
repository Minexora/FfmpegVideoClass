from video_converter import FfmpegVideoConverterClass, Resolution,AspectRatio

if __name__ =="__main__":
    cls = FfmpegVideoConverterClass(input_file="input_video.mp4")
    cls.set_aspect_ratio(aspect_ratio=AspectRatio.AR_3_2)
    cls.convert(output_file="output.mp4")