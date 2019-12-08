<h2 style="margin-bottom:0; padding-top: 20px">[PROJECTS]</h2>

{% for prj in site.prj_menu %}
<div style="padding-top:10px">
  {% if page.url contains prj[1] %}
  > <strong style="color:orange">{{ prj[0] }}</strong>
  {% else %}
  > <a href="{{ site.url }}/prjct/{{ prj[1] }}.html">{{ prj[0] }}</a>
  {% endif %}
</div>
{% endfor %}

