<h2 style="margin-bottom:0; padding-top: 20px">[HTB CHALLENGES]</h2>

{% for htb in site.htb_chls %}
<div style="padding-top:10px">
  > <a href="{{ site.url }}/chals/htb/challenges.html#{{ htb[0] }}">
  {% if page.url contains htb[0] %}
  <strong style="color:orange">{{ htb[1] }}</strong>
  {% else %}
  {{ htb[1] }}
  {% endif %}
  </a>
</div>
{% endfor %}
