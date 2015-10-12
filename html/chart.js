// Get the contexts for each of the canvases
var sevenDayTimeAverage = document.getElementById(
    "sevenDayTimeAverage").getContext("2d");
var thirtyDayTimeAverage = document.getElementById(
    "thirtyDayTimeAverage").getContext("2d");

sevenDayTimeAverage.canvas.width = window.innerWidth / 3;
sevenDayTimeAverage.canvas.height = window.innerHeight / 3;
thirtyDayTimeAverage.canvas.width = window.innerWidth / 3;
thirtyDayTimeAverage.canvas.width = window.innerHeight / 3;

// Data definition
var sevenDayTimeAverage_data = {
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

var sevenDayTimeAverage_chart = new Chart(
    sevenDayTimeAverage).Bar(sevenDayTimeAverage_data);

Chart.defaults.global.responsive = true;

