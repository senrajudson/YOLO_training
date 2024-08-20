import numpy as np
import cv2
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import os
from datetime import datetime
import time

class ConcatFramesNumpy:
    def __init__(self):
        self._file_path = None
        self._output_folder = None
        self._read_frames = None

    @property
    def read_frame(self):
        # if os.path.isdir(self._read_frames):
        if isinstance(self._read_frames, str):
            files = os.listdir(self._read_frames)
            files = (sorted(files))

            frames_list = []
            for file in files:
                img = cv2.imread(os.path.join(self._read_frames, file))
                frames_list.append(img)
        
        else:
            raise ValueError("Values does not match.")

        return frames_list

    @read_frame.setter
    def read_frame(self, file):
        self._read_frames = file

    @property
    def output_folder(self):
        return self._output_folder
    
    @output_folder.setter
    def output_folder(self, path):
        self._output_folder = path

    def concat_frames(self, frames, concat_num):

        concat_frames = []
        for i in range(0, len(frames), concat_num):
            image1 = frames[i]
            image2 = frames[i + 1]
            concatenated_image = np.concatenate((image1, image2), axis=0)
            concat_frames.append(concatenated_image)
        
        return concat_frames

    def save(self, file, video_name="video", data=False):
        if data == True:
            data_formatada = datetime.fromtimestamp(time.time()).strftime('%Y-%d-%m_%H.%M.%S')
            nome_dir = data_formatada+"_"+self.output_folder
            if isinstance(file, list):
                if self.output_folder is None:
                    raise ValueError("Output folder path is not set.")
                os.makedirs(f"{nome_dir}", exist_ok=True)

                for i, frame in enumerate(file):
                    frame_filename = os.path.join(f"../../{nome_dir}", f'frame_{i:04d}.jpg')
                    cv2.imwrite(frame_filename, frame)

            if isinstance(file, ImageSequenceClip):
                os.makedirs(f"../../{self.output_folder}", exist_ok=True)
                file.write_videofile(f'../../{self.output_folder}/{video_name}.mp4')
        else:
            if isinstance(file, list):
                if self.output_folder is None:
                    raise ValueError("Output folder path is not set.")
                os.makedirs(f"{self.output_folder}", exist_ok=True)

                for i, frame in enumerate(file):
                    frame_filename = os.path.join(f"../../{self.output_folder}", f'frame_{i:04d}.jpg')
                    cv2.imwrite(frame_filename, frame)

            if isinstance(file, ImageSequenceClip):
                os.makedirs(f"../../{self.output_folder}", exist_ok=True)
                file.write_videofile(f'../../{self.output_folder}/{video_name}.mp4')


    def convert_vid(self, frames, fps=30):
        clip = ImageSequenceClip(frames, fps=fps)

        return clip
    
    def matrix_color(self, frames, type):
        if type=="BGR>RGB":
            change_matrix = cv2.COLOR_BGR2RGB
        elif type=="BGR>GRAY":
            change_matrix = cv2.COLOR_BGR2GRAY
        elif type=="RGB>GRAY":
            change_matrix = cv2.COLOR_RGB2GRAY

        new_frame_list = []
        for frame in frames:
            new_frame_color = cv2.cvtColor(frame, change_matrix)
            new_frame_list.append(new_frame_color)

        return new_frame_list
        
