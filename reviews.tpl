<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>the music for the blind review</title>
    <link href='http://fonts.googleapis.com/css?family=Cinzel' rel='stylesheet' type='text/css'>
    <link href='http://fonts.googleapis.com/css?family=Gilda+Display' rel='stylesheet' type='text/css'>
    <link href='/m/css' rel='stylesheet' type='text/css'>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
    <script src='/m/js/filter' type='text/javascript'></script>
  </head>
  <body>
    <h1><span class="the">The</span> <span class="mftb"><span class="music">Music</span>&nbsp;for the&nbsp;Blind</span> <span class="review">Review<span></h1>
    
    <p class="types">
      <span class="type"><a href="/">all</a></span>

      %typecount = len(types)
      %for type, slug in types:
        - <span class="type"><a href="/type={{ slug }}/">{{ type }}s</a></span>
      %end
    </p>
    
    <table class="reviews">
      %for review in reviews:
        <tr class="review {{ review['typeslug'] }} {{ review['stars'] }}-star" id="{{ review['slug'] }}">
          <td class="title">
            <h2>
              <a href="/{{ review['slug'] }}">
                %if 'artist' in review:
                  <span class="artist">{{ review['artist'] }}</span> -
                %end

                {{ review['title'] }}
              </a>
            </h2>
          </td>

          <td class="type"><a href="/type={{ review['typeslug'] }}/">{{ review['type'] }}</a></p>

          <td class="words">
            {{!review['words_string']}}
          </td>

          <td class="stars">
            %if 'stars' in review:
              <a href="/stars={{ review['stars'] }}/">
                %for i in xrange(1,6):
                  %if review['stars'] >= i:
                    <span class="star">★</span>\\
                  %else:
                    <span class="nonstar">★</span>\\
                  %end
                %end
              </a>
            %end
          </td>
        </tr>
      %end
    </table>

    <p class="footer">
      <a href="https://twitter.com/mftb"><img class="bird" src="/m/svg/bird" alt="twitter"></a>
      <a href="https://github.com/colons/review"><img class="octocat" src="/m/svg/octocat" alt="github"></a>
    </p>
  </body>
</html>

