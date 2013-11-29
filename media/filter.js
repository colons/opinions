function parse_path(path) {
  var filter = {};
  var matcher = /^([^=]+)=([^=]+)$/;

  $.each(path.split("/"), function(i, element) {
    var match = matcher.exec(element);
    if (match) {
      filter[match[1]] = match[2];
    } else if (element) {
      filter.title = element;
    }
  });
  return filter;
}

function apply_filter(filter, func) {
  /* apply func(review, true) or func(review, false) depending on if a review matches */
  var type;
  var title;

  if ('title' in filter) {
    title = filter.title;
    func(everything_but(title), false);
    func($('tr.review#'+title), true);
  }
  else if ('type' in filter) {
    type = filter.type;
    func(reviews_not_of_type(type), false);
    func(reviews_of_type(type), true);
  }
  else if ('stars' in filter) {
    type = filter.stars + '-star';
    func(reviews_not_of_type(type), false);
    func(reviews_of_type(type), true);
  }
  else {
    func($('tr.review'), true);
  }
}

function visible(review, selected) {
  if (selected) {
    show(review);
  } else {
    hide(review);
  }
}

function highlight(review, selected) {
  /* set a review as highlighted */
  if (selected) {
    review.addClass('selected');
  }
}

function hide(review) {
  review.removeClass('visible').addClass('invisible');
}

function show(review) {
  review.addClass('visible').removeClass('invisible');
}

function unhighlight() {
  /* reset highlighting state */
  $('tr.review.selected').removeClass('selected');
  $('table.reviews.hovering').removeClass('hovering');
}

function reviews_of_type(type) {
  return $('tr.review.'+type);
}

function reviews_not_of_type(type) {
  return $('tr.review:not(.'+type+')');
}

function everything_but(title) {
  return $('tr.review:not(#'+title+')');
}

$('document').ready(function() {
  var path = window.location.pathname;
  var filter = parse_path(path);
  apply_filter(filter, visible);

  var filter_links = $('.type a, td.title h2 a, td.stars a, a.home');

  filter_links.click(function(e) {
    $('body').removeClass('init');
    e.preventDefault();
    path = $(this).attr('href');
    window.history.pushState(null, $(this).text(), path);
    filter = parse_path(path);
    apply_filter(filter, visible);
  });

  filter_links.hover(function(e) {
    $('body').removeClass('init');
    path = $(this).attr('href');
    $('table.reviews').addClass('hovering');
    filter = parse_path(path);
    apply_filter(filter, highlight);
  }, function(e) {
    unhighlight();
  });
});
