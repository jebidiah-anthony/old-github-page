<h2 style="margin-bottom:0; padding-top:20px">[CTF EVENTS]</h2>

{% for ctf in site.ctf_menu %}
<div style="padding-top:10px">
  > <a href="{{ site.url }}/chals/ctf/{{ ctf[1] }}-{{ ctf[0] }}.html">
  {% if page.url contains ctf[0] %}
  <strong style="color:orange;text-decoration:none">{{ ctf[2] }} {{ ctf[1] }}</strong>
  {% else %}
  {{ ctf[2] }} {{ ctf[1] }}
  {% endif %}
  </a>
</div>
{% endfor %}
