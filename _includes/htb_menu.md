<h2 style="margin-bottom:0; padding-top: 20px">[HTB BOXES]</h2>

{% for box in site.htb_menu %}
<div style="padding-top:10px">
  {% if page.url contains box[1] %}
  > <strong style="color:orange">{{ box[1] }}</strong>
  {% else %}
  > <a href="{{ site.url }}/boxes/{{ box[0] }}_{{ box[1] }}.html">{{ box[1] }}</a>
  {% endif %}
</div>
{% endfor %}

