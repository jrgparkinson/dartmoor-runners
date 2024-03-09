---
layout: page
title: Previous Series
permalink: /Previous Series/
---

{% for series in site.previous_series reversed %}
  <h3>
    <a href="{{ series.url }}">
      {{ series.title }}
    </a>
  </h3>
{% endfor %}