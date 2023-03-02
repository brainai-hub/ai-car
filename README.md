[<img src="https://i.ytimg.com/vi/Hc79sDi3f0U/maxresdefault.jpg" width="50%">](https://www.youtube.com/watch?v=Hc79sDi3f0U "Now in Android: 55")


import 'package:vimeo_video_player/vimeo_video_player.dart';

VimeoVideoPlayer(
  vimeoPlayerModel: VimeoPlayerModel(
    url: 'https://vimeo.com/70591644',
    systemUiOverlay: const [
      SystemUiOverlay.top,
      SystemUiOverlay.bottom,
      ],
   ),
);
