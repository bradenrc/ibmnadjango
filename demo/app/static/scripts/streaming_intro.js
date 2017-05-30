function  BrunelVis(visId) {
  "use strict";                                                                       // strict mode
  var datasets = [],                                      // array of datasets for the original data
      pre = function(d, i) { return d },                         // default pre-process does nothing
      post = function(d, i) { return d },                       // default post-process does nothing
      transitionTime = 200,                                        // transition time for animations
      charts = [],                                                       // the charts in the system
      vis = d3.select('#' + visId).attr('class', 'brunel');                     // the SVG container

  BrunelD3.addDefinitions(vis);                                   // ensure standard symbols present

  // Define chart #1 in the visualization //////////////////////////////////////////////////////////

  charts[0] = function(parentNode, filterRows) {
    var geom = BrunelD3.geometry(parentNode || vis.node(), 0, 0, 1, 1, 5, 43, 93, 0),
      elements = [];                                              // array of elements in this chart

    // Define groups for the chart parts ///////////////////////////////////////////////////////////

    var chart =  vis.append('g').attr('class', 'chart1')
      .attr('transform','translate(' + geom.chart_left + ',' + geom.chart_top + ')');
    var overlay = chart.append('g').attr('class', 'element').attr('class', 'overlay');
    var zoom = d3.zoom().scaleExtent([1/3,3]);
    var zoomNode = overlay.append('rect').attr('class', 'overlay')
      .attr('x', geom.inner_left).attr('y', geom.inner_top)
      .attr('width', geom.inner_rawWidth).attr('height', geom.inner_rawHeight)
      .style('cursor', 'move').call(zoom)
      .node();
    zoomNode.__zoom = d3.zoomIdentity;
    chart.append('rect').attr('class', 'background').attr('width', geom.chart_right-geom.chart_left).attr('height', geom.chart_bottom-geom.chart_top);
    var interior = chart.append('g').attr('class', 'interior zoomNone')
      .attr('transform','translate(' + geom.inner_left + ',' + geom.inner_top + ')')
      .attr('clip-path', 'url(#clip_visualization_chart1_inner)');
    interior.append('rect').attr('class', 'inner').attr('width', geom.inner_width).attr('height', geom.inner_height);
    var gridGroup = interior.append('g').attr('class', 'grid');
    var axes = chart.append('g').attr('class', 'axis')
      .attr('transform','translate(' + geom.inner_left + ',' + geom.inner_top + ')');
    vis.append('clipPath').attr('id', 'clip_visualization_chart1_inner').append('rect')
      .attr('x', 0).attr('y', 0)
      .attr('width', geom.inner_rawWidth+1).attr('height', geom.inner_rawHeight+1);

    // Scales //////////////////////////////////////////////////////////////////////////////////////

    var scale_x = d3.scalePoint().padding(0.5)
      .domain(['Midwest', 'Mountain', 'Northeast', 'Pacific', 'South', 'South Atlantic'])
      .range([0, geom.inner_width]);
    var scale_inner = d3.scaleLinear().domain([0,1])
      .range([-0.5, 0.5]);
    var scale_y = d3.scaleLinear().domain([0, 450.00004])
      .range([geom.inner_height, 0]);
    var base_scales = [scale_x, scale_y];                           // untransformed original scales

    // Axes ////////////////////////////////////////////////////////////////////////////////////////

    axes.append('g').attr('class', 'x axis')
      .attr('transform','translate(0,' + geom.inner_rawHeight + ')')
      .attr('clip-path', 'url(#clip_visualization_chart1_haxis)');
    vis.append('clipPath').attr('id', 'clip_visualization_chart1_haxis').append('polyline')
      .attr('points', '-1,-1000, -1,-1 -5,5, -1000,5, -100,1000, 10000,1000 10000,-1000');
    axes.select('g.axis.x').append('text').attr('class', 'title').text('Region').style('text-anchor', 'middle')
      .attr('x',geom.inner_rawWidth/2)
      .attr('y', geom.inner_bottom - 2.0).attr('dy','-0.27em');
    axes.append('g').attr('class', 'y axis')
      .attr('clip-path', 'url(#clip_visualization_chart1_vaxis)');
    vis.append('clipPath').attr('id', 'clip_visualization_chart1_vaxis').append('polyline')
      .attr('points', '-1000,-10000, 10000,-10000, 10000,' + (geom.inner_rawHeight+1) + ', -1,' + (geom.inner_rawHeight+1) + ', -1,' + (geom.inner_rawHeight+5) + ', -1000,' + (geom.inner_rawHeight+5) );
    axes.select('g.axis.y').append('text').attr('class', 'title').text('Sum(Rain)').style('text-anchor', 'middle')
      .attr('x',-geom.inner_rawHeight/2)
      .attr('y', 4-geom.inner_left).attr('dy', '0.7em').attr('transform', 'rotate(270)');

    var axis_bottom = d3.axisBottom(scale_x).ticks(Math.min(10, Math.round(geom.inner_width / 124.5)));
    var axis_left = d3.axisLeft(scale_y).ticks(Math.min(10, Math.round(geom.inner_width / 20)));

    function buildAxes(time) {
      axis_bottom.tickValues(BrunelD3.filterTicks(scale_x))
      var axis_x = axes.select('g.axis.x');
      BrunelD3.transition(axis_x, time).call(axis_bottom.scale(scale_x)).selectAll('.tick text')
        .attr('transform', function() {
          var v = this.getComputedTextLength() / Math.sqrt(2)/2;
          return 'translate(-' + (v+6) + ',' + v + ') rotate(-45)'
      });
      var axis_y = axes.select('g.axis.y');
      BrunelD3.transition(axis_y, time).call(axis_left.scale(scale_y));
    }
    zoom.on('zoom', function(t, time) {
        t = t ||BrunelD3.restrictZoom(d3.event.transform, geom, this);
        scale_y = t.rescaleY(base_scales[1]);
        zoomNode.__zoom = t;
        interior.attr('class', 'interior ' + BrunelD3.zoomLabel(t.k));;
        build(time || -1);
    });

    // Define element #1 ///////////////////////////////////////////////////////////////////////////

    elements[0] = function() {
      var original, processed,                           // data sets passed in and then transformed
        element, data,                                 // brunel element information and brunel data
        selection, merged;                                      // d3 selection and merged selection
      var elementGroup = interior.append('g').attr('class', 'element1'),
        main = elementGroup.append('g').attr('class', 'main'),
        labels = BrunelD3.undoTransform(elementGroup.append('g').attr('class', 'labels').attr('aria-hidden', 'true'), elementGroup);

      function makeData() {
        original = datasets[0];
        if (filterRows) original = original.retainRows(filterRows);
        processed = pre(original, 0)
          .summarize('Rain=Rain:sum; Region=Region:base');
        processed = post(processed, 0);
        var f0 = processed.field('Region'),
          f1 = processed.field('Rain'),
          f2 = processed.field('#row'),
          f3 = processed.field('#selection');
        var keyFunc = function(d) { return f0.value(d) };
        data = {
          Region:       function(d) { return f0.value(d.row) },
          Rain:         function(d) { return f1.value(d.row) },
          $row:         function(d) { return f2.value(d.row) },
          $selection:   function(d) { return f3.value(d.row) },
          Region_f:     function(d) { return f0.valueFormatted(d.row) },
          Rain_f:       function(d) { return f1.valueFormatted(d.row) },
          $row_f:       function(d) { return f2.valueFormatted(d.row) },
          $selection_f: function(d) { return f3.valueFormatted(d.row) },
          _split:       function(d) { return 'ALL' },
          _key:         keyFunc,
          _rows:        BrunelD3.makeRowsWithKeys(keyFunc, processed.rowCount())
        };
      }

      // Build element from data ///////////////////////////////////////////////////////////////////

      function build(transitionMillis) {
        element = elements[0];
        var w = 0.9 * Math.abs(scale_x(scale_x.domain()[1]) - scale_x(scale_x.domain()[0]) );
        var x = function(d) { return scale_x(data.Region(d))};
        var h = geom.default_point_size;
        var y1 = scale_y.range()[0];
        var y2 = function(d) { return scale_y(data.Rain(d))};

        // Define selection entry operations
        function initialState(selection) {
          selection
            .attr('class', 'element bar filled')
        }

        // Define selection update operations on merged data
        function updateState(selection) {
          selection
            .each(function(d) {
              var width = w, left = x(d) - width/2,
              c = y1, d = y2(d), top = Math.min(c,d), height = Math.max(1e-6, Math.abs(c-d));
              this.r = {x:left, y:top, w:width, h:height};
            })
            .attr('x', function(d) { return this.r.x })
            .attr('y', function(d) { return this.r.y })
            .attr('width', function(d) { return this.r.w })
            .attr('height', function(d) { return this.r.h });
        }

        // Define labeling for the selection
        function label(selection, transitionMillis) {

          var tooltipLabeling  = {
            index: -1, method: 'box', location: ['center', 'top'], inside: true, align: 'middle', pad: 0, dy: 0.7,
            fit: true, granularity: 0,
            content: function(d) {
              return d.row == null ? null : '<span class="field">' + data.Rain_f(d) + '</span>'
            }
          };
          BrunelD3.addTooltip(selection, tooltipLabeling, geom);
        }
        // Create selections, set the initial state and transition updates
        selection = main.selectAll('.element').data(data._rows, function(d) { return d.key });
        var added = selection.enter().append('rect');
        merged = selection.merge(added);
        initialState(added);
        selection.filter(BrunelD3.hasData)
          .classed('selected', BrunelD3.isSelected(data))
          .filter(BrunelD3.isSelected(data)).raise();
        updateState(BrunelD3.transition(merged, transitionMillis));
        label(merged, transitionMillis);

        BrunelD3.transition(selection.exit(), transitionMillis/3)
          .style('opacity', 0.5).each( function() {
            this.remove(); BrunelD3.removeLabels(this);
        });
      }

      return {
        data:           function() { return processed },
        original:       function() { return original },
        internal:       function() { return data },
        selection:      function() { return merged },
        makeData:       makeData,
        build:          build,
        chart:          function() { return charts[0] },
        group:          function() { return elementGroup },
        fields: {
          x:            ['Region'],
          y:            ['Rain'],
          key:          ['Region']
        }
      };
    }();

    function build(time, noData) {
      var first = elements[0].data() == null;
      if (first) time = 0;                                           // no transition for first call
      buildAxes(time);
      if ((first || time > -1) && !noData) {
        elements[0].makeData();
      }
      elements[0].build(time);
    }

    // Expose the following components of the chart
    return {
      elements : elements,
      interior : interior,
      scales: {x:scale_x, y:scale_y},
      zoom: function(params, time) {
          if (params) zoom.on('zoom').call(zoomNode, params, time);
          return d3.zoomTransform(zoomNode);
      },
      build : build
    };
    }();

  function setData(rowData, i) { datasets[i||0] = BrunelD3.makeData(rowData) }
  function updateAll(time) { charts.forEach(function(x) {x.build(time || 0)}) }
  function buildAll() {
    for (var i=0;i<arguments.length;i++) setData(arguments[i], i);
    updateAll(transitionTime);
  }

  return {
    dataPreProcess:     function(f) { if (f) pre = f; return pre },
    dataPostProcess:    function(f) { if (f) post = f; return post },
    data:               function(d,i) { if (d) setData(d,i); return datasets[i||0] },
    visId:              visId,
    build:              buildAll,
    rebuild:            updateAll,
    charts:             charts
  }
}


