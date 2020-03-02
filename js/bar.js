function getBarSpec(field) {
  return {
    "$schema": "https://vega.github.io/schema/vega/v5.json",
    "description": "Standard bar charts display the ranks of values much more easily when sorted into order",
    "width": 400,
    "height": 250,
    "padding": 5,
    "autosize": { "type": "fit", "contains": "padding" },
    "data": [
      {
        "name": "source",
        "url": `data/updates?Status=Fulfilled&_by=${field}&_c=${field}|count&_sort=-${field}|count&_limit=5`
      }
    ],
    "scales": [
      {
        "name": "yscale",
        "type": "band",
        "domain": {
          "data": "source",
          "field": `${field}`,
          // "sort": {"op": "median", "field": "Sales", "order": "descending"}
        },
        "range": "height",
        "padding": 0.25,
        "round": true
      },
      {
        "name": "xscale",
        "domain": { "data": "source", "field": `${field}|count` },
        "nice": true,
        "range": "width"
      }
    ],
    "axes": [
      { "orient": "bottom", "scale": "xscale", "format": "s" , "labelColor":"#ffffff"},
      // { "orient": "left", "scale": "yscale" }
    ],
    "marks": [
      {
        "type": "rect",
        "from": { "data": "source" },
        "encode": {
          "enter": {
            "y": { "scale": "yscale", "field": `${field}` },
            "height": { "scale": "yscale", "band": 1 },
            "x": { "scale": "xscale", "field": `${field}|count` },
            "x2": { "scale": "xscale", "value": 0 },
            "fill": { "value": "#1D81B2" },
            "tooltip": { "signal": `{'Completed Updates': datum["${field}|count"]}` }
          }
        }
      },
      {
        "type": "text",
        "from": { "data": "source" },
        "encode": {
          "update": {
            "y": { "scale": "yscale", "field":`${field}` },
            "dy":{"value": 20},
            "text": { "field": `${field}` },
            "align": { "value": "left" },
            "fontSize": { "value": 15 },
            // "fontStyle": { "value": "italic" },
            "fill": { "value": "#ffffff" }

          }
        }
      }
    ]
  }
}
