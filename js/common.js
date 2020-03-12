function renderVega(spec, container, data = null) {
    if (data) { // for the marimekko chart, data needs to be passed explicitly.
      spec.data[0].values = data
    }
    width = $(container).width()
    height = $(container).height()
    spec.width = width
    // spec.height= height
    var view = new vega.View(vega.parse(spec))
      .renderer('svg')
      .logLevel(vega.Warn)
      .initialize(container)
      .hover()
      .run()
    return view
  }
