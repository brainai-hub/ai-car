<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Begin Jekyll SEO tag v2.8.0 -->
<title>YouTube embed example | youtube-embed</title>
<meta name="generator" content="Jekyll v3.9.2" />
<meta property="og:title" content="YouTube embed example" />
<meta property="og:locale" content="en_US" />
<meta name="description" content="An example how to embed YouTube videos in your GitHub Pages" />
<meta property="og:description" content="An example how to embed YouTube videos in your GitHub Pages" />
<link rel="canonical" href="https://codepo8.github.io/youtube-embed/demo.html" />
<meta property="og:url" content="https://codepo8.github.io/youtube-embed/demo.html" />
<meta property="og:site_name" content="youtube-embed" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary" />
<meta property="twitter:title" content="YouTube embed example" />
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebPage","description":"An example how to embed YouTube videos in your GitHub Pages","headline":"YouTube embed example","url":"https://codepo8.github.io/youtube-embed/demo.html"}</script>
<!-- End Jekyll SEO tag -->

    <link rel="stylesheet" href="/youtube-embed/assets/css/style.css?v=5a058b7485572b1d572649ec43f9170aa7cc1adf">
    <!-- start custom head snippets, customize with your own _includes/head-custom.html file -->

<!-- Setup Google Analytics -->



<!-- You can set your favicon here -->
<!-- link rel="shortcut icon" type="image/x-icon" href="/youtube-embed/favicon.ico" -->

<!-- end custom head snippets -->

  </head>
  <body>
    <div class="container-lg px-3 my-5 markdown-body">
      
      <h1><a href="https://codepo8.github.io/youtube-embed/">youtube-embed</a></h1>
      

      <h2 id="youtube-embed-example">YouTube embed example</h2>

<p>The YouTube URL of the video is https://www.youtube.com/watch?v=JLMbpiywVxQ.</p>

<p>Here is how to embed a clickable preview:</p>

<div class="language-markdown highlighter-rouge"><div class="highlight"><pre class="highlight"><code>[![Final video of fixing issues in your code in VS Code]
(https://img.youtube.com/vi/JLMbpiywVxQ/maxresdefault.jpg)]
(https://www.youtube.com/watch?v=JLMbpiywVxQ)
</code></pre></div></div>

<p>Which shows as:</p>

<p><a href="https://www.youtube.com/watch?v=JLMbpiywVxQ"><img src="https://img.youtube.com/vi/JLMbpiywVxQ/maxresdefault.jpg" alt="Final video of fixing issues in your code in VS Code" /></a></p>

<p>Here is how to embed the video:</p>

<p>{% include youtube.html id=”JLMbpiywVxQ” %}</p>

<div class="embed-container">
    <iframe width="640" height="390" src="https://www.youtube.com/embed/JLMbpiywVxQ" frameborder="0" allowfullscreen=""></iframe>
</div>
<style>
.embed-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  max-width: 100%;
}
.embed-container iframe,
.embed-container object,
.embed-container embed {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>

<p>To enable this, you need to create an <code class="language-plaintext highlighter-rouge">_includes</code> folder in your GitHub Pages root folder and include the <a href="/youtube-embed/youtube.html">youtube.html</a> file from this repository.</p>


      
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/anchor-js/4.1.0/anchor.min.js" integrity="sha256-lZaRhKri35AyJSypXXs4o6OPFTbTmUoltBbDCbdzegg=" crossorigin="anonymous"></script>
    <script>anchors.add();</script>
  </body>
</html>
