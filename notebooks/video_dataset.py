
        #################################################
        ### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
        #################################################
        # file to edit: 03_video_dataset.ipynb

from visionmod.utils import list_dir
from visionmod.folder import make_dataset
from visionmod.video_utils import VideoClips
from torchvision.datasets.vision import VisionDataset

class VideoDataset(VisionDataset):
    """
    Parameters
    ----------
        root : string
            Root directory of the dataset.

        frames_per_clip : int
            No. of frames in per video

        step_between_clips : int
            Difference between the starting frame of each subclip

        frame_stride : int
            Step between frames within a subclip. For example, with `frame_stride=2`, a
            `num_frames=16` subclip gets downsized to `16 // 2 = 8`

        tfms_torch (callable, optional)
            A function/transform that  takes in a (T,H,W,C) video
            and returns a transformed version with shape (C,T,H,W).

        tfms_albu (callable, optional)
            An albumentations video transformation function that takes in
            (C,T,H,W) and outputs (C,T,H,W)

    Returns
    -------
        video : Tensor[T, H, W, C]
            Tensor of shape (T, H, W, C) where `T = num_frames`

        audio : Tensor[K, L]:
            the audio frames, where `K` is the number of channels
            and `L` is the number of points

        label : int
            class of the video clip
    """

    def __init__(self, root, frames_per_clip=32, step_between_clips=1, frame_stride=1, frame_rate=None,
                 extensions=('mp4',), tfms_torch=None, tfms_albu=None, _precomputed_metadata=None,
                 num_workers=1, _video_width=0, _video_height=0,
                 _video_min_dimension=0, _audio_samples=0):
        super(VideoDataset, self).__init__(root)

        classes      = list(sorted(list_dir(root)))
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        self.samples = make_dataset(self.root, class_to_idx, extensions, is_valid_file=None)
        self.classes = classes
        video_list   = [x[0] for x in self.samples]
        self.video_clips = VideoClips(
            video_list,
            frames_per_clip,
            step_between_clips,
            frame_stride,
            frame_rate,
            _precomputed_metadata,
            num_workers=num_workers,
            _video_width=_video_width,
            _video_height=_video_height,
            _video_min_dimension=_video_min_dimension,
            _audio_samples=_audio_samples,
        )
        self.tfms_torch = tfms_torch
        self.tfms_albu  = tfms_albu

    @property
    def metadata(self):
        return self.video_clips.metadata

    def get_info(self):
        import pandas as pd
        fnames     = [f.rsplit('/')[-1] for f   in self.video_clips.metadata['video_paths']]
        classes    = [f.rsplit('/')[-2] for f   in self.video_clips.metadata['video_paths']]
        num_frames = [len(pts)          for pts in self.video_clips.metadata['video_pts']]
        fps        = [i                 for i   in self.video_clips.metadata['video_fps']]
        subclips   = [len(x)            for x   in self.video_clips.clips]

        info = pd.DataFrame(data    = list(zip(fnames, classes, num_frames, fps, subclips)),
                            columns = ['Filename', 'Class', '# Frames', 'FPS', '# Subclips'])
        return info

    def __len__(self):
        return self.video_clips.num_clips()

    def __getitem__(self, idx):
        video, audio, info, video_idx = self.video_clips.get_clip(idx)
        label = self.samples[video_idx][1]

        if self.tfms_albu is None: self.tfms = A.Compose([])
        if self.tfms_torch is not None:
            video = apply_tfms_albu(self.tfms_torch(video), self.tfms_albu)

        return video, audio, label