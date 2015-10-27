/* The following code is auto-generated. Beward of Dragons! */

// Get the contexts for each of the canvases

var ctx = document.getElementById("mainDisplay").getContext("2d");
ctx.canvas.width = window.innerWidth * 0.9;
ctx.canvas.height = window.innerHeight * 0.85;

{% set last_id = data[-1].id %}

var chart = null;

function drawLineChart(data){
    if(chart!=null){
        chart.destroy();
    }
    chart = new Chart(ctx).Line(data, {animateScale: true});
}

function drawBarChart(data){
    if(chart!=null){
        chart.destroy();
    }
    chart = new Chart(ctx).Bar(data, {animateScale: true});
}

{% for d in data %}

var data_{{ d.id }} = {
  labels: [
  {% if d.data_type is equalto 'top-builds' %}
    {% for item in d.data[0].data|dictsort|reverse %}
      "{{ item[1] }}",
    {% endfor %}
  {% else %}
    {% for item in d.data[0].data|dictsort %}
      "{{ item[0] }}",
    {% endfor %}
  {% endif %}
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
      {% if d.data_type is equalto "top-builds" %}
        {% for item in ds.data|dictsort|reverse %}
          {{ item[0] }},
        {% endfor %}
      {% else %}
        {% for item in ds.data|dictsort %}
          {{ item[1] }},
        {% endfor %}
      {% endif %}
        ]
    },
  {% endfor %}
  ]
};

{% endfor %}

{% for d in data %}

function runCycle_{{ d.id }}() {
  document.getElementById('label').innerHTML = "{{ d.label }}";
  {% if d.chart_type is equalto "bar" %}
    drawBarChart(data_{{ d.id }});
  {% else %}
    drawLineChart(data_{{ d.id }});
  {% endif %}
  setTimeout(function() { runCycle_{{ last_id }}(); }, 5000);
}

{% set last_id = d.id %}

{% endfor %}

Chart.defaults.global.responsive = true;

function runCycle() {
  runCycle_{{ data[0].id }}();
}
