var donutSpec={
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "description": "todo",
  "width": "200",
  "height": "200",
  "autosize": { "type": "fit", "contains": "padding", "resize":true },
  "signals": [{ "name": "radius", "update": "min(width, height)" }],
  "data": [
    {
      "name": "table",
      "url": "data/updates?_by=Status&_c=Status|count",
      "transform": [{ "type": "pie", "field": "Status|count" }]
    },
    {
      "name": "summary",
      "source": "table",
      "transform": [
        {
          "type": "aggregate",
          "groupby": [],
          "ops": ["sum"],
          "fields": ["Status|count"],
          "as": ["total"]
        }
      ]
    }
  ],
  "scales": [
    {
      "name": "color",
      "type": "ordinal",
      "domain": { "data": "table", "field": "Status" },
      "range": ["#1e7e34","#0062cc","#dc3545"]
    }
  ],
  "marks": [
    {
      "type": "arc",
      "from": { "data": "table" },
      "encode": {
        "update": {
          "fill": { "scale": "color", "field": "Status" },
          "x": { "signal": "width / 2" },
          "y": { "signal": "height / 2" },
          "startAngle": { "field": "startAngle" },
          "endAngle": { "field": "endAngle" },
          "innerRadius": { "signal": "radius / 3" },
          "outerRadius": { "signal": "radius / 2" },
          "tooltip": { "signal": "datum.Status" }
        }
      }
    },
    {
      "type": "text",
      "from": { "data": "summary" },
      "encode": {
        "enter": {
          "x": { "signal": "width / 2" },
          "y": { "signal": "height / 2" },
          "fill": { "value": "#000" },
          "align": { "value": "center" },
          "baseline": { "value": "middle" },
          "text": { "signal": "format(datum.total, '.2s')" },
          "fontSize": { "value": 28 },
          "fontWeight": { "value": "bold" },
          "fill":{"value": "#ffffff"}
        }
      }
    }
  ]
}
