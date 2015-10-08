// Get the context of the canvas element we want to select
var ctx = document.getElementById("myChart").getContext("2d");

ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;

// Data definition
var data = {
  labels: [
  {% for item in data.data|dictsort %}
    "{{ item[0] }}",
  {% endfor %}
    ],
  datasets: [
    {
      label: "All Branches",
      fillColor: "rgba(220,220,220,0.5)",
      strokeColor: "rgba(220,220,220,0.8)",
      highlightFill: "rgba(220,220,220,0.75)",
      highlightStroke: "rgba(220,220,220,1)",
      data: [
      {% for item in data.data|dictsort %}
        {{ item[1] }},
      {% endfor %}
        ]
    },
    {% for b in bdata|dictsort %}
      {
        label: "{{ b[0] }}",
        fillColor: "rgba(151,187,205,0.5)",
        strokeColor: "rgba(151,187,205,0.8)",
        highlightFill: "rgba(151,187,205,0.75)",
        highlightStroke: "rgba(151,187,205,1)",
        data: [
        {% for item in b[1].data|dictsort %}
          {{ item[1] }},
        {% endfor %}
          ]
      },
    {% endfor %}
    ]
};

var myNewChart = new Chart(ctx).Bar(data);

Chart.defaults.global.responsive = true;

