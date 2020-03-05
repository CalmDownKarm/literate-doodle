function renderVega(spec, container, data = null) {
    if (data) { // for the marimekko chart, data needs to be passed explicitly.
      spec.data[0].values = data
    }
    width = $(container).width()
    spec.width = width
    var view = new vega.View(vega.parse(spec))
      .renderer('svg')
      .logLevel(vega.Warn)
      .initialize(container)
      .hover()
      .run()
  }