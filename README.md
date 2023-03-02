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


