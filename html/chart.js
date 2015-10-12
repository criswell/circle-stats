// Get the context of the canvas element we want to select
var ctx = document.getElementById("myChart").getContext("2d");

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;

// Data definition
var data = {
  labels: [
  {% for item in data[0].data|dictsort %}
    "{{ item[0] }}",
  {% endfor %}
    ],
  datasets: [
  {% for d in data %}
    {
      {% if d.branch is none %}
      label: "All Branches",
      {% else %}
      label: "{{ d.branch }}",
      {% endif %}

      {% if colors[d.branch] %}
      fillColor: "rgba({{ colors[d.branch][0] }},{{ colors[d.branch][1] }},{{ colors[d.branch][2] }},0.5)",
      strokeColor: "rgba({{ colors[d.branch][0] }},{{ colors[d.branch][1] }},{{ colors[d.branch][2] }},0.8)",
      highlightFill: "rgba({{ colors[d.branch][0] }},{{ colors[d.branch][1] }},{{ colors[d.branch][2] }},0.75)",
      highlightStroke: "rgba({{ colors[d.branch][0] }},{{ colors[d.branch][1] }},{{ colors[d.branch][2] }},1)",
      {% else %}
      fillColor: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},0.5)",
      strokeColor: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},0.8)",
      highlightFill: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},0.75)",
      highlightStroke: "rgba({{ colors[""][0] }},{{ colors[""][1] }},{{ colors[""][2] }},1)",
      {% endif %}
      data: [
      {% for item in d.data|dictsort %}
        {{ item[1] }},
      {% endfor %}
        ]
    },
    {% endfor %}
    ]
};

var myNewChart = new Chart(ctx).Bar(data);

Chart.defaults.global.responsive = true;

