/* The following code is auto-generated. Beward of Dragons! */

// Get the contexts for each of the canvases

{% for d in data %}
// Context("{{ d.id }}")
var ctx_{{ d.id }} = document.getElementById("{{ d.id }}").getContext("2d");
ctx_{{ d.id }}.canvas.width = window.innerWidth / 2.5;
ctx_{{ d.id }}.canvas.height = window.innerHeight / 3;

var data_{{ d.id }} = {
  labels: [
  {% for item in d.data[0].data|dictsort %}
    "{{ item[0] }}",
  {% endfor %}
    ],
  datasets: [
  {% for ds in d.data %}
    {
      {% if ds.branch is none %}
      label: "All Branches",
      {% else %}
      label: "{{ ds.branch }}",
      {% endif %}
      {% if colors[ds.branch] %}
      fillColor: "rgba({{ colors[ds.branch][0] }},{{ colors[ds.branch][1] }},{{ colors[ds.branch][2] }},0.5)",
      strokeColor: "rgba({{ colors[ds.branch][0] }},{{ colors[ds.branch][1] }},{{ colors[ds.branch][2] }},0.8)",
      highlightFill: "rgba({{ colors[ds.branch][0] }},{{ colors[ds.branch][1] }},{{ colors[ds.branch][2] }},0.75)",
      highlightStroke: "rgba({{ colors[ds.branch][0] }},{{ colors[ds.branch][1] }},{{ colors[ds.branch][2] }},1)",
      {% else %}
      fillColor: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},0.5)",
      strokeColor: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},0.8)",
      highlightFill: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},0.75)",
      highlightStroke: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},1)",
      {% endif %}
       data: [
      {% for item in ds.data|dictsort %}
        {{ item[1] }},
      {% endfor %}
        ]
    },
  {% endfor %}
  ]
};

{% if d.chart_type is equalto "bar" %}
var chart_{{ d.id }} = new Chart(ctx_{{ d.id }}).Bar(data_{{ d.id }});
{% else %}
// Defaults to Line
var chart_{{ d.id }} = new Chart(ctx_{{ d.id }}).Line(data_{{ d.id }});
{% endif %}

Chart.defaults.global.responsive = true;

{% endfor %}
