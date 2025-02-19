import subprocess
from enum import Enum
from pathlib import Path
from typing import Optional, Union


class AspectRatio(Enum):
    # Standard ratios
    AR_4_3 = "4:3"
    AR_16_9 = "16:9"
    AR_8_5 = "8:5"
    AR_25_16 = "25:16"
    AR_3_2 = "3:2"
    AR_5_3 = "5:3"
    AR_5_4 = "5:4"
    AR_1_1 = "1:1"
    AR_32_9 = "32:9"  
    AR_1_85_1 = "37:20"
    AR_2_39_1 = "239:100"

    # Rotated ratios
    AR_ROTATED_3_4 = "3:4"
    AR_ROTATED_9_16 = "9:16"
    AR_ROTATED_2_3 = "2:3"
    AR_ROTATED_3_5 = "3:5"
    AR_ROTATED_4_5 = "4:5"
    AR_ROTATED_9_32 = "9:32"
    AR_ROTATED_1_85 = "20:37"
    AR_ROTATED_2_39 = "100:239"


class Resolution(Enum):
    R_2K = "2560x1440"
    R_1080P = "1920x1080"
    R_720P = "1280x720"
    R_480P = "854x480"
    R_360P = "640x360"


class FfmpegVideoConverterClass:
    """FFmpeg kullanarak video dönüştürme işlemleri yapan sınıf.
    
    :param input_file: İşlenecek video dosyasının yolu
    :type input_file: Union[str, Path]
    """

    def __init__(self, input_file: Union[str, Path]):
        self.input_file = str(input_file)
        self.ffmpeg_cmd = ["ffmpeg", "-i", self.input_file]
        self.output_options = []
        self.output_format = None

    def set_resolution(self, resolution: Resolution) -> "FfmpegVideoConverterClass":
        """Videonun çözünürlüğünü değiştirir.

        :param resolution: Yeni çözünürlük değeri
        :type resolution: Resolution

        :return: Sınıfın kendisi (method chaining için)
        :rtype: FfmpegVideoConverterClass

        .. code-block:: python
            converter.set_resolution(Resolution.R_1080P)
        """
        self.output_options.extend(["-s", resolution.value])
        return self

    def set_aspect_ratio(self, aspect_ratio: AspectRatio) -> "FfmpegVideoConverterClass":
        """Videonun en-boy oranını değiştirir.

        :param aspect_ratio: Yeni en-boy oranı
        :type aspect_ratio: AspectRatio

        :return: Sınıfın kendisi (method chaining için)
        :rtype: FfmpegVideoConverterClass

        .. code-block:: python
            converter.set_aspect_ratio(AspectRatio.AR_16_9)
        """
        self.output_options.extend(["-aspect", aspect_ratio.value])
        return self

    def add_subtitle(self, subtitle_file: Union[str, Path]) -> "FfmpegVideoConverterClass":
        """Videoya altyazı ekler.

        :param subtitle_file: Altyazı dosyasının yolu (.srt, .ass, vb.)
        :type subtitle_file: Union[str, Path]

        :return: Sınıfın kendisi (method chaining için)
        :rtype: FfmpegVideoConverterClass

        .. code-block:: python
            converter.add_subtitle("altyazi.srt")
        """
        self.output_options.extend(["-vf", f"subtitles={subtitle_file}"])
        return self

    def add_watermark(self, watermark_file: Union[str, Path], position: str = "10:10") -> "FfmpegVideoConverterClass":
        """Videoya filigran (watermark) ekler.

        :param watermark_file: Filigran olarak eklenecek görsel dosyasının yolu
        :type watermark_file: Union[str, Path]
        :param position: Filigranın konumu "x:y" formatında (piksel)
        :type position: str

        :return: Sınıfın kendisi (method chaining için)
        :rtype: FfmpegVideoConverterClass

        .. code-block:: python
            converter.add_watermark("logo.png", "10:10")
        """
        self.output_options.extend(["-vf", f"movie={watermark_file}[watermark];[in][watermark]overlay={position}[out]"])
        return self

    def trim_video(self, start_time: str, end_time: str) -> "FfmpegVideoConverterClass":
        """Videoyu belirtilen zaman aralığında keser.

        :param start_time: Başlangıç zamanı ("HH:MM:SS" formatında veya dakika olarak "10")
        :type start_time: str
        :param end_time: Bitiş zamanı ("HH:MM:SS" formatında veya dakika olarak "25")
        :type end_time: str

        :return: Sınıfın kendisi (method chaining için)
        :rtype: FfmpegVideoConverterClass

        .. code-block:: python
            # Dakika olarak kullanım
            converter.trim_video("10", "25")
            # veya
            # HH:MM:SS formatında kullanım
            converter.trim_video("00:10:00", "00:25:00")
        """
        # Eğer sadece dakika girilmişse HH:MM:SS formatına çevir
        if ":" not in start_time:
            start_time = f"00:{int(start_time):02d}:00"
        if ":" not in end_time:
            end_time = f"00:{int(end_time):02d}:00"

        self.output_options.extend(["-ss", start_time, "-to", end_time])
        return self

    def change_format(self, output_format: Optional[str] = None) -> "FfmpegVideoConverterClass":
        """Video formatını değiştirir.

        :param output_format: Yeni format (örn: "mp4", "avi", "mkv"). None ise orijinal format korunur
        :type output_format: Optional[str]

        :return: Sınıfın kendisi (method chaining için)
        :rtype: FfmpegVideoConverterClass

        .. code-block:: python
            converter.change_format("mp4")
            # veya format değiştirmeden
            converter.change_format()
        """
        if output_format:
            if not output_format.startswith("."):
                output_format = f".{output_format}"
            self.output_format = output_format
        return self

    def convert(self, output_file: Optional[Union[str, Path]] = None) -> bool:
        """Videoyu dönüştürür ve kaydeder.

        :param output_file: Çıktı dosyasının yolu. None ise orijinal dosya adı kullanılır
        :type output_file: Optional[Union[str, Path]]

        :return: İşlemin başarılı olup olmadığını belirtir
        :rtype: bool

        .. code-block:: python
            # Belirli bir dosya adıyla kaydetme
            converter.convert("output.mp4")
            # veya
            # Otomatik dosya adıyla kaydetme
            converter.convert()
            # Format değiştirme ile birlikte
            converter.change_format("mkv").convert("output.mp4")  # output.mkv olarak kaydedilir

        :raises subprocess.CalledProcessError: FFmpeg işlemi başarısız olduğunda
        """
        if output_file is None:
            input_path = Path(self.input_file)
            output_suffix = self.output_format if self.output_format else input_path.suffix
            output_file = input_path.with_suffix(output_suffix)
        else:
            # Eğer output_file belirtilmiş ve yeni format ayarlanmışsa
            if self.output_format:
                output_file = Path(output_file).with_suffix(self.output_format)
            output_file = str(output_file)
        
        final_command = self.ffmpeg_cmd + self.output_options + ["-y", str(output_file)]

        try:
            subprocess.run(final_command, check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Hata oluştu: {e.stderr.decode()}")
            return False
