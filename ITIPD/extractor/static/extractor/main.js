(function() {
  var $, addDeleteHandler, color_selection, deleteMarkedRange, initializeCssAppliers, isBlank, isEmpty, redrawColors, resetColor, resetColors, root, showTypeMenu;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  $ = jQuery;

  root.types = [
    {
      name: "functionalityandbehavior",
      nicename: "Functionality and Behavior",
      id: 1,
      cssApplier: null
    }, {
      name: "concepts",
      nicename: "Concepts",
      id: 2,
      cssApplier: null
    }, {
      name: "directives",
      nicename: "Directives",
      id: 3,
      cssApplier: null
    }, {
      name: "purposes",
      nicename: "Purpose and Rationale",
      id: 4,
      cssApplier: null
    }, {
      name: "qualityattributes",
      nicename: "Quality Attributes and Internal Aspects",
      id: 5,
      cssApplier: null
    }, {
      name: "controlflow",
      nicename: "Control-Flow",
      id: 6,
      cssApplier: null
    }, {
      name: "structure",
      nicename: "Structure and Relationships",
      id: 7,
      cssApplier: null
    }, {
      name: "patterns",
      nicename: "Patterns",
      id: 8,
      cssApplier: null
    }, {
      name: "codeexamples",
      nicename: "Code Examples",
      id: 9,
      cssApplier: null
    }, {
      name: "environment",
      nicename: "Environment",
      id: 10,
      cssApplier: null
    }, {
      name: "externalreferences",
      nicename: "External References",
      id: 11,
      cssApplier: null
    }, {
      name: "noninformation",
      nicename: "Non-Information",
      id: 12,
      cssApplier: null
    }
  ];

  root.deletebutton = '#deletebutton';

  root.submitbutton = '#submitbutton';

  root.typemenu = '#typemenu';

  root.objecttext = '#objecttext';

  root.markedRanges = [];

  root.coloredRanges = [];

  $(function() {
    root.markedRanges = window.ranges_marked;
    ($(root.typemenu)).hide();
    ($(root.typemenu)).menu();
    ($(root.typemenu)).draggable();
    ($("#sortable")).sortable();
    ($("#sortable")).disableSelection();
    rangy.init();
    root.types = initializeCssAppliers();
    ($(root.deletebutton)).click(function() {
      root.markedRanges.length = 0;
      return resetColors();
    });
    ($(root.typemenu + " li")).click(color_selection);
    ($('body')).mouseup(function(e) {
      var currentSelection;
      currentSelection = rangy.getSelection();
      if (!isBlank(currentSelection || ($(root.typemenu)).is(':visible'))) {
        showTypeMenu(e.pageX, e.pageY);
      }
      if (isBlank(currentSelection)) return ($(root.typemenu)).hide();
    });
    ($(root.submitbutton)).click(function() {
      var data, htmlString;
      console.log(root.markedRanges);
      htmlString = ($(root.objecttext)).clone().html();
      data = JSON.stringify(root.markedRanges);
      return $.post('/pydoc/vote/', {
        range: data,
        html_text: htmlString,
        unit: ($("#documentationunitid")).attr("class")
      }, function(data) {
        console.log("ajax request successful");
        return window.location = '/pydoc/myunits';
      });
    });
    return redrawColors();
  });

  initializeCssAppliers = function() {
    return root.types.map(function(type) {
      return {
        name: type.name,
        nicename: type.nicename,
        id: type.id,
        cssApplier: rangy.createCssClassApplier(type.name, {
          normalize: true
        })
      };
    });
  };

  isEmpty = function(str) {
    return !str || str.length === 0;
  };

  isBlank = function(str) {
    return !str || /^\s*$/.test(str);
  };

  resetColors = function() {
    var type, _i, _len, _ref, _results;
    _ref = root.types;
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      type = _ref[_i];
      _results.push(resetColor(type));
    }
    return _results;
  };

  resetColor = function(type) {
    ($(root.objecttext)).find("span." + type.name).contents().unwrap();
    return ($('li.delete-list-entry')).remove();
  };

  showTypeMenu = function(atPositionX, atPositionY) {
    ($(root.typemenu)).css('left', atPositionX);
    ($(root.typemenu)).css('top', atPositionY);
    return ($(root.typemenu)).show();
  };

  color_selection = function(event) {
    var currentCharacterRange, currentRange, type, typeid, _i, _len, _ref;
    try {
      rangy.serializeRange(rangy.getSelection().getRangeAt(0), false, ($(root.objecttext))[0]);
    } catch (err) {
      rangy.getSelection().removeAllRanges();
      ($(root.typemenu)).hide();
      return;
    }
    typeid = $(this).attr("id");
    currentCharacterRange = rangy.getSelection().saveCharacterRanges(($(root.objecttext))[0]);
    _ref = root.types;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      type = _ref[_i];
      if (type.id === parseInt(typeid, 10)) type.cssApplier.applyToSelection();
    }
    ($(root.typemenu)).hide();
    resetColors();
    currentRange = rangy.serializeRange(rangy.getSelection().getRangeAt(0), false, ($(root.objecttext))[0]);
    root.markedRanges.push({
      type: typeid,
      serializedRange: currentRange,
      characterRange: currentCharacterRange
    });
    rangy.getSelection().removeAllRanges();
    return redrawColors();
  };

  /*
     This function draws all saved ranges in their respective colors to the objecttext.
     It also creates mouseover handlers for all those ranges.
  */

  redrawColors = function() {
    return root.markedRanges.map(function(elem) {
      var range;
      range = rangy.createRange(($(root.objecttext))[0]);
      range.selectCharacters(($(root.objecttext))[0], elem.characterRange[0].characterRange.start, elem.characterRange[0].characterRange.end);
      return root.types.map(function(type) {
        var nodes;
        if (type.id === parseInt(elem.type, 10)) {
          type.cssApplier.applyToRange(range);
          nodes = range.getNodes([1], function(el) {
            return rangy.CssClassApplier.util.hasClass(el, type.cssApplier.cssClass);
          });
          if (nodes.length === 0) nodes.push(range.startContainer.parentNode);
          return addDeleteHandler(nodes, elem.serializedRange, type.nicename);
        }
      });
    });
  };

  addDeleteHandler = function(nodes, serializedRange, name) {
    var deleteButton123,
      _this = this;
    deleteButton123 = $("<li>" + name + "</li>");
    deleteButton123.addClass('ui-state-default');
    deleteButton123.addClass('delete-list-entry');
    deleteButton123.on('click', {
      serializedRange: serializedRange
    }, function(event) {
      var i, index, range, _len, _ref;
      _ref = root.markedRanges;
      for (i = 0, _len = _ref.length; i < _len; i++) {
        range = _ref[i];
        if (event.data.serializedRange === range.serializedRange) index = i;
      }
      deleteMarkedRange(index);
      return event.currentTarget.remove();
    });
    nodes.map(function(node) {
      var _this = this;
      ($(node)).on('mouseover', {
        deleteButton: deleteButton123
      }, function(event) {
        event.data.deleteButton.css('border', '3px dotted red');
        ($(node)).css('border', '3px dotted red');
        ($(node)).css('border-left', 'none');
        return ($(node)).css('border-right', 'none');
      });
      ($(node)).on('mouseout', {
        deleteButton: deleteButton123
      }, function(event) {
        event.data.deleteButton.css('border', '1px solid #cccccc');
        return ($(node)).css('border', 'none');
      });
      deleteButton123.on('mouseover', {
        node: $(node)
      }, function(event) {
        event.data.node.css('border', '3px dotted red');
        event.data.node.css('border-left', 'none');
        event.data.node.css('border-right', 'none');
        return deleteButton123.css('border', '3px dotted red');
      });
      return deleteButton123.on('mouseout', {
        node: $(node)
      }, function(event) {
        event.data.node.css('border', 'none');
        return deleteButton123.css('border', '1px solid #cccccc');
      });
    });
    return ($('#sortable')).append(deleteButton123);
  };

  deleteMarkedRange = function(index) {
    if (index == null) index = root.markedRanges.length - 1;
    resetColors();
    root.markedRanges.splice(index, 1);
    return redrawColors();
  };

}).call(this);
