var marimekkoSpec = {
  "$schema": "https://vega.github.io/schema/vega/v5.json",
  "description": "todo",
  "width": 390,
  "height": 250,
  "padding": 5,
  "autosize": {"type": "fit", "contains": "padding"},
  "data": [
    {
      "name": "table",

      "transform": [
        {"type": "nest", "keys": ["Department", "Status"]},
        {
          "type": "treemap",
          "field": "Status|count",
          "method": "slicedice",
          "ratio": 1,
          "paddingInner": 1,
          "size": [{"signal": "height"}, {"signal": "width"}],
          "as": ["y0", "x0", "y1", "x1", "depth", "children"]
        }
      ]
    },
    {
      "name": "labels",
      "source": "table",
      "transform": [{"type": "filter", "expr": "datum.x0 == 0"}]
    }
  ],
  "scales": [
    {
      "name": "color",
      "type": "ordinal",
      "domain": {"data": "table", "field": "Status"},
      "range": ["#1e7e34","#0062cc","#dc3545"]
    }
  ],
  "marks": [
    {
      "type": "rect",
      "from": {"data": "table"},
      "encode": {
        "update": {
          "x": {"field": "x0"},
          "y": {"field": "y0"},
          "x2": {"field": "x1"},
          "y2": {"field": "y1"},
          "fill": {"scale": "color", "field": "Status"},
          "tooltip": {"signal": "datum"}
        }
      }
    },
    {
      "type": "text",
      "from": {"data": "labels"},
      "encode": {
        "update": {
          "y": {"signal": "(datum.y0 + datum.y1)/2"},
          // "x": {"value": -5},
          "text": {"field": "Department"},
          "align": {"value": "top"},
          // "angle":{"value": -45},
          "fontStyle":{"value":"italic"}
        }
      }
    }
  ]
}
