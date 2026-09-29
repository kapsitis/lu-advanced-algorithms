---
layout: default
title: "Video Compression"
lang: en
permalink: /lectures/lossy_video/en/
---
# 6. Video Compression

## Introduction

Compressing video content requires two codecs -- one for audio and one for video. Some codecs are widespread enough to serve as standards, contain modern ideas (a good balance between compression speed, file size and quality), can be played in web browsers and various other environments, and can also be edited with open-source software.

In this lecture we look at the audio codecs **MP3** and **Opus** and the video codecs **H.264** and **VP9** (as well as its successor AV1). H.264 and MP3 were the most popular standards in earlier decades; all the key compression ideas already appeared in them, and they spread thanks to the Napster and BitTorrent file-sharing movements. VP9 (and AV1) and Opus are open, royalty-free modern codecs used by browsers and video calls.

### Files, Containers and Codecs

When talking about media files, three things must be distinguished:

* The **file extension** (`.mp4`, `.webm`, `.mp3`, …) is only part of the file name -- a hint of what kind of content the file *might* contain. Programs use it to choose a player, but the extension can also be misleading.
* A **container** is a file format that combines (*multiplexes*) several *streams* -- video, one or more audio tracks, subtitles -- into one file or stream and adds timestamps so that they play in sync, metadata (title, language) and an index for jumping quickly to any position. The container itself does not compress the data.
* A **codec** (*coder–decoder*) is the compression algorithm and format of one stream: the encoder turns uncompressed frames or audio samples into a bit string, and the decoder turns it back.

The same codec can be put into different containers, and one container can hold different codecs. Therefore the extension alone does not tell whether a device will play a file -- one must know which codecs are inside. This can be found out, for example, with `ffprobe file.mp4` (or the MediaInfo program).

| Container | Extension | Typical video codecs | Typical audio codecs | Where used |
| --- | --- | --- | --- | --- |
| MP4 (MPEG-4 Part 14) | `.mp4`, `.m4a` | H.264, H.265, AV1 | AAC, Opus | almost everywhere: phones, streaming, social networks |
| WebM (a subset of Matroska) | `.webm` | VP8, VP9, AV1 | Opus, Vorbis | browsers (HTML5 video), YouTube |
| Matroska (MKV) | `.mkv`, `.mka` | any | any | movies with several audio tracks, subtitles, chapters |
| Ogg | `.ogg`, `.opus` | (rarely) | Opus, Vorbis, FLAC | audio files |
| IVF | `.ivf` | VP8, VP9, AV1 | -- | the simplest video container: a single video stream without audio; for codec tests and research (see "VP9 Coding") |

AVI (Microsoft, `.avi`; often with the DivX or Xvid codec), MOV (Apple QuickTime, `.mov`), FLV (Flash Video) and 3GP (3G mobile phones) used to be popular as well. Some formats are both a codec and a file format: an `.mp3` file simply contains MP3 frames one after another (and possibly ID3 metadata), without a real container.

**Remuxing and transcoding.** If only the container changes (*remux*), the bits of the streams can be copied unchanged (`ffmpeg -i input.webm -c copy output.mkv`): this is fast and does not change quality. If the codec has to change (*transcode*), the stream must be decoded and encoded again: this is slow, and for a lossy codec every repeated encoding degrades quality (*generation loss*).

### Models of Vision and Hearing: Where the Savings Come From

Compression saves bits in two ways. First, it removes *statistical redundancy*: neighboring pixels and consecutive frames are similar, so they can be predicted and only the difference encoded -- lossless methods do this too. Second, lossy compression discards what is *perceptually irrelevant* (*irrelevance*): information whose absence a person will not notice. Models of vision and hearing determine what exactly is irrelevant.

#### Vision (the HVS Model)

The *Human Visual System* (HVS) model is an averaged model of human vision created for image and audio processing.

Visual perception is formed by rods and cones; the model assumes that the resolution of the rods is twice as good. Therefore the black-and-white component of the image (the light intensity, independent of color) must be reproduced precisely, while colors may have a lower resolution.

At the dawn of color television there was a saying: "Chrominance is at half resolution of luminance".

Video codecs use the following properties of vision:

* **chroma at a lower resolution** -- 4:2:0 subsampling (see the JPEG lecture) reduces the color data $4$ times;
* **high spatial frequencies** (fine details, noise) are perceived more weakly, so the corresponding DCT coefficients are quantized more coarsely;
* **in textures and motion** errors are noticed less than in smooth areas (sky, skin), so the encoder can spend more bits on smooth areas (adaptive quantization);
* **frame rate**: $24$--$30$ frames per second already give the impression of continuous motion (see below).

#### Flicker Frequency

Flicker is an effect caused by switching frames. Film recording: 24 frames per second (and the legends about the 25th frame). To reduce the sensation of flicker, frames are repeated (usually unchanged), so that the picture flickers 48 or 72 times per second.

Television recordings have 25 or 30 frames per second; the flicker is often twice as frequent (50 Hz or 60 Hz), using "interlacing" -- only part of the pixel rows is redrawn each time. Cathode-ray tubes flicker at 50 Hz or 60 Hz (they regularly change the light intensity); people can notice such flicker.

#### Hearing

Audio codecs use the facts that people hear only frequencies from about $20$ Hz to $20$ kHz, that a loud sound masks quieter sounds of a nearby frequency (*frequency masking*) and sounds immediately before or after it (*temporal masking*), and that both ears usually hear a very similar signal (*stereo*). These properties are discussed in more detail in the section "Audio Coding".

## Audio Coding

Audio codecs compress sound using the fact that human hearing is not perfect: it does not perceive frequencies that are too high, quiet sounds next to loud ones, or short noises immediately before or after a loud sound. First we look at common concepts, then at two codecs: the historically important MP3 and the modern Opus.

### Basics of Audio Compression

#### Sampling and the Nyquist Theorem

Sound is oscillation of air pressure. A microphone converts it into an electrical signal, which is measured regularly -- *samples* are taken. The *sample rate* is measured in hertz ($1\ \mathrm{Hz} = 1\ \mathrm{s}^{-1}$) -- how many times per second the signal is measured. Compact disc quality recordings use $44.1$ kHz (CD); there are also standards with $48$ kHz (video, Opus), $88.2$ kHz or $96$ kHz.

**The Nyquist–Shannon theorem:** If a function $x(t)$ (after applying the Fourier transform) has no frequencies above $B$ hertz, then it can be fully reconstructed if its values are known at time intervals of ${\displaystyle \Delta t = \frac{1}{2B}}$. (*Nyquist-Shannon Sampling theorem*)

These two statements are equivalent

**Nyquist-Shannon 1:** A function $f(t)$ whose values are known at equal time intervals $\Delta T$ can be uniquely reconstructed from these values $\lbrace f_n \rbrace$ if and only if the energy spectrum of $f(t)$ contains no frequencies above $\frac{\pi}{\Delta T}\ \mathrm{rad/s}$.

**Nyquist-Shannon 2:** There is only one function $f(t)$ whose frequency spectrum lies entirely below $\frac{\pi}{\Delta T}$ that satisfies the given values $\lbrace f_n \rbrace$.

[Lecture10 in 2.161](https://ocw.mit.edu/courses/mechanical-engineering/2-161-signal-processing-continuous-and-discrete-fall-2008/lecture-notes/lecture_10.pdf).

**Intuition.** The sample rate must be **more than twice** the highest frequency of the signal. If samples are taken less often, a high frequency cannot be distinguished from a low one: the same samples also fit another, lower sine wave (*aliasing*). Therefore the signal is filtered before sampling, discarding frequencies above $f_s / 2$. People hear up to about $20$ kHz, so $44.1$ kHz and $48$ kHz are sufficient.

<img
  id="paraugu_nemsana"
  alt="Sampling a sine wave often and rarely"
  src="{{ '/lectures/lossy_video/figs/sampling.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

*A 7 Hz sine wave and its samples at three sample rates. At $8$ Hz the same points also fit a 1 Hz sine wave, because $\sin\left(2\pi \cdot 7 \cdot \frac{n}{8}\right) = -\sin\left(2\pi \cdot \frac{n}{8}\right)$.*

#### Bitrate, CBR and VBR

The *bitrate* -- how many bits per second the compressed sound takes -- is the most important compression parameter. An uncompressed compact disc recording is $44\,100$ samples per second $\times$ $16$ bits $\times$ $2$ channels $= 1411.2$ kbit/s. MP3 usually uses $128$--$320$ kbit/s (about $5$--$10$ times less), Opus uses $64$--$128$ kbit/s for music and $16$--$32$ kbit/s for speech.

* **Constant bitrate** (CBR): every second takes the same number of bits. It is easy to transmit over a fixed-rate channel, but too many bits are spent on simple parts (silence) and too few on complex ones.
* **Variable bitrate** (VBR): the encoder keeps a fixed *quality* (e.g., the LAME parameter `-V 0` ... `-V 9`), and the number of bits varies with the complexity of the signal -- how many instruments are playing, whether there is noise and transients. At the same average bitrate the quality is better, but the file size is not known exactly in advance, and older players had trouble determining the length of a track.
* **Constrained VBR** is a compromise: the bitrate varies, but over short time intervals does not exceed a certain limit. It is used for streaming and video calls.

#### Audible Frequencies, Critical Bands and Filter Banks

* The human ear can perceive sound frequencies from $20$ to $20\,000$ hertz. Middle-aged people hear only up to about $16\,000$ hertz (a *dog whistle* is at the edge of the audible range).
* The "A" of the first octave (or **A4**) uses a tuning fork called the **Stuttgart pitch**, at 440 Hz (it vibrates the air 440 times per second). If the frequency doubles, the sound is an octave higher.
* The "well-tempered" scale consists of $12$ semitones with equal frequency ratios between neighboring semitones.
* For example, the frequency ratio of "do" (C) and "do sharp" (C♯) is $1$ to $\sqrt[12]{2}$.

In the inner ear (the cochlea) each place responds to its own frequency region, so hearing works like a set of filters. The regions in which sounds affect each other's perception are called *critical bands*; there are about $24$ of them. At low frequencies the critical bands are narrow (about $100$ Hz), at high frequencies wide (several kHz): the ear resolves low frequencies much more finely. This scale is called the Bark scale.

**Analysis filter banks** imitate this structure of hearing: the encoder splits the sound signal into many frequency bands (usually with the MDCT -- the modified discrete cosine transform, see DCT in the image lecture) and quantizes each band separately -- as coarsely as hearing allows.

<img
  id="audio_joslas"
  alt="MP3 bands, critical bands of the ear and Opus bands"
  src="{{ '/lectures/lossy_video/figs/audio-bands.en.svg' | relative_url }}"
  style="width: 100%; max-width: 960px; border:none; background-color:#FFFFFF;"
/>

*The $32$ equal-width bands of the MP3 filter bank, the $24$ critical bands of the ear and the $21$ bands of Opus (CELT) on the same frequency axis.*

#### Frequency Masking

A loud sound makes quieter sounds of a nearby frequency inaudible (*frequency masking*). For each frequency a *masking threshold* can be computed -- the level below which a sound is inaudible. The encoder quantizes the signal so that the quantization noise in each band stays below this threshold: where the threshold is high, few bits can be spent. Masking is asymmetric: it reaches much further toward high frequencies than toward low ones.

<img
  id="frekvencu_maskesana"
  alt="Frequency masking"
  src="{{ '/lectures/lossy_video/figs/frequency-masking.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

*The threshold in quiet and the masking threshold of a $1$ kHz, $70$ dB tone (a simplified Bark-scale model). Tone A is louder than B, but it is inaudible, because it lies close to the masking tone.*

#### Temporal Masking

Masking also works in time (*temporal masking*): a loud sound masks quiet sounds about $100$--$200$ ms after it (*post-masking*) and -- for a much shorter time, about $5$--$20$ ms -- also before it (*pre-masking*). This matters for transform codecs: quantization noise spreads over the whole MDCT window. If the window is longer than pre-masking and a sharp beat starts in it after silence, the noise can be heard before the beat itself -- this is called *pre-echo*. Therefore codecs switch to short windows at transients.

<img
  id="temporala_maskesana"
  alt="Temporal masking"
  src="{{ '/lectures/lossy_video/figs/temporal-masking.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

*Pre-masking and post-masking (schematic) and the length of the long MDCT window of MP3.*

The figures are generated by the Python scripts [sampling.py]({{ '/lectures/lossy_video/figs/sampling.py' | relative_url }}), [audio_bands.py]({{ '/lectures/lossy_video/figs/audio_bands.py' | relative_url }}) and [masking.py]({{ '/lectures/lossy_video/figs/masking.py' | relative_url }}).

#### Stereo Sound

* *Joint Stereo* transmits the sound of the left and right ear in two channels: the sum in one channel, the difference in the other.
* Since both ears hear a very similar sound, the sum is an averaged sound, while the difference is small and compresses well.
* *Intensity stereo* transmits only one channel for high frequencies, plus the loudness ratio between the left and right side for each band, because at high frequencies the ear determines direction mainly by loudness.
* Human spatial perception of sound (*immersive sound*) is very nuanced: the direction/azimuth of a sound can be heard with 1 degree precision; the elevation above the horizon with about 10 degrees precision.
* It is still a hard problem how to place speakers and change what is heard in headphones when a person moves around a room. But MP3 does not address this.

### MP3

*MP3* (*MPEG-1 Audio Layer III*) was the first audio codec to spread massively on computers and the Internet, and it showed that a psychoacoustic codec can compress music about $10$ times with the listener barely noticing a difference.

**History.** MP3 was developed by the German Fraunhofer IIS institute (K. Brandenburg et al.) together with other organizations, based on research on auditory perception from the 1980s. It was standardized as part of MPEG-1 (ISO/IEC 11172-3, 1993), and in 1995 the file extension `.mp3` was chosen. Public MP3 player software appeared around 1994, and in 1997 the popular player Winamp. Napster appeared in 1999; it was an early file-sharing service, but it kept the file directory centrally, so it was taken to court and had to shut down in 2001. Still, the distribution of music in MP3 format continued (BitTorrent, as well as legal portable players such as the iPod from 2001 and online music stores) and completely changed the music industry.

**Features.**

* *Hybrid filter bank*: the signal is first split into $32$ bands of equal width (a polyphase filter bank), then each band is further split into $18$ frequency lines with the MDCT -- $576$ lines in total. At transients short windows ($6$ lines) are used to reduce pre-echo.
* *Psychoacoustic model*: the encoder computes the masking threshold and the signal-to-mask ratio for each band and allocates bits accordingly. The standard specifies only decoding, so the quality depends heavily on the encoder (for a long time the best one was the free program LAME).
* *Quantization and Huffman coding*: the MDCT coefficients are quantized non-uniformly (with the power $\frac{3}{4}$) and coded with one of $32$ fixed Huffman tables (see the lecture on [Huffman coding]({{ '/lectures/lossless_entropy_and_huffman/' | relative_url }})).
* *Bit reservoir*: in CBR mode a frame can use bits left unused by previous frames -- a small element of VBR within a CBR stream.
* *Frames* of $1152$ samples, bitrates $32$--$320$ kbit/s; *joint stereo* (M/S and intensity stereo).
* Limitations: at low bitrates high frequencies have to be cut off (at $64$ kbit/s -- above about $11$ kHz), pre-echo, encoder delay (a silence appears between songs without a pause unless it is specifically compensated).

**Licensing.** MP3 was protected by many patents; Fraunhofer IIS and Thomson (later Technicolor) sold licenses and collected fees from software and device manufacturers, especially for encoders. Therefore open-source projects could not freely distribute MP3 encoders: LAME was distributed only as source code ("LAME Ain't an MP3 Encoder"), and many Linux distributions did not include MP3 support until 2017. The unclear patent situation was one of the reasons why Xiph.Org developed the royalty-free codecs Vorbis and later Opus. The last patents expired around 2017, and Technicolor ended its licensing program; since then MP3 can be used freely.

Today MP3 is a *legacy* format: newer codecs (AAC, Opus) give better quality at the same bitrate, but MP3 is still supported by almost any device.

### Opus

*Opus* is an open and royalty-free audio codec standardized by the IETF in 2012 ([RFC 6716](https://www.rfc-editor.org/rfc/rfc6716)). It combines two codecs: Skype's speech codec SILK and Xiph.Org's music codec CELT. Opus is mandatory in WebRTC (video calls in browsers) and widely used: Discord, WhatsApp, YouTube (WebM audio), voice chats in games.

It may appear in file names, but it is often replaced by the extension of the container file.

* `audiofile.opus` (certainly encoded with Opus),
* `audiofile.ogg` (an Ogg container, if it does not use another codec such as Vorbis; the codec actually used can be seen in the Ogg metadata),
* `audiofile.webm` (a WebM container for streaming or web use)
* `audiofile.mka` (a Matroska or MKV container; the extension `*.mka` means audio only)

Opus can switch between modes that optimize different things -- either high sound quality, or the ability to adapt to transport channels of varying bandwidth and low latency.

**SILK Mode:** SILK mode is better suited for speech compression. SILK uses *Linear Predictive Coding* (LPC) instead of the MDCT: the speech signal is modeled as an excitation of the vocal cords passing through the filter of the vocal tract, and the filter parameters and the excitation are transmitted. The frequency band goes up to $8$ kHz.

**CELT Mode:** Usually used for music compression. CELT stands for Constrained Energy Lapped Transform. It uses the *Modified Discrete Cosine Transform* (MDCT) with very short frames ($2.5$--$20$ ms), so the latency is low.

**Hybrid mode:** low frequencies (up to $8$ kHz) are coded by SILK, high frequencies by CELT. The encoder can change the mode and the bitrate in every frame.

**CELT structure and psychoacoustics.** CELT groups the MDCT coefficients into $21$ bands that approximate the critical bands of the ear (see the figure above). The *energy* (loudness) of each band is coded separately and precisely -- this is where the name "constrained energy" comes from: even at a very low bitrate the spectral envelope (the loudness of each band) stays correct. The *shape* of a band (the normalized coefficient vector) is coded with a pyramid vector quantizer (*PVQ*). If very few bits are left for a band, it is filled with a "folded" spectrum of lower frequencies instead of being left empty -- this is why Opus keeps the high frequencies even at a low bitrate. At transients the frame is split into several short MDCTs to reduce pre-echo. Opus psychoacoustics is mostly built into the format itself (the bands, energy preservation) rather than into a separate masking model as in MP3.

**Entropy coding:** all symbols are coded with a *range coder* -- a variant of arithmetic coding (see the lecture on [arithmetic coding]({{ '/lectures/lossless_arithmetic_and_ans/' | relative_url }})).

**Bitrate modes:** VBR (the default), constrained VBR and hard CBR (`opusenc --vbr/--cvbr/--hard-cbr`, `ffmpeg -vbr on/constrained/off`); bitrates $6$--$510$ kbit/s. For network use there is built-in packet loss concealment, forward error correction (FEC) and discontinuous transmission of silence (DTX).

#### Comparing MP3 and Opus

For the comparison we use an $8$-second synthetic music sample ($48$ kHz, stereo) created by the Python script [audio_examples.py]({{ '/lectures/lossy_video/figs/audio_examples.py' | relative_url }}): $0$--$3$ s -- chords (a tonal signal with harmonics); $3$--$5.5$ s -- the same chords, "hi-hat" noise and sharp clicks; $5.5$--$7$ s -- a quiet $1$ kHz tone with a single isolated click; $7$--$8$ s -- silence. The script encodes it with `ffmpeg` (`libmp3lame` and `libopus`) and analyzes the decoded files.

| File | Codec | Mode | Size | Average bitrate | Play |
| --- | --- | --- | --- | --- | --- |
| [sample_ref.flac]({{ '/lectures/lossy_video/audio-examples/sample_ref.flac' | relative_url }}) | FLAC | lossless reference | 494 KB | -- | <audio controls preload="none" src="{{ '/lectures/lossy_video/audio-examples/sample_ref.flac' | relative_url }}"></audio> |
| [sample_mp3_cbr128.mp3]({{ '/lectures/lossy_video/audio-examples/sample_mp3_cbr128.mp3' | relative_url }}) | MP3 | 128 kbit/s CBR | 129 KB | 129 kbit/s | <audio controls preload="none" src="{{ '/lectures/lossy_video/audio-examples/sample_mp3_cbr128.mp3' | relative_url }}"></audio> |
| [sample_mp3_vbr_v5.mp3]({{ '/lectures/lossy_video/audio-examples/sample_mp3_vbr_v5.mp3' | relative_url }}) | MP3 | VBR (`-q:a 5`) | 97 KB | 97 kbit/s | <audio controls preload="none" src="{{ '/lectures/lossy_video/audio-examples/sample_mp3_vbr_v5.mp3' | relative_url }}"></audio> |
| [sample_mp3_cbr64.mp3]({{ '/lectures/lossy_video/audio-examples/sample_mp3_cbr64.mp3' | relative_url }}) | MP3 | 64 kbit/s CBR | 65 KB | 64 kbit/s | <audio controls preload="none" src="{{ '/lectures/lossy_video/audio-examples/sample_mp3_cbr64.mp3' | relative_url }}"></audio> |
| [sample_opus_vbr64.opus]({{ '/lectures/lossy_video/audio-examples/sample_opus_vbr64.opus' | relative_url }}) | Opus | 64 kbit/s VBR | 90 KB | 89 kbit/s | <audio controls preload="none" src="{{ '/lectures/lossy_video/audio-examples/sample_opus_vbr64.opus' | relative_url }}"></audio> |
| [sample_opus_cbr64.opus]({{ '/lectures/lossy_video/audio-examples/sample_opus_cbr64.opus' | relative_url }}) | Opus | 64 kbit/s CBR | 65 KB | 64 kbit/s | <audio controls preload="none" src="{{ '/lectures/lossy_video/audio-examples/sample_opus_cbr64.opus' | relative_url }}"></audio> |
| [sample_opus_vbr32.opus]({{ '/lectures/lossy_video/audio-examples/sample_opus_vbr32.opus' | relative_url }}) | Opus | 32 kbit/s VBR | 50 KB | 49 kbit/s | <audio controls preload="none" src="{{ '/lectures/lossy_video/audio-examples/sample_opus_vbr32.opus' | relative_url }}"></audio> |

**Bitrate over time.** In CBR files the bitrate is the same throughout the recording -- also in silence. VBR redistributes bits: MP3 VBR uses up to $200$ kbit/s in the noisy part, but about $30$ kbit/s in the quiet tone part; Opus VBR transmits almost nothing in silence. The "target" bitrate of VBR is the average for typical music -- for this complex sample (many harmonics, noise, transients) Opus VBR spent more bits than specified.

<img
  id="audio_bitu_atrums"
  alt="Bitrate over time"
  src="{{ '/lectures/lossy_video/figs/audio-bitrate.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

**Frequency band.** At a lower bitrate MP3 cuts off the high frequencies: the $64$ kbit/s file has nothing above about $11$ kHz. Thanks to band filling, Opus keeps frequencies up to $20$ kHz even at $32$ kbit/s (their exact values are not preserved, though -- what is preserved is the energy of each band).

<img
  id="audio_spektrs"
  alt="Average spectrum of the noisy part"
  src="{{ '/lectures/lossy_video/figs/audio-spectrum.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

**Pre-echo.** The figure shows the coding error (the decoded signal minus the original) around the isolated click ($6.25$ s). For all codecs the error starts already before the click, because the quantization noise spreads over the transform window; at a lower bitrate it is larger. Here the pre-echo lasts at most about $10$ ms -- within pre-masking --, so it is usually inaudible; with longer windows and without short windows it would be much more noticeable.

<img
  id="audio_pirmsatbalss"
  alt="Pre-echo around a click"
  src="{{ '/lectures/lossy_video/figs/audio-preecho.en.svg' | relative_url }}"
  style="width: 100%; max-width: 900px; border:none; background-color:#FFFFFF;"
/>

## H.264 Coding

*H.264*, or *MPEG-4 Part 10 / AVC* (*Advanced Video Coding*), is a video codec standardized jointly by the ITU-T and ISO/IEC MPEG working groups in 2003. It is the most widely used video codec: Blu-ray discs, digital television, streaming, video calls, cameras and phones; almost every device has a hardware decoder for it. The H.264 patents are licensed by a patent pool, which is why Google developed the royalty-free alternatives VP8 and VP9 (see the next section). The successors of H.264 are H.265/HEVC (2013) and H.266/VVC (2020).

Compared to the earlier MPEG-1 and MPEG-2 standards, the basic idea (I, P and B frames, motion compensation, residual transform) is the same, but H.264 introduces much more precise tools: for motion compensation a $16 \times 16$ macroblock can be split down to $4 \times 4$ blocks; motion vectors have $\frac{1}{4}$ pixel precision; a block can be predicted from several reference frames; in I-frames a block is predicted from already decoded neighbors (intra prediction); instead of the DCT, a $4 \times 4$ (and $8 \times 8$) integer transform is used; block boundaries are smoothed by an in-loop filter (*deblocking filter*); entropy coding uses CAVLC (variable-length codes) or CABAC (context-adaptive binary arithmetic coding).

### The Basic Idea of Video Compression

In the simplest view, video is a sequence of many raster images. Even encoding them with JPEG (each image separately) produces huge files. Consecutive images are strongly correlated (unless two pieces were edited together exactly at that point or the camera position changed abruptly).

**MPEG frame types:** MPEG is suitable both for statically compressed and for streamed data; each image is encoded in one of these 3 ways:

* I-frame (*intra-frame*) - a picture that is coded as a full image.
* P-frame (*predictive coded frame*) is based on the previous I-frame or P-frame
* B-frame (*bidirectionally predictive coded frame*) uses both the previous and the next frame, each of which can be an I- or a P-frame.

**Coding I-frames:** Similarly to JPEG (8x8 blocks), MPEG also codes equal blocks: 16x16 pixels. For I-frames the algorithm is similar to JPEG. I-frames are the "anchor points" on which the other frames are built. [YCbCr color plane](https://en.wikipedia.org/wiki/YCbCr) - not the same as YIQ.

### P-Frames and Motion Vectors

**Coding P-frames:** **Motion vector:** for a 16x16 pixel block of a P-frame, the most similar block is searched for in the previous I-frame or P-frame. Sometimes it may be shifted - if the video shows motion or the camera pans (*panning*).

<img
  id="p_freima_kodesana"
  alt="Encoding a P-frame macroblock with a motion vector"
  src="{{ '/lectures/lossy_video/figs/p-frame-encoding.en.svg' | relative_url }}"
  style="width: 100%; max-width: 960px; border:none; background-color:#FFFFFF;"
/>

*An example with real pixels (Python script [p_frame_encoding.py]({{ '/lectures/lossy_video/figs/p_frame_encoding.py' | relative_url }})). In the current frame the figure has moved by $(+6, +3)$ pixels and become slightly brighter. For the marked $16 \times 16$ macroblock, the encoder finds the most similar area in the reference frame (the green box) -- the offset to it is the motion vector $\mathrm{MV} = (-6, -3)$. The MV and the residual (the current block minus the prediction) are sent; the residual contains only the values $0$ and $4$; without motion compensation the residual would be much larger (sum of absolute differences $10\,658$ versus $720$).*

### B-Frames: Transmission and Display Order

**B-frames are postponed in the transmitted data:** a B-frame is predicted from both the previous and the next anchor frame (I or P), so the next anchor frame must be sent and decoded **before** the B-frames that precede it in display order. The decoder shows the B-frames immediately, but keeps the decoded anchor frame until its turn comes.

<img
  id="h264_freimu_seciba"
  alt="H.264 frame transmission and display order"
  src="{{ '/lectures/lossy_video/figs/h264-frame-order.en.svg' | relative_url }}"
  style="width: 100%; max-width: 910px; border:none; background-color:#FFFFFF;"
/>

*GOP pattern `IBBPBBPBBI`: on top -- the order in which the frames are sent (and decoded), at the bottom -- the display order. The transmission order is computed from the pattern by the Python script [h264_frame_order.py]({{ '/lectures/lossy_video/figs/h264_frame_order.py' | relative_url }}) (for example, `python h264_frame_order.py IBBBPBBBP`).*

H.264 generalizes this idea: B-frames can also be references for other B-frames (hierarchical B-frames), and a block can be predicted from several previous frames, so the transmission order can be more complex than in the figure.

If a film scene changes rapidly, it pays to use I-frames more often; if it is relatively static, mixed P-frames and B-frames. Codecs are usually optimized for some "average" rhythm.

### Examples of Compression Data

If the video is $356 \times 260$ pixels, the frame sizes and compression ratios are as follows:

| Frame | Size | Compression |
| --- | --- | --- |
| I-frame | 18 KiB | 7:1 |
| P-frame | 6 KiB | 20:1 |
| B-frame | 2.5 KiB | 50:1 |
| Average | 4.8 KiB | 27:1 |

The network connection needed to transmit such images:

$$
30\,\text{frames/s}\cdot 4.8\,\text{KiB/frame}\cdot 1024 \cdot 8 \approx 1.18\,\text{Mbit/s}.
$$

Together with audio this can be 1.45 megabits per second, which fills a T1 Internet connection (two twisted pair; 1.544 Mbps).

### Applications of H.264 and MPEG

* Satellite television broadcasts, which turn a digital signal from the satellite into a color TV signal (which may still be analog).
* Cable television.
* On-demand television with tens of thousands of downloadable or streamable films.

## VP9 Coding

*VP9* is an open and royalty-free (no license fees) video codec developed by Google. Its basic idea is the same as for the MPEG family of codecs: each frame is split into blocks, each block is *predicted* -- from already decoded neighbors in the same frame (*intra*) or from previous frames with a motion vector (*inter*) --, and only the prediction error, or *residual*, is coded: it is transformed (DCT or ADST), quantized and compressed with an arithmetic code.

**History.** VP9 continues the codecs of On2 Technologies (VP3, VP6, VP8); Google bought On2 in 2010 and opened VP8 as part of the WebM project. The VP9 bitstream was frozen in 2013. Compared to VP8 (and H.264), it gives files about a third to a half smaller at the same quality; it is used by YouTube, WebRTC video calls and browsers. The ideas of VP9 (and part of the unreleased VP10) became the basis of the AV1 codec (Alliance for Open Media, 2018), whose intra frames are the basis of AVIF images. The reference implementation is the *libvpx* library with the programs `vpxenc` (encoder) and `vpxdec` (decoder).

### Containers: IVF, WebM, MP4

The VP9 codec itself defines only the bit string of a *frame* (one coded picture); frame timing, dimensions and audio are stored by the container.

* **IVF** is the simplest container, used in libvpx tests and research tools. At the beginning of the file there is a $32$-byte header: the signature `DKIF`, the codec code (`VP90`), width, height, time base (e.g., $25$ frames per second) and the number of frames. After it, each record has a $12$-byte header (the data length in $4$ bytes and a timestamp in $8$ bytes) followed by the VP9 frame bit string itself. Since there is nothing else, IVF is convenient for cutting out, replacing or analyzing frames one by one.
* **WebM** is a subset of Matroska (MKV) used by browsers; it usually contains VP9 video and Opus audio. In the **MP4** container the VP9 stream code is `vp09`.
* **YouTube** offers most videos also in VP9 format (WebM, DASH streaming, each resolution as a separate video stream without audio). A downloaded WebM (respecting copyright and the terms of service) can be moved into an IVF container without transcoding: `ffmpeg -i video.webm -c:v copy -an video.ivf` (`-c:v copy` keeps the VP9 bits unchanged, `-an` drops the audio).

One IVF record can also contain several VP9 frames -- this is called a *superframe*: the frames are placed one after another, and at the end an index with the length of each frame is added. This is how a hidden frame and the next displayed frame are stored together (see the next subsection), so that each container record corresponds to exactly one displayed picture.

### Structure of a Video Clip: Frame Types and GOP

A VP9 frame has one of the following roles:

* **Keyframe** (`frame_type = KEY_FRAME`) -- all blocks are *intra*; the decoder can start from it, and it resets all references. Every clip starts with one (and so does every point one can "seek" to).
* **Inter frame** -- blocks can be predicted from up to three *reference frames*: `LAST` (usually the previous frame), `GOLDEN` (an older high-quality frame) and `ALTREF`. References are kept in $8$ memory slots (*reference slots*); the frame header field `refresh_frame_flags` specifies in which slots to store this frame after decoding.
* **Intra-only frame** -- only intra blocks (as in a keyframe), but the references are not reset.
* **Hidden ALTREF frame** (`show_frame = 0`) -- an inter frame that is decoded and stored as a reference but **not shown**. The encoder creates it from a *future* frame (usually temporally filtered, i.e., averaged over several neighboring frames and therefore less noisy) and predicts several following frames from it.
* **`show_existing_frame`** -- a frame a few bytes long without coded data, which simply shows an already decoded reference frame (e.g., a previously hidden ALTREF).

A *GOP* (*group of pictures*) is a group of frames from one "anchor" (a keyframe or ALTREF) to the next. Since ALTREF is a future frame that must be decoded **before** the frames predicted from it, the *decoding order* (the order of the frames in the file) differs from the *display order*. This is similar to MPEG B-frames (see the subsection "B-Frames: Transmission and Display Order" of the H.264 section), except that VP9 does not code separate B-frames but uses hidden frames.

<img
  id="vp9_gop"
  alt="VP9 decoding and display order"
  src="{{ '/lectures/lossy_video/figs/vp9-gop.en.svg' | relative_url }}"
  style="width: 100%; max-width: 960px; border:none; background-color:#FFFFFF;"
/>

*The first $16$ coded frames of the file `bouncing_ball_ARF.ivf` (see the gallery): $33$ IVF records contain $36$ coded frames, of which $3$ are hidden ALTREF frames, each in a superframe together with the next displayed frame.*

The encoder settings determine the GOP structure: in *low-delay* mode (`--lag-in-frames=0`) the encoder does not see future frames, so the decoding order equals the display order and there are no hidden frames (needed for video calls); with `--auto-alt-ref=1` and "look-ahead" into future frames (`--lag-in-frames=25`) ALTREF frames appear and compression improves (video on demand).

### Frame Structure: Headers, Tiles, Superblocks, Blocks

Each frame consists of three parts:

1. **Uncompressed header** -- in plain bits: frame type, `show_frame`, `show_existing_frame`, dimensions, choice of references, `refresh_frame_flags`, loop filter and quantization parameters (`base_q_idx`), segmentation, tile layout. It can be read without any arithmetic decoding.
2. **Compressed header** -- arithmetically coded: the transform size mode and corrections to the probability tables for this frame.
3. **Tile data** (*tiles*) -- the blocks themselves. A frame can be split into several tile columns (each at least $256$ pixels wide), which can be decoded in parallel; in each tile the arithmetic code starts afresh.

A tile is split into *superblocks* of $64 \times 64$ pixels, and each superblock is recursively partitioned (*partition*): a block can be left whole (`PARTITION_NONE`), split into two horizontal or vertical rectangles (`HORZ`, `VERT`) or into four squares (`SPLIT`), down to $8 \times 8$, and an $8 \times 8$ block also has $4 \times 4$ sub-blocks. For each *block* the following is stored:

* the prediction type (intra or inter) and the *mode*: for an intra mode -- the prediction direction, for an inter mode -- the reference frame and the motion vector;
* the transform size (`tx_size`) and the flag `skip` (if `skip = 1`, the residual of the block is $0$ and no coefficients are coded);
* the segment number (`segment_id`, see "Loop Filter and Segmentation").

Then come the quantized coefficients of the residual *transform blocks* (of size `tx_size`).

### YUV Pixels and Prediction

VP9 codes *YUV* (more precisely, YCbCr) pixel data: the luma plane $Y$ and two chroma planes $U$ and $V$ (see the section on color spaces and 4:2:0 subsampling in the JPEG and AVIF lecture). The basic profile (*profile 0*) is $8$ bits and 4:2:0, i.e., a $256 \times 256$ frame has $65\,536$ luma and $2 \cdot 16\,384$ chroma values. Profile 1 allows 4:2:2 and 4:4:4, profiles 2 and 3 allow $10$- or $12$-bit values (HDR). The encoder usually receives YUV frames (e.g., in a `.y4m` file: a text header and, for each frame, the $Y$, $U$, $V$ planes in bytes one after another), and the decoder outputs exactly the same planes. Two decoded streams are considered equal if all YUV planes match at the byte level (this is easy to check by comparing the SHA-256 of each frame).

**Intra prediction** fills a block from already decoded pixels above and to the left of it: VP9 has $10$ modes -- DC (the average value), vertical, horizontal, six diagonals and TM ("TrueMotion", continuation of the gradient).

**Inter prediction** takes a block from a reference frame, shifted by a *motion vector* (MV). Motion vectors have $\frac{1}{8}$ pixel (or $\frac{1}{4}$) precision. If the vector is not an integer, intermediate values are computed with an $8$-tap *interpolation filter* -- regular (`EIGHTTAP`), smooth (`EIGHTTAP_SMOOTH`) or sharp (`EIGHTTAP_SHARP`); if the filter of the frame is `SWITCHABLE`, it can be chosen for each block. For an integer (*full-pel*) vector all three filters give the same result. A block can also be predicted as the average of two references (*compound prediction*).

The motion vector itself is also predicted from neighboring blocks: the decoder builds two candidates from the neighbors, and the inter mode of the block chooses `NEARESTMV` (the first candidate), `NEARMV` (the second), `ZEROMV` (the zero vector) or `NEWMV` (codes the difference from a candidate). Therefore the same motion can often be written with several different symbols.

### Transform and Quantization: DCT and ADST

The residual is transformed in blocks of $4 \times 4$, $8 \times 8$, $16 \times 16$ or $32 \times 32$. The DCT or the *ADST* (*asymmetric discrete sine transform*) is used; the ADST suits intra blocks better, whose residual grows with the distance from the prediction edge. VP9 does not code the transform type (`tx_type`: DCT or ADST in each direction) separately: for intra blocks of the luma plane up to $16 \times 16$ it follows from the prediction direction, and for all others (inter blocks, chroma planes, $32 \times 32$) it is always DCT. All transforms are defined in integers (with rounding), so that the encoder and any decoder get bit-exact results.

The coefficients are quantized by dividing by the quantization step and rounding (see JPEG step 5). The step is determined by the *quantization index* `qindex` ($0 \ldots 255$; the larger, the coarser) through standard tables, separately for DC and AC coefficients; the `vpxenc` parameter `--cq-level` selects the target quality. The quantized coefficients are read in a certain *scan order* (similar to the JPEG zig-zag) and coded as *tokens*: `ZERO_TOKEN`, `ONE_TOKEN`, …, and for large values, categories with extra bits. The *EOB* (*end of block*) token means that the remaining coefficients are zeros; the field `eob` is the position in the scan order where coefficient coding ends.

### Arithmetic Coding and Probability Tables

Everything in a frame after the uncompressed header is coded with a *boolean arithmetic coder* -- a binary arithmetic code (see the lecture on [arithmetic coding]({{ '/lectures/lossless_arithmetic_and_ans/' | relative_url }})). Each bit has a probability of being $0$, written as a number $1 \ldots 255$ (i.e., $p/256$); a very predictable bit takes much less than $1$ bit. Symbols with several values (modes, tokens, partitions) are coded as a path in a binary tree, each tree node with its own probability.

The probabilities depend on the *context*: for example, the probability of `skip` depends on whether the neighboring blocks have `skip`, and the probability of a coefficient token depends on the transform size, the plane, the position and the neighboring coefficients. The collection of all probabilities is the *frame context* (the table `fc`). The decoder keeps $4$ such contexts; a frame chooses one (`frame_context_idx`), the compressed header can correct it (*forward update*), and after the frame is decoded the context can adapt to the actual symbol counts (*backward adaptation*) if the header fields `refresh_frame_context`, `error_resilient_mode` and `frame_parallel_decoding_mode` allow it.

### Encoder and Decoder State

VP9 is a stateful codec: a frame can be decoded only if all previous frames it depends on have been decoded. During decoding the following data structures are maintained (the encoder maintains exactly the same ones, so that it predicts in the same way as the decoder):

* $8$ **reference frame buffers** (decoded YUV planes) and their assignment to `LAST`, `GOLDEN`, `ALTREF`;
* $4$ **frame contexts** (probability tables) and symbol counters for adapting them;
* **a grid of the modes and motion vectors used in the blocks** -- the contexts of the neighbors (above and to the left) and the motion vectors of the previous frame, from which new vectors are predicted;
* the **segmentation map** and loop filter settings, which can be carried over from the previous frame.

Therefore changing the bytes of a frame also affects all subsequent frames that depend on it -- to check whether two streams give the same frames, the whole stream must be decoded from the beginning (or from a keyframe).

### Loop Filter and Segmentation

After the blocks are reconstructed, a **loop filter** is applied to the frame: it smooths block boundaries where there are only small differences (blocking artifacts) but keeps real edges. The filter strength is determined by the frame level (`filter_level` $0 \ldots 63$) and sharpness, as well as by the block modes, references and `skip`. The filtered frame is used both for display and as a reference for the following frames ("in the loop"). Therefore the decoded frame is compared **after** the loop filter: a symbol change that does not change the residual can still change pixels through the filter's decision.

**Segmentation** allows splitting the blocks into up to $8$ segments (`segment_id`); each segment can have its own quantization index, loop filter level, fixed reference frame or mandatory `skip`. The encoder uses this, for example, for adaptive quantization (`--aq-mode`): one `qindex` for complex areas, another for smooth ones.

### Lossless VP9: the Walsh–Hadamard Transform

If `base_q_idx = 0` and all quantization adjustments are $0$, the frame is **lossless** (`vpxenc --lossless=1`): the decoded pixels match the input YUV exactly. Then instead of DCT/ADST only the $4 \times 4$ *Walsh–Hadamard transform* (WHT) is used, and the loop filter is not applied.

The WHT basis vectors consist only of $\pm 1$; for example, in the $4 \times 4$ case

$$
H_4 = \left( \begin{array}{rrrr}
1 & 1 & 1 & 1 \\
1 & 1 & -1 & -1 \\
1 & -1 & -1 & 1 \\
1 & -1 & 1 & -1
\end{array} \right),
$$

so it is computed with additions, subtractions and shifts only. VP9 implements it with integer steps that can be inverted exactly (*lifting*): the coefficients give back exactly the same residual, without rounding errors. The DCT does not have this property -- its integer version is only an approximation, so even with the finest quantization a few units can change. In lossless mode no information is lost, and compression comes only from prediction and the arithmetic code, so the files are much larger (unless the content is very simple).

### Encoder Decisions: Rate-Distortion Optimization

The standard specifies only decoding; the encoder decides by itself how to partition superblocks and which modes, motion vectors, transform sizes and coefficients to choose. *Rate-distortion optimization* (RDO) makes these decisions by minimizing

$$
J = D + \lambda \cdot R,
$$

where $D$ is the distortion (e.g., the sum of squared errors between the original and the reconstructed block), $R$ is the number of bits needed for this option (computed from the current probabilities of the arithmetic code), and $\lambda$ is the "price of a bit", which grows with `qindex`. For each block the encoder tries many options and chooses the smallest $J$; even the quantized coefficients can be changed by $\pm 1$ if this saves more bits than the error grows (*trellis* quantization). A full search is very slow, so the `vpxenc` speed settings (`--good`/`--best`/`--rt`, `--cpu-used`) determine how many options are discarded by heuristics. In two-pass mode (`--passes=2`) the first pass collects statistics about the whole video, and the second pass uses them to distribute bits among frames and to place ALTREF frames.

Since RDO chooses the cheapest representation, in a typical stream each block has a "natural" choice of symbols. Often, however, the same decoded result can also be obtained with other symbols: for example, `skip = 0` for a block with a zero residual, a later `eob`, a different interpolation filter for an integer motion vector, or `NEARESTMV` instead of `NEWMV` if they give the same vector. Such "pixel-preserving" symbol changes can be used for steganography and watermarks (see "Applications of Codecs"), and rewriting to the natural RDO choice can be used to remove them.

### Gallery of Examples

These IVF files ($256 \times 256$ pixels unless stated otherwise, $33$ frames, $25$ frames per second, profile 0) are synthetic test videos encoded with `vpxenc`. In *LD* (*low delay*) files the decoding order equals the display order; *ARF* files contain hidden ALTREF frames in superframes. Uncompressed, one such clip ($33$ frames of 4:2:0) takes $3.2$ MB. The files can be played, for example, with `ffplay` or VLC, or converted to YUV with `vpxdec --i420 -o frames.yuv file.ivf`.

1. [white_static_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/white_static_LD.ivf' | relative_url }}) (1 KB) -- a static white frame. After the keyframe all blocks are `skip` with `ZEROMV`, so each subsequent frame takes only a few bytes.
2. [bouncing_ball_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/bouncing_ball_LD.ivf' | relative_url }}) (2 KB) -- a single-color ball moves $2$ pixels per frame over a single-color background. The inside of the ball is predicted with an integer motion vector, the background with `skip`.
3. [bouncing_ball_ARF.ivf]({{ '/lectures/lossy_video/vp9-examples/bouncing_ball_ARF.ivf' | relative_url }}) (2 KB) -- the same content in two-pass mode with ALTREF: $36$ coded frames, $3$ of them hidden, in superframes (see the diagram in "Structure of a Video Clip").
4. [integer_pan_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/integer_pan_LD.ivf' | relative_url }}) (6 KB) -- a fine three-color checkered texture moves by a whole number of pixels. The whole frame is well predicted by a single motion vector, so there is almost no residual, although the image is detailed.
5. [screen_content_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/screen_content_LD.ivf' | relative_url }}) (7 KB) -- screen content: single-color panels and scrolling "text". Large static areas and sharp edges.
6. [saturation_field_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/saturation_field_LD.ivf' | relative_url }}) (8 KB) -- a black and white field ($Y = 0$ and $Y = 255$) with a moving boundary. The reconstructed values are clipped to the interval $[0; 255]$.
7. [lowq_gradient_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/lowq_gradient_LD.ivf' | relative_url }}) (33 KB) -- a slowly changing smooth color gradient with a low `qindex` (high quality): many small AC coefficients and motion vectors with sub-pixel precision.
8. [midband_noise_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/midband_noise_LD.ivf' | relative_url }}) (1 MB) -- new random noise in every frame. Nothing is predictable, so the file is only about $3$ times smaller than the uncompressed video.
9. [lossless_wht_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/lossless_wht_LD.ivf' | relative_url }}) (2 KB) -- the ball content in lossless mode (`qindex` $0$, the Walsh–Hadamard transform, no loop filter); the decoded YUV matches the input exactly.
10. [clone_segment_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/clone_segment_LD.ivf' | relative_url }}) (2 KB) -- the ball content coded with segmentation (`--aq-mode=1`): the frame headers contain a segment map and several segments.
11. [yuv444_gradient_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/yuv444_gradient_LD.ivf' | relative_url }}) (68 KB) -- a color gradient in profile 1 with full-resolution chroma (4:4:4); the $U$ and $V$ planes have as many values as the $Y$ plane.
12. [hbd_gradient10_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/hbd_gradient10_LD.ivf' | relative_url }}) (23 KB) -- a gradient in profile 2 with $10$-bit values ($0 \ldots 1023$).
13. [tiled_multicolumn_LD.ivf]({{ '/lectures/lossy_video/vp9-examples/tiled_multicolumn_LD.ivf' | relative_url }}) (24 KB) -- $512 \times 256$ frames split into two tile columns that can be decoded in parallel.
14. [natural_clip_foreman_ARF.ivf]({{ '/lectures/lossy_video/vp9-examples/natural_clip_foreman_ARF.ivf' | relative_url }}) (74 KB) -- a real video (the classic test sequence *foreman*, a $256 \times 256$ crop) with camera motion, mixed intra and inter blocks, different transform sizes and hidden ALTREF frames.

## Applications of Codecs

### Steganography and Watermarks

Both technologies insert additional information into a media file that the viewer or listener does not notice, but they have opposite goals:

* **Steganography** hides the very **existence** of a message: an observer must not find out that an ordinary image, song or video contains a secret message. What matters most is imperceptibility and capacity; robustness against changes to the file is not required -- the sender and the receiver can usually agree to transfer the file unchanged.
* A **watermark** is not secret -- it may even be known that it is there --, but it must be bound to the content: it must remain readable after the file is transcoded, downscaled, cropped, or after someone tries to erase the watermark. It is used to indicate copyright, to find out which copy was leaked, or to verify that the content has not been changed.

![Embedding a watermark](figs/embedding-watermark.png)

*Embedding a watermark: from the original image and the watermark, the embedding procedure creates a watermarked image.*

**Where to hide data.** Data can be inserted into the content of a media file (pixels, audio samples), into the symbols of the compressed stream or into the metadata (headers). An extreme example is hiding information in network protocols: [Michal Drzymala, et al. Network Steganography in the DNS Protocol](http://www.czasopisma.pan.pl/Content/101654/PDF/47.pdf?handler=pdf).

* *Spatial* methods change pixels or samples directly, for example the least significant bits (*LSB*). They are simple and have a large capacity, but the first lossy compression erases them.
* *Spectral* methods change coefficients after a transform (DCT, DFT or wavelet transform). Quantization erases the highest-frequency coefficients first, so only fragile marks are placed there; robust watermarks are usually placed in the *middle* frequencies -- they are important enough for compression to keep them, but not as noticeable as low frequencies.
* *Compressed-stream* methods change coding decisions, not pixels: for example, the quantized DCT coefficients of JPEG or the symbols of a video codec -- motion vectors, prediction modes, the `skip` flag. The section "VP9 Coding" (see "Encoder Decisions: Rate-Distortion Optimization") describes how the same decoded frame can often be obtained with different symbols; such choices can carry hidden bits without changing a single pixel.

**Types of watermarks.**

* *Visible* watermarks -- a logo in the corner of a video, an image printed on all pages of a PDF file, or a stamp on page 17 of every book owned by a library; *invisible* watermarks mark the origin or the recipient of a file, sometimes also ensuring the *nonrepudiation* of this information.
* *Fragile* watermarks break under even small changes -- they help detect that a file has been modified; *robust* watermarks survive transcoding, scaling, cropping and deliberate attempts to remove them. Often both are needed: to establish the true origin of a file and also whether it has been changed on the way to the recipient.
* *Forensic* (individual) watermarks create a different copy for each user. Streaming services do this efficiently by preparing two variants with different marks for each video segment in advance (*A/B watermarking*): the sequence of variants a user receives encodes their identifier. If a film ends up on a pirate site (even filmed from a screen), the watermark reveals which account it was leaked from.

For watermarks, *capacity* -- how many bits can be inserted -- and low computational cost are also important: forensic watermarks have to be inserted into each copy separately, and detection has to work on large amounts of video.

**Attacks and defenses.**

* *Steganalysis* tries to determine whether a file contains a hidden message, usually without the original: it looks for statistical anomalies (e.g., in the histograms of least significant bits or DCT coefficients, which become atypical because of the hiding) or uses machine learning trained on clean and modified files.
* An *active warden* slightly transforms all passing files -- transcodes, downscales, or rewrites the compressed-stream symbols in a "canonical" form (the one an ordinary encoder would choose). This destroys steganography (and fragile watermarks) without degrading the content for the viewer.
* To attack robust watermarks, images (e.g., JPEG or other lossy-format images) can be compressed or transformed -- permuting pixels, cropping, scaling, geometric distortion, or combining several different copies by averaging them (*collusion*).

### Digital Rights Management (DRM)

*Digital Rights Management* (DRM) lets distributors of paid content (films, series, sports broadcasts) control who may play the content, for how long and on which device. The basic idea: the compressed video and audio stream is **encrypted**, and the decryption key is issued only to a licensed device. Encryption happens after compression (encrypted data can no longer be compressed), and decryption happens right before decoding.

**Common encryption (CENC).** The standard ISO/IEC 23001-7 *Common Encryption* (CENC) specifies how to encrypt MP4 (ISO base media file format) files with AES-128. Only the video and audio frame data are encrypted, while the container structure and the codec headers are left in the clear, so that the player can parse the file and jump to any position. There are two schemes: `cenc` (AES-CTR mode) and `cbcs` (AES-CBC, encrypting only some of the blocks, e.g., $1$ of every $10$). The key point is that **one and the same encrypted file** works with several DRM systems: the file contains a key identifier (KID), and each DRM system has its own `pssh` box with information on how to obtain a license. The content is usually prepared in fragmented MP4 files (CMAF, ISO/IEC 23000-19) and streamed with MPEG-DASH (ISO/IEC 23009-1) or Apple HLS (RFC 8216).

**DRM systems.**

* **Google Widevine** -- Chrome, Firefox, Android, Chromecast, many smart TVs. Security level L1 means that decryption and decoding happen in a protected hardware environment (*trusted execution environment*), L3 means software only; the highest-resolution content is usually issued only to L1 devices.
* **Apple FairPlay Streaming** -- Safari, iOS, macOS, Apple TV; uses HLS and the `cbcs` scheme.
* **Microsoft PlayReady** -- Edge, Windows, Xbox, many TVs and set-top boxes.

In a browser these systems are connected through the W3C standard *Encrypted Media Extensions* (EME, 2017): the JavaScript code of a web page receives the encryption information from the file, requests a license from the license server and passes it to the browser's *Content Decryption Module* (CDM). The CDM is closed software whose keys and decrypted frames are not accessible to the page; an open reference variant for testing is *ClearKey*.

**Limitations.** DRM cannot prevent the "analog hole": the screen can be filmed. Therefore DRM is complemented by output protection (HDCP encryption on the HDMI cable) and forensic watermarks that make it possible to find the source of a leak. DRM is also criticized for restricting legitimate use of content (e.g., backup copies) and for relying on closed software.

## Problems

**Problem 6.1 (the Nyquist theorem):** A music recording contains frequencies up to $20$ kHz.

* **(a)** What is the smallest sample rate at which this signal can still be reconstructed exactly?
* **(b)** What frequency will be heard in playback if a $20$ kHz tone is sampled without filtering at a sample rate of $32$ kHz?
* **(c)** Why was $44.1$ kHz chosen for the compact disc and not exactly $40$ kHz?

**Answer:**

**(a)** The sample rate must be greater than $2 \cdot 20 = 40$ kHz.

**(b)** After sampling, the frequencies $f$ and $f_s - f$ cannot be distinguished (just as in the lecture figure the samples of the $7$ Hz sine wave at $8$ Hz fit a $1$ Hz sine wave). So the $20$ kHz tone will sound like a $32 - 20 = 12$ kHz tone -- an audible distortion that was not in the original.

**(c)** Before sampling, the signal is filtered, discarding frequencies above $f_s / 2$. A real filter cannot go from "passes everything" to "passes nothing" at a single point; with $44.1$ kHz it has a band from $20$ kHz to $22.05$ kHz. $\square$

**Problem 6.2 (audio bitrate):** A song lasts $3$ minutes.

* **(a)** How many megabytes ($1$ MB $= 10^6$ bytes) does it take in uncompressed compact disc format ($44.1$ kHz, $16$ bits, stereo)?
* **(b)** How many in MP3 format at $128$ kbit/s and in Opus format at $64$ kbit/s? What are the compression ratios?
* **(c)** How many hours of MP3 music ($128$ kbit/s) fit into $1$ GB ($10^9$ bytes) of memory?

**Answer:**

**(a)** $44\,100 \cdot 16 \cdot 2 = 1\,411\,200$ bit/s; $1\,411\,200 \cdot 180 / 8 = 31\,752\,000$ bytes $\approx 31.8$ MB.

**(b)** MP3: $128\,000 \cdot 180 / 8 = 2\,880\,000$ bytes $= 2.88$ MB, compression ratio $1411.2 / 128 \approx 11$. Opus: $1.44$ MB, ratio $\approx 22$.

**(c)** $8 \cdot 10^9 / 128\,000 = 62\,500$ s $\approx 17.4$ hours. $\square$

**Problem 6.3 (uncompressed video):** A video is $1920 \times 1080$ pixels, $30$ frames per second, $8$-bit YUV with 4:2:0 chroma subsampling.

* **(a)** How many bytes does one frame take, and what is the bitrate of the uncompressed stream?
* **(b)** How would this change with 4:4:4 (no subsampling)?
* **(c)** A streaming service transmits this video with H.264 at $5$ Mbit/s. What is the compression ratio, and how many gigabytes does an hour of such video take?

**Answer:**

**(a)** $1920 \cdot 1080 = 2\,073\,600$ pixels; with 4:2:0 there are $1.5$ values per pixel, so $3\,110\,400$ bytes per frame. Bitrate: $3\,110\,400 \cdot 8 \cdot 30 \approx 746.5$ Mbit/s.

**(b)** With 4:4:4 there are $3$ values per pixel -- twice as many, about $1.49$ Gbit/s.

**(c)** $746.5 / 5 \approx 149$ times. An hour: $5 \cdot 10^6 \cdot 3600 / 8 = 2.25 \cdot 10^9$ bytes $= 2.25$ GB (uncompressed -- about $336$ GB). $\square$

**Problem 6.4 (I, P and B frames):** Use the frame sizes from the table "Examples of Compression Data" in the H.264 section (I-frame $18$ KiB, P-frame $6$ KiB, B-frame $2.5$ KiB) and $30$ frames per second.

* **(a)** The video is coded with a repeating GOP structure `IBBPBBPBB` ($9$ frames). What is the average frame size and the bitrate?
* **(b)** What would the bitrate be if all frames were I-frames (e.g., to make the video easy to edit frame by frame)?
* **(c)** In what order must the frames $I_0 B_1 B_2 P_3 B_4 B_5 P_6 B_7 B_8 I_9$ be sent?

**Answer:**

**(a)** One GOP has $1$ I, $2$ P and $6$ B frames: $(18 + 2 \cdot 6 + 6 \cdot 2.5) / 9 = 45 / 9 = 5$ KiB. Bitrate: $5 \cdot 1024 \cdot 8 \cdot 30 = 1\,228\,800$ bit/s $\approx 1.23$ Mbit/s.

**(b)** $18 \cdot 1024 \cdot 8 \cdot 30 \approx 4.42$ Mbit/s -- $3.6$ times more.

**(c)** Each anchor frame (I or P) must be sent before the B-frames that precede it in display order: $I_0 P_3 B_1 B_2 P_6 B_4 B_5 I_9 B_7 B_8$ (see the figure in "B-Frames: Transmission and Display Order"). $\square$

**Problem 6.5 (VP9 encoder parameters):** The same video is encoded with `vpxenc` in two ways:

* **A:** `--end-usage=q --cq-level=10 --good --cpu-used=0 --passes=2 --auto-alt-ref=1 --lag-in-frames=25`
* **B:** `--end-usage=q --cq-level=40 --rt --cpu-used=8 --passes=1 --auto-alt-ref=0 --lag-in-frames=0`

Compare the two results: (a) file size and quality; (b) encoding speed; (c) frame structure (hidden frames, decoding and display order); (d) which variant suits a video call and which one suits publishing a video.

**Answer:**

**(a)** The target quantization level of A (`--cq-level`, on a scale of $0$--$63$) is much lower, so `qindex` is also lower and quantization finer: the file will be much larger, but the quality high. B quantizes coarsely: the file is small, but blocks and blurred details are visible.

**(b)** A is much slower: `--good --cpu-used=0` makes RDO try very many options (block partitions, modes, motion vectors), and in two-pass mode the video has to be processed twice. B (`--rt --cpu-used=8`) discards most options with heuristics and works in real time.

**(c)** The A encoder sees $25$ future frames and creates hidden ALTREF frames (in superframes), so the decoding order differs from the display order. B is a *low-delay* stream: there are no hidden frames, and the frames are exactly in display order.

**(d)** Only B suits a video call: A has to wait for the $25$ following frames before outputting the first frame (about $1$ second of delay), and encoding is too slow. For publishing (e.g., on YouTube) A is better: it is encoded once but watched many times, so slow encoding pays off with better quality or a smaller file. $\square$

**Problem 6.6 (containers and codecs):**

* **(a)** The file `lecture.webm` contains VP9 video and Opus audio. Can it be converted to `lecture.mkv` without quality loss? And to an MP4 file for a device that supports only H.264 video and AAC audio?
* **(b)** Why does `ffmpeg -i video.webm -c:v copy -an video.ivf` not change the video quality and work very fast?
* **(c)** A friend renames `song.opus` to `song.mp3`. Does the file become an MP3 file?

**Answer:**

**(a)** Matroska (MKV) can contain both VP9 and Opus, so remuxing is enough (`ffmpeg -i lecture.webm -c copy lecture.mkv`) -- without loss. For a device that supports only H.264 and AAC, changing the container does not help: both streams must be decoded and re-encoded with other codecs, which is slow and degrades quality.

**(b)** `-c:v copy` copies the VP9 frame bits unchanged and only writes them into an IVF container (`-an` drops the audio, because IVF cannot store audio). Nothing is decoded or encoded.

**(c)** No. The extension is only part of the name; inside the file there is still an Ogg container with Opus audio. Many players determine the format from the file contents, others from the extension -- and then they will not play the file. $\square$

**Problem 6.7 (masking):** Look at the frequency masking figure in the section "Audio Coding".

* **(a)** Would a $1200$ Hz tone with a loudness of $45$ dB (tone A) be audible if the $1$ kHz masking tone were absent?
* **(b)** What can the encoder do with the band around $1200$ Hz while the masking tone is sounding?
* **(c)** Why, because of temporal masking, must the encoder switch to short transform windows before a sharp beat?

**Answer:**

**(a)** Yes: the threshold in quiet at $1200$ Hz is only a few decibels above zero, and a $45$ dB tone is clearly audible. It is masked only by the loud $1$ kHz tone.

**(b)** Quantize it very coarsely (or not code it at all): quantization noise up to about the level of the masking threshold ($\approx 48$ dB) will not be audible, so this band needs very few bits.

**(c)** Quantization noise spreads over the whole transform window. In a long window the noise also ends up in the silence before the beat, where it is covered only by the short pre-masking ($5$--$20$ ms), and it can be heard as pre-echo. In a short window the noise stays close to the beat, where the beat itself masks it. $\square$

## References

<a id="Guru14"></a>**[Guru14]** Guru, J. and Damecha, H. (2014). A review of watermarking algorithms for digital image. *Int. J. Innov. Res. Comput. Commun. Eng.*, 2, 5701--5708. Available at [https://api.semanticscholar.org/CorpusID:44191784](https://api.semanticscholar.org/CorpusID:44191784).

<a id="Pol16"></a>**[Pol16]** Yury Polyanskiy, *Information Theory*, MIT OpenCourseWare, Massachusetts Institute of Technology, Spring 2016. Available at [https://bit.ly/47EfIZ8](https://bit.ly/47EfIZ8), [Archived](https://web.archive.org/web/20240000000000*/https://ocw.mit.edu/courses/6-441-information-theory-spring-2016/).

**DRM standards:** ISO/IEC 23001-7 (*Common encryption in ISO base media file format files*, CENC); ISO/IEC 23000-19 (*Common Media Application Format*, CMAF); ISO/IEC 23009-1 (MPEG-DASH); [RFC 8216](https://www.rfc-editor.org/rfc/rfc8216) (HTTP Live Streaming); W3C [Encrypted Media Extensions](https://www.w3.org/TR/encrypted-media/).
