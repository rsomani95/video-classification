
        #################################################
        ### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
        #################################################
        # file to edit: 04_samplers.ipynb

import torch
class RandomClipSampler(torch.utils.data.Sampler):
    """
    Samples at most `max_video_clips_per_video` clips for each video randomly

    Arguments:
        video_clips (VideoClips): video clips to sample from
        max_clips_per_video (int): maximum number of clips to be sampled per video
    """
    def __init__(self, video_clips, max_clips_per_video):
        #if not isinstance(video_clips, visionmod.video_utils.VideoClips):
        #    raise TypeError("Expected video_clips to be an instance of VideoClips, "
        #                    "got {}".format(type(video_clips)))
        self.video_clips = video_clips
        self.max_clips_per_video = max_clips_per_video

    def __iter__(self):
        idxs = []
        s = 0
        # select at most max_clips_per_video for each video, randomly
        for c in self.video_clips.clips:
            length = len(c)
            size = min(length, self.max_clips_per_video)
            sampled = torch.randperm(length)[:size] + s
            s += length
            idxs.append(sampled)
        idxs = torch.cat(idxs)
        # shuffle all clips randomly
        perm = torch.randperm(len(idxs))
        idxs = idxs[perm].tolist()
        return iter(idxs)

    def __len__(self):
        return sum(min(len(c), self.max_clips_per_video) for c in self.video_clips.clips)


class UniformClipSampler(torch.utils.data.Sampler):
    """
    Sample `num_video_clips_per_video` clips for each video, equally spaced.
    When number of unique clips in the video is fewer than num_video_clips_per_video,
    repeat the clips until `num_video_clips_per_video` clips are collected
    Arguments:
        video_clips (VideoClips): video clips to sample from
        num_clips_per_video (int): number of clips to be sampled per video
    """
    def __init__(self, video_clips, num_clips_per_video):
        #if not isinstance(video_clips, torchvision.datasets.video_utils.VideoClips):
        #    raise TypeError("Expected video_clips to be an instance of VideoClips, "
        #                    "got {}".format(type(video_clips)))
        self.video_clips = video_clips
        self.num_clips_per_video = num_clips_per_video

    def __iter__(self):
        idxs = []
        s = 0
        # select num_clips_per_video for each video, uniformly spaced
        for c in self.video_clips.clips:
            length = len(c)
            if length == 0:
                # corner case where video decoding fails
                continue

            sampled = (
                torch.linspace(s, s + length - 1, steps=self.num_clips_per_video)
                .floor()
                .to(torch.int64)
            )
            s += length
            idxs.append(sampled)
        idxs = torch.cat(idxs).tolist()
        return iter(idxs)

    def __len__(self):
        return sum(
            self.num_clips_per_video for c in self.video_clips.clips if len(c) > 0
        )



class FirstClipSampler(torch.utils.data.Sampler):
    """
    Samples at most `max_video_clips_per_video` clips for each video sequentially

    Arguments:
        video_clips (VideoClips): video clips to sample from
        max_clips_per_video (int): maximum number of clips to be sampled per video
    """
    def __init__(self, video_clips, max_clips_per_video):
        #if not isinstance(video_clips, visionmod.video_utils.VideoClips):
        #    raise TypeError("Expected video_clips to be an instance of VideoClips, "
        #                    "got {}".format(type(video_clips)))
        self.video_clips = video_clips
        self.max_clips_per_video = max_clips_per_video

    def __iter__(self):
        idxs = []
        s = 0
        # select at most max_clips_per_video for each video, sequentially
        for c in self.video_clips.clips:
            length = len(c)
            size = min(length, self.max_clips_per_video)
            sampled = torch.arange(length)[:size] + s # the only change from `RandomClipSampler`
            s += length
            idxs.append(sampled)
        idxs = torch.cat(idxs)
        # shuffle all clips randomly
        perm = torch.randperm(len(idxs))
        idxs = idxs[perm].tolist()
        return iter(idxs)

    def __len__(self):
        return sum(min(len(c), self.max_clips_per_video) for c in self.video_clips.clips)

from torch.utils.data.dataloader import default_collate
def collate_fn(batch):
    # remove audio from the batch
    batch = [(d[0], d[2]) for d in batch]
    return default_collate(batch)